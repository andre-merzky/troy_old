from diane import IApplicationWorker, SimpleTaskScheduler, \
        SimpleApplicationManager, IApplicationManager
from diane.BaseThread import BaseThread
from diane.FileTransfer import FileTransferOptions
import time
import os
import glob
import shutil
import subprocess
import stat
from SimpleXMLRPCServer import SimpleXMLRPCServer
from SimpleXMLRPCServer import SimpleXMLRPCRequestHandler
import xmlrpclib
import sys
from string import Template

try:
    import troy.config
    from troy.api import State
except:
    print 'WARNING: import of troy failed, not a problem for the worker.'



def chmod_executable(path):
    "make a file executable"
    os.chmod(path,stat.S_IXUSR|os.stat(path).st_mode)

def get_uuid():
    wd_uuid=""
    if sys.version_info < (2, 5):
        uuid_str = os.popen("/usr/bin/uuidgen").read()
        wd_uuid += uuid_str.rstrip("\n")

        #preparation for fail-safe exit
        #sys.stderr.write('Incompatible Python version found! Please use Python 2.5 or higher with BigJob!')
        #sys.exit(-1)
    else:
        import uuid
        wd_uuid += str(uuid.uuid1())
    return wd_uuid

class TaskInput:
    def __init__(self):
        self.exe = None
        self.return_code = None

class WorkerData:
    def __init__(self):
        self.basedir = None

def get_rundir():
    #p1 = Popen(["diane-ls"], stdout=PIPE)
    #p2 = Popen(["head", "-n1"], stdin=p1.stdout, stdout=PIPE)
    #p3 = Popen(["cut", "-f1", "-d "], stdin=p2.stdout, stdout=PIPE)
    #p2.stdout.close()  # Allow p2 to receive a SIGPIPE if p2 exits.
    #p1.stdout.close()  # Allow p1 to receive a SIGPIPE if p2 exits.
    #rundir = p3.communicate()[0].strip()

    troy.config.read_config()
    rundir_base = troy.config.adaptor_config('diane', 'rundir_base')

    f = open(rundir_base + 'index')
    index = f.readline().strip()
    f.close()
    rundir = rundir_base + index.lstrip('I').zfill(4)

    return rundir


class BigJobDianeManager(SimpleApplicationManager, BaseThread):
    "This is the main application loop"


    def __init__(self,name=None,auto_register=True):

        print "Initializing Manager"
        self.TROYDIANE_DIR = os.path.abspath(os.path.join(os.path.abspath(__file__), "../.."))

        self.basedir = '.'
        BaseThread.__init__(self,name=name)
        SimpleApplicationManager.__init__(self)

    def list_files(self,pattern,dir=''):
        return [os.path.join(dir,os.path.basename(f)) for f in
                glob.glob(os.path.join(self.basedir,dir,pattern))]

    def start_pilotjob(self, rm, pj_desc, context=None):

        print 'pj_desc(backend):', pj_desc

        number_nodes = pj_desc['number_of_processes']

        working_directory = pj_desc['working_directory']
        try:
            self.substitutes = pj_desc['substitutes']
        except:
            self.substitutes = {}

        workers_per_node = 1 # pj_desc.processes_per_host

        # self.pj = PilotJob()

        print "Submit Diane Worker"

        print 'submitting worker, resource url: %s workdir: %s number of nodes: %s' \
                % (rm, working_directory, number_nodes)
        os.system("%s/submit_worker.sh %s %s %s %s" \
                % (self.TROYDIANE_DIR, rm, working_directory, number_nodes, workers_per_node))

        self.rundir = get_rundir()
        print 'Rundir:', self.rundir

        #self.state = 'New'

        # self.__setup_connection()

        # self.pilot_url = "diane://"

        #self.pj.state = 'Unknown'
        self.pj_id = get_uuid()
        print 'id of diane master:', self.pj_id

        return str(self.pj_id)

    def handle_file_transfer(self, su_desc, su_id):

        print 'Handling file transfers ...'

        for f in su_desc['file_transfer']:
            print f

            loc = f.split()[0]
            op = f.split()[1]
            rem = f.split()[2]

            if op == '>':
                print 'Found an input file:', loc

                dstdir = os.path.join(self.rundir,'input', su_id)
                if not os.path.isdir(dstdir):
                    os.mkdir(dstdir)
                os.symlink(loc, os.path.join(dstdir, rem))

            elif op == '<':
                print 'Found an output file:', loc
                dstdir = os.path.join(self.rundir,'output', su_id)
                if not os.path.isdir(dstdir):
                    os.mkdir(dstdir)
                open(os.path.join(dstdir, loc), 'w').close()
            else:
                print 'Oops! Dont know how handle this file transfer'

    def submit_schedunit(self, su_desc, su_id):
        print "Starting Submit_job ..."

        # return 'hello world'

        scriptname = '/tmp/' + su_id + ".sh"
        f = open(scriptname, 'w')
        f.write('#!/bin/sh\n')
        f.write(\
            Template(su_desc['executable']).substitute(self.substitutes)
        )
        for a in su_desc['arguments']:
            f.write(' ' + Template(a).substitute(self.substitutes))
        f.write('\n')
        f.close()
        os.chmod(scriptname, 0755)

        shutil.move(scriptname,os.path.join(self.rundir,'submitted'))

        self.handle_file_transfer(su_desc, su_id)

        return True

    def get_su_state(self, su_id):

        scriptname = su_id + '.sh'

        state = "None"

        if os.path.isfile(self.rundir + '/submitted/' + scriptname ):
            state = State.Unknown
        if os.path.isfile(self.rundir + '/scheduled/' + scriptname ):
            state = State.New

        if os.path.isfile(self.rundir + '/running/' + scriptname):
            state = State.Running
        elif os.path.isfile(self.rundir + '/done/' + scriptname):
            state = State.Done
        elif os.path.isfile(self.rundir + '/canceled/' + scriptname):
            state = State.Canceled
        elif os.path.isfile(self.rundir + '/failed/' + scriptname):
            state = State.Failed

        # print 'DEBUG: job state:', state
        return state

    def get_su_state_detail(self, su_id):

        scriptname = su_id + '.sh'

        state = "None"

        if os.path.isfile(self.rundir + '/uploading/' + scriptname):
            state = "Uploading"
        if os.path.isfile(self.rundir + '/running/' + scriptname):
            state = "Running"
        if os.path.isfile(self.rundir + '/downloading/' + scriptname):
            state = "Downloading"

        return state

    def __setup_listener(self):

        # Create server
        self.rpcserver = SimpleXMLRPCServer(("194.171.96.52", 8000), logRequests=False)
