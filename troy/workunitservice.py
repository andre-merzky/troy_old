import api
from workunit import WorkUnit
import uuid
from pilotjobservice import pilotjobservices
import scheduler

class WorkUnitService(api.WorkUnitService):

    def __init__(self, wus_id=None):
        if wus_id:
            print '[ERROR] Reconnecting to existing Work Unit Service not yet implemented'
            exit(-1)

        self.wus_id = 'troy.workunitservice.' + str(uuid.uuid4())
 
        self.pilotjobservices = {}
    
    def add(self, pjs):
        
        try:
            pjs_obj = pilotjobservices[pjs.pjs_id]
        except:
            print '[ERROR] Could not find pilob job service to add to.'
        
        self.pilotjobservices[pjs.pjs_id] = pjs_obj
        
    
    def remove(self, pjs):
        pass
    

    def submit(self, wud):
        wu = WorkUnit()
        
        wu.description = wud
        scheduler.bind(wu, self.pilotjobservices)
        
        return wu
    
  
        
    def cancel(self):
        pass
    