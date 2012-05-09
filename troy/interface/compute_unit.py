
from troy.interface.base  import iBase
from troy.pilot.exception import TroyException, Error
    

########################################################################
#
#  ComputeUnit (CU)
# 
class iComputeUnit (iBase) :

    """ ComputeUnit
    
        This is the object that is returned by the ComputeUnitService when a 
        new ComputeUnit is created based on a ComputeUnitDescription.

        The ComputeUnit object can be used by the application to keep track 
        of ComputeUnits that are active.

        A ComputeUnit has state, can be queried and can be cancelled.
    """

    def __init__ (self, obj, adaptor):
        pass

    
    def init (self) :
        """ dummy method to make sure the backend can initialize the object.
            This method should *not* be implemented in the adaptor!"""
        pass


    def wait (self):
        """ Wait until CU enters a final state """
        raise TroyException (Error.NotImplemented, "method not implemented!")


    def cancel (self):
        """ Cancel the CU """
        raise TroyException (Error.NotImplemented, "method not implemented!")

    
    def set_callback (self, member, cb):
        """ Set a callback function for a member.

            Keyword arguments:
            member -- The member to set the callback for (state / state_detail).
            cb     -- The callback object to call.
        """
        raise TroyException (Error.NotImplemented, "method not implemented!")

    
    def unset_callback (self, member):
        """ Unset a callback function from a member

            Keyword arguments:
            member -- The member to unset the callback from.
        """
        raise TroyException (Error.NotImplemented, "method not implemented!")

