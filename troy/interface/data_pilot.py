
from   troy.interface.base  import iBase
import troy.exception


########################################################################
# 
#
#
class iDataPilot (iBase) :
    """ :class:`troy.DataPilot` interface """


    ############################################################################
    #
    def __init__ (self, obj, adaptor) :
        """ Create a DataPilot """
        raise troy.Exception (troy.Error.NotImplemented, "interface not implemented!")


    ############################################################################
    #
    def init_ (self) :
        """ dummy method to make sure the backend can initialize the object.
            This method should *not* be implemented in the adaptor!"""
        pass


    ############################################################################
    #
    def _push_state (self, obj, key) :
        """ tell the adaptor to push state changes to the backend """
        raise troy.Exception (troy.Error.NotImplemented, "interface not implemented!")


    ############################################################################
    #
    def _pull_state (self, obj, key) :
        """ tell the adaptor to pull state changes from the backend """
        raise troy.Exception (troy.Error.NotImplemented, "interface not implemented!")

    ############################################################################
    #
    def reinitialize (self, dpd) :
        """ Re-Initialize the DataPilot to the (new) DataPilotDescription. """
        raise troy.Exception (troy.Error.NotImplemented, "method not implemented!")


    ############################################################################
    #
    def submit_unit (self, dud) :
        """ Submit a DU to this DataPilot """
        raise troy.Exception (troy.Error.NotImplemented, "method not implemented!")


    ############################################################################
    #
    def list_units (self) :
        """ list managed :class:`troy.DataUnit` instances """
        raise troy.Exception (troy.Error.NotImplemented, "method not implemented!")


    ############################################################################
    #
    def wait (self) :
        """ Wait until DP enters a final state """
        raise troy.Exception (troy.Error.NotImplemented, "method not implemented!")


    ############################################################################
    #
    def cancel (self) :
        """ Cancel DP """
        raise troy.Exception (troy.Error.NotImplemented, "method not implemented!")


# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

