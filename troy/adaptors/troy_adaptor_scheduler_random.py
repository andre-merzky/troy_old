
import imp

import troy
import troy.interface
from   troy.pilot.exception import TroyException, Error


########################################################################
# 
# This TROY adaptor implements a simple random scheduler, which schedules (as
# the above suggests) 
#   
#   DUs  on random DUSs, DPSs and DPs.
#   CUs  on random CUSs, CPSs and CPs.
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

        # if we got this far, we can now register adaptor level instance data in
        # the api.  
        self.adata = self.adaptor.register_adata (self.api)



    def schedule (self, thing, dud) :

        if isinstance ( thing, troy.pilot.DataUnitService ) :

            # print "=========== DUS submit"
            dps_list = thing.list_data_pilot_services () # FIXME: check list size
            dps      = troy.pilot.DataPilotService    (dps_list[0])
            return dps.submit_data_unit_              (dud)


        elif isinstance ( thing, troy.pilot.ComputePilotService ) :

            # print "=========== DPS submit"
            dp_list = thing.list_pilots    () # FIXME: check list size
            dp      = troy.pilot.DataPilot (dp_list[0])
            return dp.submit_compute_unit_ (dud)


        elif isinstance ( thing, troy.pilot.DataPilot ) :

            # print "=========== DP submit -> error"
            raise troy.pilot.TroyException (troy.pilot.Error.NoSuccess,
                  "Cannot run the data unit!")


        else :
            # print "=========== ??"
            raise troy.pilot.TroyException (troy.pilot.Error.NoSuccess,
                  "schedule() expects a DUS, DPS or DP as scheduling target!")


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

        # if we got this far, we can now register adaptor level instance data in
        # the api.  
        self.adata = self.adaptor.register_adata (self.api)



    def schedule (self, thing, cud) :

        if isinstance ( thing, troy.pilot.ComputeUnitService ) :

            # print "=========== CUS submit"
            cps_list = thing.list_compute_pilot_services () # FIXME: check list size
            cps      = troy.pilot.ComputePilotService    (cps_list[0])
            return cps.submit_compute_unit_              (cud)


        elif isinstance ( thing, troy.pilot.ComputePilotService ) :

            # print "=========== CPS submit"
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

        # if we got this far, we can now register adaptor level instance data in
        # the api.  
        self.adata = self.adaptor.register_adata (self.api)



    def schedule (self, thing, dcud) :

        if isinstance ( thing, troy.pilot.ComputeDataUnitService ) :

            # print "=========== DCUS submit"
            # Well, problem here is that we can't break the DCUS into DCPSs --
            # those do not exist in the troy API.  So, we would need to split
            # the dcud into a dud and cud.  That is waaaay to complicated for
            # this simple random scheduler - so we don't...
            raise troy.pilot.TroyException (troy.pilot.Error.NotImplemented,
                  "random scheduler cannot handle DCUs!")

        else :
            # print "=========== ??"
            raise troy.pilot.TroyException (troy.pilot.Error.NoSuccess,
                  "schedule() expects a DCUS as scheduling target!")


# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

