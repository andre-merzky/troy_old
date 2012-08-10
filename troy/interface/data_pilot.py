
from troy.interface.base  import iBase
from troy.pilot.exception import TroyException, Error


########################################################################
# 
#
#
class iDataPilot (iBase) :
    """ L{DataPilot} interface """


    ############################################################################
    #
    def __init__ (self, obj, adaptor) :
        """ Create a DataPilot """
        raise TroyException (Error.NotImplemented, "interface not implemented!")


    ############################################################################
    #
    def init_ (self) :
        """ dummy method to make sure the backend can initialize the object.
            This method should *not* be implemented in the adaptor!"""
        pass


    ############################################################################
    #
    def reinitialize (self, dpd) :
        """ Re-Initialize the DataPilot to the (new) DataPilotDescription. """
        raise TroyException (Error.NotImplemented, "method not implemented!")


    ############################################################################
    #
    def submit_unit (self, dud) :
        """ Submit a DU to this ComputePilot """
        raise TroyException (Error.NotImplemented, "method not implemented!")


    ############################################################################
    #
    def list_units (self) :
        """ list managed L{DataUnit}s """
        raise TroyException (Error.NotImplemented, "method not implemented!")


    ############################################################################
    #
    def get_unit (self, du_id) :
        """ Reconnect to a DataUnit """
        raise TroyException (Error.NotImplemented, "method not implemented!")


    ############################################################################
    #
    def wait (self) :
        """ Wait until DP enters a final state """
        raise TroyException (Error.NotImplemented, "method not implemented!")


    ############################################################################
    #
    def cancel (self) :
        """ Cancel DP """
        raise TroyException (Error.NotImplemented, "method not implemented!")


# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

