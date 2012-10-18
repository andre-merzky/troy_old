import Queue
import api
import config
import uuid
import scheduler


# A mapping for all pilot job services based on ID and object
pilotjobservices = {}

class PilotJobService(api.PilotJobService):

    def __init__(self):
        self.pjs_id = 'troy.pilotjobservice.' + str(uuid.uuid4())
        
        pilotjobservices[self.pjs_id] = self

        # loaded adaptor implementations
        self.adaptors = {}
        
        # mapping between pilots and adaptors
        self.pj2ad = {}
        self.ad2pj = {}
        
        config.read_config()
        
        self._load_adaptors()
        
        #self.wuq = Queue.Queue()
        
        
        
    def _load_adaptors(self):

        if 'bigjob' in config.adaptors:
            try:
                print '[INFO] Trying to load BigJob adaptor ...'
                from adaptors.bigjob import BigJobAdaptor
                self.adaptors['bigjob'] = BigJobAdaptor 
            except ImportError:
                print '[ERROR] Import failed!'
                exit(-1)
            else:
                print '[INFO] Import OK!'
        
        if 'diane' in config.adaptors:
            try:
                print '[INFO] Trying to load DIANE adaptor ...'
                from adaptors.diane import DianeAdaptor
                self.adaptors['diane'] = DianeAdaptor 

            except ImportError:
                print '[ERROR] Import failed!'
                exit(-1)
            else:
                print '[INFO] Import OK!'
        
        if 'condor' in config.adaptors:
            try:
                print '[INFO] Trying to load Condor adaptor ...'
                from adaptors.condor import CondorAdaptor
                self.adaptors['condor'] = CondorAdaptor 
            except ImportError:
                print '[ERROR] Import failed!'
                exit(-1)
            else:
                print '[INFO] Import OK!'
        
        
        print self.adaptors
        
    def create_pilotjob(self, rm, desc, pj_type=None, context=None):
        print '[INFO] Request to create a new pilot job ...'
        
        if not pj_type:
            print '[ERROR] Please specify pilot job type for now!'
            exit(-1)
        else:
            print 'Type:', pj_type
            
        if pj_type not in self.adaptors:
            print 'adaptor not supported'
            exit(-1)
        
        # Create a new adaptor instance of the requested type
        ad_inst = self.adaptors[pj_type]()
        pj = ad_inst.start_pilotjob(rm, desc, context)
        
        print '[INFO] PilotJob ID:', pj.pj_id
        
        # Map the PJ to this adaptor instance
        self.pj2ad[pj] = ad_inst
        self.ad2pj[ad_inst] = pj
        
        return pj
        
    def cancel(self):
        print 'Cancelling all pilotjobs in this pilotjobservice ...'
        for ad in self.pj2ad.values():
            ad.cancel()
   
    def _bind(self, wu):
        print '[INFO] Work Unit bound to:', self.pjs_id
        
        #self.wuq.put_nowait(wu)
        
        scheduler.schedule(wu, self)

if __name__ == '__main__':
    pjs = PilotJobService()
    
    
