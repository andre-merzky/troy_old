
import imp
import urlparse
import traceback
import threading
import warnings

from   time import sleep

import pilot

import troy
import troy.interface
from   troy.adaptors.base import aBase
from   troy.exception     import Exception, Error


########################################################################
# 
# This is a bigjob adaptor for pilot framework backends.
# 
########################################################################


########################################################################
#
# main adaptor class, registers the implementation with troy upon loading
#
class adaptor (aBase) :
    

    ########################################################################
    #
    def __init__ (self) :
        
        # duh!
        self.name     = 'troy_adaptor_bigjob'

        # The registry maps api interface classes to the adaptor classes 
        # implementing them.  Note that we need to add Base, as the registration
        # will no automatically register the base classes (yet).
        self.registry = {'PilotFramework' : 'bigjob_pf' ,

                         'ComputePilot'   : 'bigjob_cp' ,
                         'ComputeUnit'    : 'bigjob_cu' ,

                         'DataPilot'      : 'bigjob_dp' ,
                         'DataUnit'       : 'bigjob_du' ,

                         'Base'           : 'bigjob_pf' ,
                         'Base'           : 'bigjob_cp' ,
                         'Base'           : 'bigjob_cu' , 
                         'Base'           : 'bigjob_dp' ,
                         'Base'           : 'bigjob_du' }
        
        self.data = {}


    ############################################################################
    #
    def sanity_check (self) :
        # raise troy.Exception (Error.NoSuccess, "adaptor disabled")
        
        # try lo load your backend python module, check for the version, and
        # moon phase, check if pi is still normal, or whatever.  If it looks
        # like the universe disagrees with you, and this adaptor will not be
        # able to run, raise a 'UniverseMismatch' exception.  Or
        # 'Error.NoSuccess' if you are shy.
        #
        # If you load a module here, you may want to keep it around for usage.
        # Do *not* import the module -- that will screw up not only this adaptor
        # on failure, but in fact all of Troy.
        #
        # To disable this adaptor, obviously throw with a sensible error.
        #
        # For the purpose of this bigjob adaptor, we load a dummy backend
        # module.
        try :
            with warnings.catch_warnings () :
                warnings.simplefilter ("ignore")
                (f, p, d)    = imp.find_module ('pilot')
                self.backend = imp.load_module ('backend', f, p, d)

        except Exception as e :
            print ' ======== could not load bigjob adaptor: ' + str (e)
            raise troy.Exception (Error.NoSuccess, 'could not load bigjob adaptor')



#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# Pilot Framework
#
########################################################################
class bigjob_pf (troy.interface.iPilotFramework) :


    ############################################################################
    #
    def __init__ (self, api, adaptor) :

        self.api     = api 
        self.adaptor = adaptor
        self.backend = self.adaptor.backend

        # we don't do empty ID's, as it is hard to come up with a useful default
        # coordination URL...
        # id = 'bigjob+redis://localhost/'  

        if 'id' in self.api :
            self.id = self.api.id
        else :
            raise troy.Exception (troy.Error.BadParameter, 
                  "need a URL to connect to BigJob")

        if  self.id in self.adaptor.data :
            self.adata = self.adaptor.data[self.id]
            # id exists -- reconnect
            return

        self.adaptor.data[self.id] = {}
        self.adata = self.adaptor.data[self.id]

        # we expect an URL of the form 'bigjob+redis://something.net', where we
        # strip the bigjob part and can hand the remainder down to BJ
        elems = self.id.split ("+", 2)
        if not len(elems) == 2 :
            print elems
            raise troy.Exception (troy.Error.BadParameter, 
                  "need a 'bigjob+something://...' style URL to connect to BigJob")

        if elems[0] != 'bigjob' :
            raise troy.Exception (troy.Error.BadParameter, 
                  "Need a 'bigjob+something://...' style URL to connect to BigJob")

        self.adata['coord']  = elems[1]
        self.adata['cps']    = pilot.PilotComputeService (self.adata['coord'])
        self.adata['dps']    = pilot.PilotDataService    (self.adata['coord'])
        self.adata['pilots'] = {}



    ############################################################################
    #
    # synchronize troy level state changes with the backend
    #
    def push_state (self, obj, key) :
        # nothing to do here
        raise troy.Exception (troy.Error.NotImplemented, "method not implemented!")


    ############################################################################
    #
    # synchronize backend level state changes with troy (on state queries)
    #
    def pull_state (self, obj, key) :
        # this really should be implemented by the adaptor
        raise troy.Exception (troy.Error.NotImplemented, "method not implemented!")


    ############################################################################
    #
    def sync_backend_state (self) :
        # well, nothing to do in this bigjob adaptor...
        raise troy.Exception (troy.Error.NotImplemented, "method not implemented!")

    
    ############################################################################
    #
    # below are the adaptor implementations for the pilot framework methods.  
    #
    def submit_pilot (self, pd) :
        """ Add a ComputePilot to the ComputePilotFramework

            Keyword arguments:
            cpd     -- ComputePilot Description

            Return value:
            A ComputePilot handle
        """

        bj_pd = {}
        for att in pd.list_attributes () :
            bj_pd[att] = pd[att]


        if  isinstance (pd, troy.ComputePilotDescription) :

            bj_pilot = self.adata['cps'].create_pilot (pilot_compute_description=bj_pd)
            my_pilot = bigjob_cp (self.api, self.adaptor, _pilot=bj_pilot)

            self.adata['pilots'][bj_pilot.get_url ()] = my_pilot

            print self.adata['pilots'].keys ()

            return my_pilot # FIXME: this should be a troy pilot instance!


        if  isinstance (pd, troy.DataPilotDescription) :
            raise troy.Exception (troy.Error.NotImplemented, "data pilots not implemented!")

        return




    ############################################################################
    
    def submit_unit (self, ud) :
        raise troy.Exception (troy.Error.NotImplemented, "method not implemented!")


    ############################################################################
    #
    def list_pilots (self) :

        return self.adata['pilots'].keys ()
        


    ############################################################################
    #
    def list_units (self) :
        raise troy.Exception (troy.Error.NotImplemented, "method not implemented!")


    ############################################################################
    #
    def cancel (self) :
        # this does nothing right now
        pass


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# Compute API
#

