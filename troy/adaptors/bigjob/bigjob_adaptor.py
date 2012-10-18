import os
import troy.cpi
import troy.config
from troy.pilotjob import PilotJob
import saga
from troy.api import State
from string import Template

from bigjob.bigjob_manager import bigjob, subjob

# BigJob Interface
#
# class bigjob
#     def __init__(self, database_host):
#     def start_pilot_job(self,
#                 lrms_url,
#                 bigjob_agent_executable,
#                 number_nodes,
#                 queue,
#                 project,
#                 working_directory,
#                 userproxy,
#                 walltime,
#                 processes_per_node=1)
#    def get_state(self):
#    def get_state_detail(self):
#    def cancel(self):
#
# class subjob(object):
#    def __init__(self, database_host):
#    def submit_job(self, pilot_url, jd):
#    def get_state(self):
#    def cancel(self):


  

#
# This is the BigJob Troy Adaptor
# It implements the Abstract TroyAdaptor class
# 
#
class BigJobAdaptor(troy.cpi.TroyAdaptor):
    def __init__(self):
        self.coordination_url = troy.config.adaptor_config('bigjob', 'coordination_url')
        
        print 'coordination_url:', self.coordination_url

        # map between subjobs and workunits
        self.sj2su = {}
        self.su2sj = {}


    def start_pilotjob(self, rm, pj_desc, context=None):
        lrms_url = rm 
        nodes = int(pj_desc.total_core_count)/int(pj_desc.processes_per_host)
        userproxy = None
        workingdirectory=pj_desc.working_directory  # working directory for agent

        self.substitutes = pj_desc.substitutes

        self.bj = bigjob(self.coordination_url)

        self.bj.start_pilot_job(lrms_url,
                            None,
                            nodes,
                            None,
                            None,
                            workingdirectory,
                            userproxy,
                            None)
        
        
        # Create a PilotJob object to give back to application
        self.pj = PilotJob()
        
        # Map the PilotJob object to the BigJob object
        #self.pj2bj[pj] = bj
        #self.bj2pj[bj] = pj
        
        # The BigJob ID is suitable as an ID, so use it
        self.pj.pj_id = self.bj.uuid
   
        return self.pj

    def cancel(self):
        
        self.bj.cancel()

            
    def submit_schedunit(self, su):
        """ Submit a scheduling unit to this pilot job. """
        
        jd = saga.job.description()
        
        jd.executable = \
            Template(su.description.executable).substitute(self.substitutes)
        jd.arguments = [ Template(a).substitute(self.substitutes) \
                        for a in su.description.arguments ]

        jd.number_of_processes = str(su.description.number_of_processes)
        jd.working_directory = su.description.working_directory 
        jd.output = su.description.output
        jd.error = su.description.error

        sj = subjob()
        sj.submit_job(self.bj.pilot_url, jd)
        
        self.sj2su[sj] = su
        self.su2sj[su] = sj
        
    def get_su_state(self, su):
        
        sj = self.su2sj[su]
        
        state =  sj.get_state()
        
        #print '[INFO] get_su_state():', state
        
        return bjstate2troystate(state)
    
    def get_su_state_detail(self, su):
        
        return 'None'


def bjstate2troystate(state):
    
    if state == 'Done':
        return State.Done
    elif state == 'Canceled':
        return State.Canceled
    elif state == 'Unknown':
        return State.Unknown
    elif state == 'Failed':
        return State.Failed
    elif state == 'New':
        return State.New
    elif state == 'Running':
        return State.Running
        
