
import imp
import urlparse
import traceback
import threading
from   time import sleep

import troy
import troy.interface
from   troy.adaptors.base import aBase
from   troy.exception     import Exception, Error


########################################################################
# 
# This is a skeleton adaptor for pilot framework backends.
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
        self.name     = 'troy_adaptor_skeleton'

        # The registry maps api interface classes to the adaptor classes 
        # implementing them.  Note that we need to add Base, as the registration
        # will no automatically register the base classes (yet).
        self.registry = {'PilotFramework' : 'skeleton_pf' ,

                         'ComputePilot'   : 'skeleton_cp' ,
                         'ComputeUnit'    : 'skeleton_cu' ,

                         'DataPilot'      : 'skeleton_dp' ,
                         'DataUnit'       : 'skeleton_du' ,

                         'Base'           : 'skeleton_pf' ,
                         'Base'           : 'skeleton_cp' ,
                         'Base'           : 'skeleton_cu' , 
                         'Base'           : 'skeleton_dp' ,
                         'Base'           : 'skeleton_du' }
        
        # We assume that this adaptor does not keep state, as all skeleton
        # entities are easily and cheaply reconnectable.  So, no need to keep
        # any adaptor_data around.  Some object state will be cached on API
        # object level however.
        #
        # self.adata = {}


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
        # For the purpose of this skeleton adaptor, we load a dummy backend
        # module.
        try :
            (f, p, d)    = imp.find_module ('backend', ['/some/path/'])
            self.backend = imp.load_module ('backend', f, p, d)

        except Exception as e :
            raise troy.Exception (Error.NoSuccess, 'could not load skeleton adaptor')


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# Pilot Framework
#
########################################################################
class skeleton_pf (troy.interface.iPilotFramework) :


    ############################################################################
    #
    def __init__ (self, api, adaptor) :

        self.api     = api 
        self.adaptor = adaptor
        self.backend = self.adaptor.backend

        raise troy.Exception (troy.Error.NotImplemented, "method not implemented!")


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
        # well, nothing to do in this skeleton adaptor...
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
        raise troy.Exception (troy.Error.NotImplemented, "method not implemented!")


    ############################################################################
    
    def submit_unit (self, ud) :
        raise troy.Exception (troy.Error.NotImplemented, "method not implemented!")


    ############################################################################
    #
    def list_pilots (self) :
        raise troy.Exception (troy.Error.NotImplemented, "method not implemented!")


    ############################################################################
    #
    def list_units (self) :
        raise troy.Exception (troy.Error.NotImplemented, "method not implemented!")


    ############################################################################
    #
    def cancel (self) :
        raise troy.Exception (troy.Error.NotImplemented, "method not implemented!")


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# Compute API
#

########################################################################
class skeleton_cp (troy.interface.iComputePilot) :

    ############################################################################
    #
    def __init__ (self, api, adaptor) :

        self.api      = api 
        self.adaptor  = adaptor
        self.backend  = self.adaptor.backend

        raise troy.Exception (troy.Error.NotImplemented, "method not implemented!")


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

        raise troy.Exception (troy.Error.NotImplemented, "method not implemented!")


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

        raise troy.Exception (troy.Error.NotImplemented, "method not implemented!")


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
class skeleton_cu (troy.interface.iComputeUnit) :

    ############################################################################
    #
    def __init__ (self, api, adaptor) :
        raise troy.Exception (troy.Error.NotImplemented, "method not implemented!")


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