#        self.rpcserver.register_introspection_functions()

        self.rpcserver.register_function(self.start_pilotjob)
        self.rpcserver.register_function(self.submit_schedunit)
        self.rpcserver.register_function(self.get_su_state)
        self.rpcserver.register_function(self.get_su_state_detail)

        # timeout to wait for a client request
        self.rpcserver.timeout = 0.1



    def initialize(self, run_data):
        print "Initializing Diane Application Manager"
        w = WorkerData()
        w.basedir = self.basedir
        self.worker_init = w

        self.__setup_listener()

        # create dirs and clean up garbage
        for d in ['submitted', 'scheduled', 'running', 'done', 'failed',
            'exit_codes', 'canceled', 'cancel-request', 'stderr','stdout',
            'stdin', 'input', 'output', 'uploading', 'downloading']:
            if not os.access(os.path.join(self.basedir,d),os.F_OK):
                print "Creating directory ",os.path.join(self.basedir,d)
                os.mkdir(os.path.join(self.basedir,d))

#            if d!='submitted':
#                old_jobs = self.list_files(d+'/*')
#                for f in old_jobs:
#                    print "Removing file ",f," from directory ",d
#                    os.remove(os.path.join(self.basedir,d,f))

        self.scheduler.job_master.file_server.servant.setAuthorizedDirs('/home/marksant')    

        return []


    def run(self):
        while self.scheduler.has_more_work():
            # print "Application loop ..."

            self.rpcserver.handle_request()

            new_jobs = self.list_files('submitted/*')

            for f in new_jobs:
                print "Found new task, scheduling it"
                shutil.move(os.path.join(self.basedir,'submitted',f),os.path.join(self.basedir,'scheduled'))

                d=self._task()
                d.task_input = TaskInput()
                d.task_input.exe = 'scheduled/'+f

                # input
                input_dir = os.path.join(self.basedir, 
                        'input', f.rsplit('.sh', 1)[0])
                if os.path.isdir(input_dir):
                    d.task_input.input_files = \
                        [os.path.join(input_dir, x) for x in os.listdir(input_dir)]
                else:
                    print 'INFO: No input dir present, is that correct?'
                    d.task_input.input_files = []

                # output
                output_dir = os.path.join(self.basedir, 
                        'output', f.rsplit('.sh', 1)[0])
                if os.path.isdir(output_dir):
                    d.task_input.output_files = \
                        [os.path.join(output_dir, x) for x in os.listdir(output_dir)]
                else:
                    print 'INFO: No output dir present, is that correct?'
                    d.task_input.output_files = []

                # inform scheduler that there are new tasks
                self.scheduler.todo_tasks.put(d)

            #time.sleep(2)

    def tasks_done(self, tasks):
        for f in tasks:
            #print "Task ",f.task_input.exe," is done: moving it to directory 'done'"
            shutil.move(f.task_input.exe,'done')
            #in case the task has been put in the running dir
            os.remove(os.path.join('running',os.path.basename(f.task_input.exe)))
            os.remove(os.path.join('downloading',os.path.basename(f.task_input.exe)))
            os.remove(os.path.join('uploading',os.path.basename(f.task_input.exe)))

        
    def has_more_work(self):
             return 1

