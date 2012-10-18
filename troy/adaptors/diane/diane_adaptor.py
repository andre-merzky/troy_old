import troy.cpi
#import api.base
#import saga
import os
import sys
from stat import *
from subprocess import *
import shutil
#from multiprocessing.connection import Client
from troy.api import State
import troy.config
from troy.pilotjob import PilotJob
from string import Template
import xmlrpclib



"""
Job States

* Unknown
  Not part of the SPEC...

* New
  This state identies a newly constructed job instance which has not yet run.
  This state corresponds to the BES state Pending. This state is initial.

* Running     
  The run() method has been invoked on the job, either explicitly or implicitly.
  This state corresponds to the BES state Running. This state is initial.

* Done    
  The synchronous or asynchronous operation has finished successfully. It
  corresponds to the BES state Finished. This state is final.

* Canceled    
  The asynchronous operation has been canceled, i.e. cancel() has been called on
  the job instance. It corresponds to the BES state Canceled. This state is final.

* Failed  
  The synchronous or asynchronous operation has finished unsuccessfully. It
  corresponds to the BES state Failed. This state is final.

* Suspended   
  Suspended identifies a job instance which has been suspended. This state
  corresponds to the BES state Suspend. 

"""



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

#class DianeAdaptor(object):
#
#    def __init(self):
#        print 'bla'

class DianeAdaptor(troy.cpi.TroyAdaptor):
    
    def __init__(self, database_host=None):  

        self.master_host = troy.config.adaptor_config('diane', 'master_host')
        self.master_port = troy.config.adaptor_config('diane', 'master_port')

        #self.TROYDIANE_DIR = os.path.abspath(os.path.join(os.path.abspath(__file__), ".."))
        #os.system(self.TROYDIANE_DIR + "/run_master.sh")

        print "Connecting to DIANE master on %s:%s ..." % (self.master_host, self.master_port)
        try:
            self.rpcproxy = xmlrpclib.ServerProxy('http://%s:%s/' % (self.master_host, self.master_port),
                verbose=False, allow_none=True)
        except Exception as err:
            print 'ERROR:', err
            sys.exit(-1)


    def __del__(self):
        # TODO: kill the right master, not the most recent
        #print 'Killing the master'
        #import os
        #os.system("diane-master-ping kill")
        pass

    def start_pilotjob(self, rm, pj_desc, context=None):

        pj = PilotJob()
        try:
            pj.pj_id = self.rpcproxy.start_pilotjob(rm, pj_desc)
        except Exception as err:
            print 'ERROR:', err
            sys.exit()

        return pj


    def get_state_detail(self): 
        # TODO
        print 'get_state_detail'
        return "running"
    
    def cancel(self):        
        # TODO: kill master? agents?
        pass
                    
    def submit_schedunit(self, su):

        self.rpcproxy.submit_schedunit(su.description, su.su_id)



    def get_su_state(self, su):

        state = self.rpcproxy.get_su_state(su.su_id)

        return state

    def get_su_state_detail(self, su):        

        detail = self.rpcproxy.get_su_state_detail(su.su_id)

        return detail
    
    