########################################################################
class bigjob_cp (troy.interface.iComputePilot) :

    ############################################################################
    #
    def __init__ (self, api, adaptor, _pilot=None) :

        self.api      = api 
        self.adaptor  = adaptor
        self.backend  = self.adaptor.backend

        if _pilot :
            self._pilot = _pilot
            self._id    = _pilot.get_url ()

        else :
            self._id    = self.api.id
            self._pilot = pilot.PilotCompute (pilot_url=self._id)


        self.adaptor.data[self._id] = {}
        self.adata = self.adaptor.data[self._id]
        self.adata['cu'] = {}

        print "######################################"
        print self._pilot
        print "######################################"


    ############################################################################
    #
    def push_state (self, obj, key) :
        raise troy.Exception (troy.Error.NotImplemented, "method not implemented!")


    ############################################################################
    #
    def pull_state (self, obj, key) :
        raise troy.Exception (troy.Error.NotImplemented, "method not implemented!")


    ############################################################################
    #
    def sync_backend_state (self) :
        """ 
        sync api level state with backend state.

        This method can potentially be called very often, so it is advisable to
        cache the state for some amount of time.
        """

        raise troy.Exception (troy.Error.NotImplemented, "method not implemented!")


    ############################################################################
    #
    def is_final (self) :
        """ 
        Check if the job reached a final state.  
        We consider Unknown states to be final. 
        """

        raise troy.Exception (troy.Error.NotImplemented, "method not implemented!")


    ############################################################################
    #
    def submit_unit (self, cud) :
        """
        Create a compute unit
        
        Just as a pf uses a pilot description to create a pilot, this pilot
        uses a compute unit description to create a compute unit -- the code
        looks very similar.
        """
        print " ============================================== "

        bj_cud = {}
        for att in cud.list_attributes () :
            bj_cud[att] = cud[att]

        bj_cu = self._pilot.submit_compute_unit (bj_cud)
        my_cu = bigjob_cu (self.api, self.adaptor, _cu=bj_cu)

        self.adata['cu'][bj_cu.get_url ()] = my_cu

        cu = troy.ComputeUnit (bj_cu.get_url ())

        print "-------------------------------- "
        print bj_cu
        print my_cu
        print cu
        print "-------------------------------- "

        return cu


    ############################################################################
    #
    def wait (self) :
        """ Wait until CP enters a final state """

        raise troy.Exception (troy.Error.NotImplemented, "method not implemented!")


    ############################################################################
    #
    def cancel (self) :
        """ 
        Cancel the pilot, and unregister it from the pilot framework
        """
        return self._pilot.cancel ()


    ############################################################################
    #
    def reinitialize (self, cpd) :
        """ 
        This method is not implemented.  It is actually not necessary to add the
        code for the method and to raise an exception -- if the method is not
        available at all, the interface will raise an exception.
        """

        raise troy.Exception (troy.Error.NotImplemented, "method not implemented!")


########################################################################
class bigjob_cu (troy.interface.iComputeUnit) :

    ############################################################################
    #
    def __init__ (self, api, adaptor, _cu=None) :

        self.api      = api 
        self.adaptor  = adaptor
        self.backend  = self.adaptor.backend

        if _cu :
            self._cu = _cu
            self._id = _cu.get_url ()

        else :
            self._id = self.api.id
            self._cu = pilot.ComputeUnit (cu_url=self._id)

        print "######################################"
      # print self._cu
      # print "######################################"



    ############################################################################
    #
    def push_state (self, obj, key) :
        raise troy.Exception (troy.Error.NotImplemented, "method not implemented!")


    ############################################################################
    #
    def _pull_state (self, obj, key) :

        s = self._cu.get_state ()
        print "state:::: %s (%s)" % (s, type(s))
        if   s == "New"     : self._state = troy.State.New
        elif s == "Running" : self._state = troy.State.Running
        elif s == "Done"    : self._state = troy.State.Done
        elif s == "Failed"  : self._state = troy.State.Failed
        else                : self._state = troy.State.Unknown
        print "state:::: %s (%s)" % (self._state, type(self._state))
        self.api._attributes_i_set ('state', self._state)



    ############################################################################
    #
    def wait (self) :
        """ Wait until CU enters a final state """

        raise troy.Exception (troy.Error.NotImplemented, "method not implemented!")


    ############################################################################
    #
    def cancel (self) :
        """ Cancel the CU """
        raise troy.Exception (troy.Error.NotImplemented, "method not implemented!")

    
    ############################################################################
    #
    def set_callback (self, member, cb) :
        """ Set a callback function for a member.

            Keyword arguments:
            member -- The member to set the callback for (state / state_detail).
            cb     -- The callback object to call.
        """

        raise troy.Exception (troy.Error.NotImplemented, "method not implemented!")

    
    ############################################################################
    #
    def unset_callback (self, member) :
        """ Unset a callback function from a member

            Keyword arguments:
            member -- The member to unset the callback from.
        """

        raise troy.Exception (troy.Error.NotImplemented, "method not implemented!")


# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

