
from troy.interface.base  import iBase
from troy.pilot.exception import TroyException, Error
    

########################################################################
#
#
#
class iComputeDataScheduler (iBase) :
    """ L{ComputeDataScheduler} interface """


    ############################################################################
    #
    def __init__ (self, obj, adaptor):
        """ Create a ComputeDataScheduler """
        pass



    ############################################################################
    #
    def init (self) :
        """ dummy method to make sure the backend can initialize the object.
            This method should *not* be implemented in the adaptor!"""
        pass



    ############################################################################
    #
    def schedule (self, cdus, cdud):
        """ schedule a cdu on a cdus """
        raise TroyException (Error.NotImplemented, "method not implemented!")


# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

