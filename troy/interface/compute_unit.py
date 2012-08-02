
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

    ############################################################################
    #
    def __init__ (self, obj, adaptor):
        raise TroyException (Error.NotImplemented, "method not implemented!")
        pass



    ############################################################################
    #
    def init_ (self) :
        """ dummy method to make sure the backend can initialize the object.
            This method should *not* be implemented in the adaptor!"""
        pass



    ############################################################################
    #
    def wait (self):
        """ Wait until CU enters a final state """
        raise TroyException (Error.NotImplemented, "method not implemented!")



    ############################################################################
    #
    def cancel (self):
        """ Cancel the CU """
        raise TroyException (Error.NotImplemented, "method not implemented!")


    
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

