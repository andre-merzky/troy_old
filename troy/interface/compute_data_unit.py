
from troy.interface.compute_unit import iComputeUnit
from troy.interface.data_unit    import iDataUnit


########################################################################
#
#
#
class iComputeDataUnit (iComputeUnit, iDataUnit) :
    """ L{ComputeDataUnit} interface """


    ############################################################################
    #
    def __init__ (self, obj, adaptor) :
        """ Create a Compute Data Unit """
        raise TroyException (Error.NotImplemented, "method not implemented!")


    ############################################################################
    #
    def init_ (self) :
        """ dummy method to make sure the backend can initialize the object.
            This method should *not* be implemented in the adaptor!"""
        pass


# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