class BigJobDianeData:
    def __init__(self):
        print "Initializing Data"
        self.basedir = '.'


class BigJobDianeScheduler(SimpleTaskScheduler):
#    def __init__(self, job_master, appmgr):
        #SimpleTaskScheduler.__init__(self, job_master, appmgr)
        #self.todo_tasks = PilotTodoTaskQueue(appmgr)
#        job_master.file_server.servant.setAuthorizedDirs('/home/marksant')    

    def tasks_failed(self, tasks):
        for f in tasks:
            print "Task ",f.task_input.exe," failed: moving it to \
                    directory 'failed'"
            shutil.move(f.task_input.exe,'failed')
            #in case the task has been put in the running dir
            os.remove(os.path.join('running',
                    os.path.basename(f.task_input.exe)))

#    def worker_initialized(self, w_entry):
#        """This method is called by RunMaster when the worker agent
#        sucessfully initialized and optionally returned initialization output
#        (w_entry.init_output).  Until this method returns the worker will not
#        be fully initialized (so the framework will not mark it as a ready
#        worker)."""
#
#        print 'Worker Initialized'
#        SimpleTaskScheduler.worker_initialized(self, w_entry)
#        pass

#    def worker_removed(self, w_entry):
#        """This method is called when the worker has been removed (either
#        lost or terminated due to some reason)."""
#
#        print 'Worker Removed'
#        SimpleTaskScheduler.worker_removed(self, w_entry)
#        pass

#    def worker_added(self, w_entry):
#        """This method is called by RunMaster when the new worker agent is
#        added.  The w_entry parameter is an instance of WorkerEntry class.
#        Application specific initialization data may be assigned to
#        w_entry.init_input at this point."""
#
#        print 'Worker Added'
#        SimpleTaskScheduler.worker_added(self, w_entry)
#        pass


class BigJobDianeWorker(IApplicationWorker):
    def initialize(self,worker_data):
        print "Initializing worker"
        self.worker_data = worker_data
        return None

    def do_work(self, task_input):
        self.file_transfer = self._agent.ftc
        self.allow_overwrite = FileTransferOptions(overwrite=True)

        execFile = os.path.join(self.worker_data.basedir,task_input.exe)
        print "Downloading ",execFile
        localExecName = os.path.basename(execFile)
        self.file_transfer.download(localExecName,execFile)

        #uploads executable to 'upload' directory
        self.file_transfer.upload("./"+localExecName,"uploading/"+localExecName,opts=self.allow_overwrite)

        # download input files
        for f in task_input.input_files:
            self.file_transfer.download(os.path.basename(f), f)
            chmod_executable(os.path.basename(f))

        #uploads executable to 'running' directory
        self.file_transfer.upload("./"+localExecName,"running/"+localExecName,opts=self.allow_overwrite)

        outFile = open ( 'std.out', 'w' )
        errFile = open ( 'std.err', 'w' )
        print "Executing ",localExecName
        chmod_executable('./'+localExecName)
        process = subprocess.Popen(['./'+localExecName],stdout=outFile,
                stderr=errFile)
        return_code = process.poll()

        while return_code is None:
            self.file_transfer.upload("./std.out",'stdout/'+localExecName+'.std.out',
                    opts=self.allow_overwrite)
            self.file_transfer.upload("./std.err",'stderr/'+localExecName+'.std.err',
                    opts=self.allow_overwrite)
            #self.file_transfer.download("std.in",localExecName+".std.in")
            return_code = process.poll()
            time.sleep(5)

        print "Done. Exit code was ", return_code

        #uploads executable to 'running' directory
        self.file_transfer.upload("./"+localExecName,"downloading/"+localExecName,opts=self.allow_overwrite)

        # download input files
        for f in task_input.output_files:
            self.file_transfer.upload(os.path.basename(f), f,
                    opts=self.allow_overwrite)

        task_input.return_code=return_code

        if return_code!=0:
            raise Exception('Application exited with code '+str(return_code))

        return None


# the run function is called when the master is started
# input.data stands for run parameters
def run(input,config):
    print "Diane master starting ..."

    input.scheduler = BigJobDianeScheduler
    input.manager = BigJobDianeManager
    input.worker = BigJobDianeWorker
    input.data = BigJobDianeData()
