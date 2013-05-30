
import imp
import random

import troy
import troy.interface
from   troy.adaptors.base import aBase
from   troy.exception     import Exception, Error


########################################################################
# 
# This TROY adaptor implements a simple random scheduler, which schedules 
# (as the above suggests) 
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

        if self.api.id != 'Random' :
            raise troy.Exception (troy.Error.NoSuccess,
                  "Requested scheduler (%s) not implemented by this adaptor (Random)" % self.api.id)

        # we MUST interpret policy, if present
        if 'policy' in self.api._idata :
            if self.api._idata['policy'] != 'Random' :
                raise troy.Exception (troy.Error.NoSuccess,
                      "Cannot provide the requested scheduling policy!")

    def ud_is_compute (self, ud) :
        if 'executable' in ud :
            return True
        return False

    def ud_is_data (self, ud) :
        if 'urls' in ud :
            return True
        return False


    def schedule (self, t, ud) :

        pf_ids = t.list_pilot_frameworks ()
        pilots = []

        # gather all available pilots
        for pf_id in pf_ids :
            print "PILOT_FRAMEWORK"
            print pf_id
            pf    = troy.PilotFramework (pf_id)
            p_ids = pf.list_pilots ()
            print "have pf: %s" % pf

            for p_id in p_ids :
                print "PILOT"
                print p_id
                try :
                    if self.ud_is_compute (ud) :
                        p = troy.ComputePilot (p_id)
                        print p
                        pilots.append (p)
                    elif self.ud_is_data (ud) :
                        pilots.append (troy.DataPilot (p_id))
                    else :
                        # ignore invalid ud's
                        pass
                except Exception as e:
                    # print str(e)
                    # ignore invalid pilot IDs (think race condition)
                    pass


        if len (pilots) == 0 :
            raise troy.Exception (troy.Error.IncorrectState,
                  "Cannot schedule: no pilots available")

        # select a random pilot
        idx = random.randint (0, len  (pilots) - 1)
        p   = pilots[idx]

        # and attempt to submit
        return p.submit_unit (ud)


# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

