
import imp

import troy
import troy.interface
from   troy.pilot.exception import TroyException, Error


########################################################################
# 
# This TROY adaptor implements a simple random scheduler, which schedules (as
# the above suggests) CUs on random CUSs, CPSs and CPs.
#


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
        self.registry = {'ComputeScheduler'       : 'scheduler_random' }
        
        # The adaptor_data keeps links between all id's and backend instances.
        # It is also use to maintain any other adaptor level state.
        self.adata = { 'cs' : {} }


    def get_name (self):
        return self.name


    def get_registry (self):
        return self.registry


    def sanity_check (self):
        # what did you expect?
        # if sys.random (1) > 0.5 :
        #     return True
        # else :
        #     return False
        return True
    

    # for each api object, we register our adaptor data.  That way, the adata
    # will be available in all adaptor level calls (each belonging to exactly
    # one api class instance).
    def register_adata (self, api) :

        api.set_idata_ (self.adata, self.get_name ())
        return self.adata


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# Compute API
#

########################################################################
class scheduler_random (troy.interface.iComputeScheduler) :

    def __init__ (self, api, adaptor) :

        self.api     = api 
        self.adaptor = adaptor
        self.idata   = self.api.get_idata_ ()

        # we MUST interpret policy, if present
        if 'policy' in self.idata :
            if self.idata['policy'] != 'Random' :
                raise troy.pilot.TroyException (troy.pilot.Error.NoSuccess,
                      "Cannot provide the requested scheduling policy!")

        # print " === random scheduler initialized"

        # if we got this far, we can now register adaptor level instance data in
        # the api.  
        self.adata = self.adaptor.register_adata (self.api)



    def schedule (self, thing, cud) :

        if isinstance ( thing, troy.pilot.ComputeUnitService ) :

            # print "=========== CUS submit"
            # submit to the first cps (0 was randomly chosen)
            # http://xkcd.com/221/
            cps_list = thing.list_compute_pilot_services () # FIXME: check list size
            cps      = troy.pilot.ComputePilotService    (cps_list[0])
            return cps.submit_compute_unit_              (cud)


        elif isinstance ( thing, troy.pilot.ComputePilotService ) :

            # print "=========== CPS submit"
            # submit to the first cps (0 was randomly chosen)
            # http://xkcd.com/221/
            cp_list = thing.list_pilots       () # FIXME: check list size
            cp      = troy.pilot.ComputePilot (cp_list[0])
            return cp.submit_compute_unit_ (cud)


        elif isinstance ( thing, troy.pilot.ComputePilot ) :

            # print "=========== CP submit -> error"
            raise troy.pilot.TroyException (troy.pilot.Error.NoSuccess,
                  "Cannot run the compute unit!")


        else :
            # print "=========== ??"
            raise troy.pilot.TroyException (troy.pilot.Error.NoSuccess,
                  "schedule() expects a CUS, CPS or CP as scheduling target!")


# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

