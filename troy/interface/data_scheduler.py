
from troy.interface.base  import iBase
from troy.pilot.exception import TroyException, Error
    

########################################################################
#
#
#
class iDataScheduler (iBase) :

    """ DataScheduler (CS)
    
        The CS is a troy-internal object which provides scheduling capabilities
        to Troy.  In particular, it will schedule data units over a set of
        data pilots.  To do that, the scheduler implementation (adaptor) will
        need to pull various information from the backend.
    """

    def __init__ (self, obj, adaptor):
        """ Create a DataScheduler """
        pass


    def init (self) :
        """ dummy method to make sure the backend can initialize the object.
            This method should *not* be implemented in the adaptor!"""
        pass


    def schedule (self, thing, dud):
        """ schedule a du/dud on a dus/dps/dp """
        raise TroyException (Error.NotImplemented, "method not implemented!")

