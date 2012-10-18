import api

class PilotJob(api.PilotJob):
    def __init__(self):
        pass
    
    
    def cancel(self):
        pass
    
    
    def reinitialize(self, pilotjob_description):        
        pass


    def set_callback(self, member, cb):
        pass


    def unset_callback(self, member):
        pass


class PilotJobDescription(api.PilotJobDescription):
    pass