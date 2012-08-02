
from troy.interface.base  import iBase
from troy.pilot.exception import TroyException, Error
    

########################################################################
#
#
#
class iComputeScheduler (iBase) :
    """ L{ComputeScheduler} interface """


    ############################################################################
    #
    def __init__ (self, obj, adaptor) :
        """ Create a ComputeScheduler """
        pass



    ############################################################################
    #
    def init_ (self) :
        """ dummy method to make sure the backend can initialize the object.
            This method should *not* be implemented in the adaptor!"""
        pass



    ############################################################################
    #
    def schedule (self, cus, cud) :
        """ schedule a cu on a cus """
        raise TroyException (Error.NotImplemented, "method not implemented!")


# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

