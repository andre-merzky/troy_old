
import imp
import random

import troy
import troy.interface
from   troy.pilot.exception import TroyException, Error


########################################################################
# 
# This TROY adaptor implements a simple random scheduler, which schedules (as
# the above suggests) 
#   
#   DUs  on random DUSs, and DPs.
#   CUs  on random CUSs, and CPs.
#   DCUs on ??? (see below)
#
# Note: http://xkcd.com/221/


########################################################################
#
# main adaptor class, registers the implementation with troy upon loading
#
class adaptor (troy.interface.aBase) :
    
    def __init__ (self) :
        
        # duh!
        self.name     = 'troy_adaptor_scheduler_random'

        # The registry maps api interface classes to the adaptor classes 
        # implementing them:
        self.registry = { 
                'DataScheduler'        : 'scheduler_data_random' ,
                'ComputeScheduler'     : 'scheduler_compute_random' ,
                'ComputeDataScheduler' : 'scheduler_compute_data_random' ,
                }
        
        # The adaptor_data keeps links between all id's and backend instances.
        # It is also use to maintain any other adaptor level state.
        self.adata = { 'cs' : {} }


    def get_name (self) :
        return self.name

    def get_registry (self) :
        return self.registry

    def get_order (self) :
        return 4

    def sanity_check (self) :
        # what did you expect?
        # if sys.random (1) > 0.5 :
        #     return True
        # else :
        #     return False
        pass
    

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# Data Scheduler
#

########################################################################
class scheduler_data_random (troy.interface.iDataScheduler) :

    def __init__ (self, api, adaptor) :

        self.api     = api 
        self.adaptor = adaptor
        self.idata   = self.api.get_idata_ ()

        # we MUST interpret policy, if present
        if 'policy' in self.idata :
            if self.idata['policy'] != 'Random' :
                raise troy.pilot.TroyException (troy.pilot.Error.NoSuccess,
                      "Cannot provide the requested scheduling policy!")



    def schedule (self, dus, dud) :

        # print "=========== DUS submit"
        dp_list = dus.list_data_pilots ()  # FIXME: check list size
        dp      = troy.pilot.DataPilot (dp_list[0])
        return dp.submit_data_unit_    (dud)


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# Compute Scheduler
#

########################################################################
class scheduler_compute_random (troy.interface.iComputeScheduler) :

    def __init__ (self, api, adaptor) :

        self.api     = api 
        self.adaptor = adaptor
        self.idata   = self.api.get_idata_ ()

        # we MUST interpret policy, if present
        if 'policy' in self.idata :
            if self.idata['policy'] != 'Random' :
                raise troy.pilot.TroyException (troy.pilot.Error.NoSuccess,
                      "Cannot provide the requested scheduling policy!")


    def schedule (self, cus, cud) :

        # print "=========== CUS submit"
        pilots = cus.list_compute_pilots ()

        if len (pilots) == 0 :
            raise troy.pilot.TroyException (troy.pilot.Error.IncorrectState,
                  "Cannot schedule: no pilots available")

        idx = random.randint (0, len  (pilots) - 1)
        cp  = troy.pilot.ComputePilot (pilots[idx])

        return cp.submit_compute_unit (cud)


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# Data Compute Scheduler
#

########################################################################
class scheduler_compute_data_random (troy.interface.iComputeDataScheduler) :

    def __init__ (self, api, adaptor) :

        self.api     = api 
        self.adaptor = adaptor
        self.idata   = self.api.get_idata_ ()

        # we MUST interpret policy, if present
        if 'policy' in self.idata :
            if self.idata['policy'] != 'Random' :
                raise troy.pilot.TroyException (troy.pilot.Error.NoSuccess,
                      "Cannot provide the requested scheduling policy!")


    def schedule (self, dcus, dcud) :

        # print "=========== DCUS submit"
        # Well, problem here is that we can't break the DCUS into DCPSs --
        # those do not exist in the troy API.  So, we would need to split
        # the dcud into a dud and cud.  That is waaaay to complicated for
        # this simple random scheduler - so we don't...
        raise troy.pilot.TroyException (troy.pilot.Error.NotImplemented,
              "random scheduler cannot handle DCUs!")


# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

