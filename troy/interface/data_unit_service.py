
from troy.interface.base  import iBase
from troy.pilot.exception import TroyException, Error


########################################################################
#
# 
class iDataUnitService (iBase) :
    """ L{DataUnitService} interface"""

    ############################################################################
    #
    def __init__ (self, obj, adaptor) :
        """ Create a DataUnitService """
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
    def submit_unit (self, dud) :
        """ Submit a DU to this DataUnitService """
        raise TroyException (Error.NotImplemented, "method not implemented!")


    ############################################################################
    #
    def list_units (self) :
        """ list managed L{DataUnit}s """
        raise TroyException (Error.NotImplemented, "method not implemented!")


    ############################################################################
    #
    def get_unit (self, du_id) :
        """ Reconnect to a L{DataUnit} """
        raise TroyException (Error.NotImplemented, "method not implemented!")


    ############################################################################
    #
    def add_pilot_service (self, dps) :
        """ Add a DataPilotFramework to this DUS """
        raise TroyException (Error.NotImplemented, "method not implemented!")


    ############################################################################
    #
    def list_pilot_services (self) :
        """ List all DPS IDs of this DUS """
        raise TroyException (Error.NotImplemented, "method not implemented!")
    

    ############################################################################
    #
    def remove_pilot_service (self, dps) :
        """ Remove a DataPilotFramework """
        raise TroyException (Error.NotImplemented, "method not implemented!")
    

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

