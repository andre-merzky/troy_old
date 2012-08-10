
from compute_unit_service import iComputeUnitService
from data_unit_service    import iDataUnitService


########################################################################
#
#
#
class iComputeDataUnitService (iComputeUnitService, iDataUnitService) :
    """ L{ComputeDataUnitService} interface """


    ############################################################################
    #
    def __init__ (self, obj, adaptor) :
        """ Create a ComputeDataUnitService """
        raise TroyException (Error.NotImplemented, "interface not implemented!")


    ############################################################################
    #
    def init_ (self) :
        """ dummy method to make sure the backend can initialize the object.
            This method should *not* be implemented in the adaptor!"""
        pass


# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

