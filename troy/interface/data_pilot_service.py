
from troy.interface.base  import iBase
from troy.pilot.exception import TroyException, Error


########################################################################
#
#
#
class iDataPilotFramework (iBase) :
    """  L{DataPilotFramework} interface """

    ############################################################################
    #
    def __init__ (self, obj, adaptor) :
        """ Create a DataPilotFramework """
        raise TroyException (Error.NotImplemented, "interface not implemented!")


    ############################################################################
    #
    def init_ (self) :
        """ dummy method to make sure the backend can initialize the object.
            This method should *not* be implemented in the adaptor!"""
        pass


    ############################################################################
    #
    def submit_pilot (self, dpd) :
        """ Create a DataPilot """  
        raise TroyException (Error.NotImplemented, "method not implemented!")


    ############################################################################
    #
    def list_pilots (self) :
        """ list managed L{DataPilot}s """
        raise TroyException (Error.NotImplemented, "method not implemented!")


    ############################################################################
    #
    def get_pilot (self, dp_id) :
        """ Reconnect to a DataPilot """
        raise TroyException (Error.NotImplemented, "method not implemented!")


    ############################################################################
    #
    def submit_unit (self, dud) :
        """ Submit a CU to this DataPilotFramework """
        raise TroyException (Error.NotImplemented, "method not implemented!")


    ############################################################################
    #
    def list_units (self) :
        """ list managed L{DataUnit}s """
        raise TroyException (Error.NotImplemented, "method not implemented!")


    ############################################################################
    #
    def get_unit (self, cu_id) :
        """ Reconnect to a DataUnit """
        raise TroyException (Error.NotImplemented, "method not implemented!")


# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

