
from troy.interface.base  import iBase
from troy.exception       import Exception, Error
    

########################################################################
#
#
#
class iComputePilot (iBase) :
    """ L{ComputePilot} interface """


    ############################################################################
    #
    def __init__ (self, obj, adaptor) :
        """ Create a ComputePilot """
        raise troy.Exception (Error.NotImplemented, "interface not implemented!")


    ############################################################################
    #
    def init_ (self) :
        """ dummy method to make sure the backend can initialize the object.
            This method should *not* be implemented in the adaptor!"""
        pass


    ############################################################################
    #
    def reinitialize (self, cpd) :
        """ Re-Initialize the ComputePilot to the (new) ComputePilotDescription.  """
        raise troy.Exception (Error.NotImplemented, "method not implemented!")


    ############################################################################
    #
    def submit_unit (self, cud) :
        """ Submit a CU to this ComputePilot  """
        raise troy.Exception (Error.NotImplemented, "method not implemented!")


    ############################################################################
    #
    def list_units (self) :
        """ list managed L{ComputeUnit}s """
        raise troy.Exception (Error.NotImplemented, "method not implemented!")


    ############################################################################
    #
    def wait (self) :
        """ Wait until CP enters a final state """
        raise troy.Exception (Error.NotImplemented, "method not implemented!")


    ############################################################################
    #
    def cancel (self) :
        """ Cancel CP.  """
        raise troy.Exception (Error.NotImplemented, "method not implemented!")


# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

