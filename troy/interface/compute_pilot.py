
from   troy.interface.base  import iBase
import troy.exception
    

########################################################################
#
#
#
class iComputePilot (iBase) :
    """ :class:`troy.ComputePilot` interface """


    ############################################################################
    #
    def __init__ (self, obj, adaptor) :
        """ Create a ComputePilot """
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
    def reinitialize (self, cpd) :
        """ Re-Initialize the ComputePilot to the (new) ComputePilotDescription.  """
        raise troy.Exception (troy.Error.NotImplemented, "method not implemented!")


    ############################################################################
    #
    def submit_unit (self, cud) :
        """ Submit a CU to this ComputePilot  """
        raise troy.Exception (troy.Error.NotImplemented, "method not implemented!")


    ############################################################################
    #
    def list_units (self) :
        """ list managed :class:`troy.ComputeUnit` instances """
        raise troy.Exception (troy.Error.NotImplemented, "method not implemented!")


    ############################################################################
    #
    def wait (self) :
        """ Wait until CP enters a final state """
        raise troy.Exception (troy.Error.NotImplemented, "method not implemented!")


    ############################################################################
    #
    def cancel (self) :
        """ Cancel CP.  """
        raise troy.Exception (troy.Error.NotImplemented, "method not implemented!")


# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

