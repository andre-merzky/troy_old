
from troy.interface.base  import iBase
from troy.pilot.exception import TroyException, Error
    

########################################################################
#
#
#
class iComputeDataScheduler (iBase) :

    """ ComputeDataScheduler (CDS)
    
        The CDS is a troy-internal object which provides scheduling capabilities
        to Troy.  In particular, it will schedule compute_data units over a set of
        compute_data pilots.  To do that, the scheduler implementation (adaptor) will
        need to pull various information from the backend.
    """

    def __init__ (self, obj, adaptor):
        """ Create a ComputeDataScheduler """
        pass


    def init (self) :
        """ dummy method to make sure the backend can initialize the object.
            This method should *not* be implemented in the adaptor!"""
        pass


    def schedule (self, thing, cdud):
        """ schedule a cdu/cdud on a cdus """
        raise TroyException (Error.NotImplemented, "method not implemented!")

