
from troy.interface.base  import iBase
from troy.pilot.exception import TroyException, Error
    

########################################################################
#
#  
#
class iComputePilotService (iBase) :
    """  L{ComputePilotService} interface """


    ############################################################################
    #
    def __init__ (self, obj, adaptor) :
        """ Create a ComputePilotService """
        raise TroyException (Error.NotImplemented, "interface not implemented!")


    ############################################################################
    #
    def init_ (self) :
        """ dummy method to make sure the backend can initialize the object.
            This method should *not* be implemented in the adaptor!"""
        pass


    ############################################################################
    #
    def submit_pilot (self, cpd) :
        """ Create a ComputePilot. """
        raise TroyException (Error.NotImplemented, "method not implemented!")


    ############################################################################
    #
    def list_pilots (self) :
        """ list managed L{ComputePilot}s. """
        raise TroyException (Error.NotImplemented, "method not implemented!")


    ############################################################################
    #
    def get_pilot (self, cp_id) :
        """ Reconnect to a ComputePilot. """
        raise TroyException (Error.NotImplemented, "method not implemented!")


    ############################################################################
    #
    def submit_unit (self, cud) :
        """ Submit a CU to this ComputePilotService """
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


# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

