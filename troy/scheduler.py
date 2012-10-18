import random
import uuid


class SchedulingUnit(object):
    """ This class represents the Scheduling Unit from the P* model
        It is the object that is being passed from the TROY engine to
        the adaptor. 
    """
    def __init__(self):
        self.su_id = 'troy.schedunit.' + str(uuid.uuid4())
     
   

def bind(wu, pilotjobservices):
    """ The binding characteristic defines how and at what time the 
        assignment of a WU to a pilot is done.
    """
    print '[INFO] WorkUnit binding to Pilot Job Service randomly ... '
    pjs = random.choice(pilotjobservices.values())
    pjs._bind(wu)
    
    
def schedule(wu, pilotjobservice):
    """ This method takes care of mapping a WU to a SU and then
        scheduling it to an adaptor.
    """
    #ad = random.choice(pilotjobservice.pj2ad
    print '[INFO] Printing pj2ad'
    print pilotjobservice.pj2ad.values()
    
    print '[INFO] Selecting random adaptor ...'
    ad = random.choice(pilotjobservice.pj2ad.values())
    
    su = SchedulingUnit()
    su.description = wu.description
    su.adaptor = ad
    
    wu._schedunit = su
    
    ad.submit_schedunit(su)

def get_wu_state(wu):
    su = wu._schedunit
    return su.adaptor.get_su_state(su)
    
def get_wu_state_detail(wu):
    su = wu._schedunit
    return su.adaptor.get_su_state_detail(su)


