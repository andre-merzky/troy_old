
from   troy.interface.base  import iBase
import troy.exception
    

########################################################################
#
# 
#
class iScheduler (iBase) :
    """  :class:`troy.Scheduler` interface """

    ############################################################################
    #
    def __init__ (self, obj, adaptor) :
        """ Create a Scheduler """
        raise troy.Exception (troy.Error.NotImplemented, "interface not implemented!")


    ############################################################################
    #
    def schedule (self, t, ud) :
        """ Schedule a work unit on Troy """
        raise troy.Exception (troy.Error.NotImplemented, "method not implemented!")



# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

