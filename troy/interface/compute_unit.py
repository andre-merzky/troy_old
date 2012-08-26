
from troy.interface.base  import iBase
from troy.exception       import Exception, Error
    

########################################################################
#
#  ComputeUnit (CU)
# 
class iComputeUnit (iBase) :
    """ ComputeUnit """


    ############################################################################
    #
    def __init__ (self, obj, adaptor):
        raise troy.Exception (Error.NotImplemented, "method not implemented!")


    ############################################################################
    #
    def init_ (self) :
        """ dummy method to make sure the backend can initialize the object.
            This method should *not* be implemented in the adaptor!"""
        pass


    ############################################################################
    #
    def wait (self) :
        """ Wait until CU enters a final state """
        raise troy.Exception (Error.NotImplemented, "method not implemented!")


    ############################################################################
    #
    def cancel (self) :
        """ Cancel the CU """
        raise troy.Exception (Error.NotImplemented, "method not implemented!")

    
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

