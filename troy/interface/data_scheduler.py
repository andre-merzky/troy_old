
from troy.interface.base  import iBase
from troy.pilot.exception import TroyException, Error
    

########################################################################
#
#
#
class iDataScheduler (iBase) :
    """ L{DataScheduler} interface """


    ############################################################################
    #
    def __init__ (self, obj, adaptor):
        """ Create a DataScheduler """
        raise TroyException (Error.NotImplemented, "method not implemented!")


    ############################################################################
    #
    def init_ (self) :
        """ dummy method to make sure the backend can initialize the object.
            This method should *not* be implemented in the adaptor!"""
        pass


    ############################################################################
    #
    def schedule (self, dus, dud):
        """ schedule a du on a dus """
        raise TroyException (Error.NotImplemented, "method not implemented!")


# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

