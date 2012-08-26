
import imp
import random

import troy
import troy.interface
from   troy.adaptors.base import aBase
from   troy.exception     import Exception, Error


########################################################################
# 
# This TROY adaptor implements a simple random scheduler, which schedules (as
# the above suggests) 
#   
# Note: http://xkcd.com/221/


########################################################################
#
# main adaptor class, registers the implementation with troy upon loading
#
class adaptor (aBase) :
    
    def __init__ (self) :
        
        # duh!
        self.name     = 'troy_adaptor_scheduler_random'

        # The registry maps api interface classes to the adaptor classes 
        # implementing them:
        self.registry = { 'Scheduler' : 'scheduler_random' }
        
    def get_name (self) :
        return self.name

    def get_registry (self) :
        return self.registry

    def get_order (self) :
        return 4

    def sanity_check (self) :
        # raise troy.Exception (Error.NoSuccess, "adaptor disabled")
        
        # what did you expect?
        # if sys.random (1) > 0.5 :
        #     return True
        # else :
        #     return False
        pass
    

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# Random Scheduler
#

########################################################################
class scheduler_random (troy.interface.iScheduler) :

    def __init__ (self, api, adaptor) :

        self.api     = api 
        self.adaptor = adaptor

        # we MUST interpret policy, if present
        if 'policy' in self.api.idata_ :
            if self.api.idata_['policy'] != 'Random' :
                raise troy.Exception (troy.Error.NoSuccess,
                      "Cannot provide the requested scheduling policy!")


    def schedule (self, t, ud) :

        pilot_frameworks = t.list_pilot_frameworks ()

        pilots = []

        for id in pilot_frameworks :
            pilot_framework = troy.PilotFramework (id)
            pilots.extend (pilot_framework.list_pilots ())

        if len (pilots) == 0 :
            raise troy.Exception (troy.Error.IncorrectState,
                  "Cannot schedule: no pilots available")

        idx = random.randint (0, len  (pilots) - 1)
        cp  = troy.ComputePilot (pilots[idx])

        return cp.submit_unit (ud)


# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

