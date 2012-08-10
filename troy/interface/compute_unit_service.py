
from troy.interface.base  import iBase
from troy.pilot.exception import TroyException, Error
    

########################################################################
#
# 
#
class iComputeUnitService (iBase) :
    """  L{ComputeUnitService} interface """


    ############################################################################
    #
    def __init__ (self, obj, adaptor) :
        """ Create a ComputeUnitService """
        raise TroyException (Error.NotImplemented, "interface not implemented!")


    ############################################################################
    #
    def init_ (self) :
        """ dummy method to make sure the backend can initialize the object.
            This method should *not* be implemented in the adaptor!"""
        pass


    ############################################################################
    #
    def set_scheduler (self, s) :
        """ Set a scheduler for submitted work units """
        raise TroyException (Error.NotImplemented, "method not implemented!")


    ############################################################################
    #
    def submit_unit (self, cud) :
        """ Submit a CU to this ComputeUnitService """
        raise TroyException (Error.NotImplemented, "method not implemented!")


    ############################################################################
    #
    def list_units (self) :
        """ list managed L{ComputeUnit}s """
        raise TroyException (Error.NotImplemented, "method not implemented!")


    ############################################################################
    #
    def get_unit (self, cu_id) :
        """ Reconnect to a ComputeUnit """
        raise TroyException (Error.NotImplemented, "method not implemented!")
    
    
    ############################################################################
    #
    def add_pilot_service (self, cps) :
        """ Add a ComputePilotService to this CUS """
        raise TroyException (Error.NotImplemented, "method not implemented!")


    ############################################################################
    #
    def list_pilot_services (self) :
        """ List all CPSs of CUS """
        raise TroyException (Error.NotImplemented, "method not implemented!")


    ############################################################################
    #
    def remove_pilot_service (self, cps) :
        """ Remove a ComputePilotService """
        raise TroyException (Error.NotImplemented, "method not implemented!")


# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

