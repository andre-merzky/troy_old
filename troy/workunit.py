import api
import uuid
import scheduler

class WorkUnit(api.WorkUnit):

    def __init__(self):
        self.wu_id = 'troy.workunit.' + str(uuid.uuid4())
        self.state = api.State.New
        print 'creating new WorkUnit:', self.wu_id
        
    
    def add_callback(self, member, callback):
        pass
    
    def get_state(self):
        return scheduler.get_wu_state(self)
    
    def get_state_detail(self):
        return scheduler.get_wu_state_detail(self)

class WorkUnitDescription(api.WorkUnitDescription):
    pass
