
from troy.interface.base  import iBase
from troy.pilot.exception import TroyException, Error
    

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
        raise TroyException (Error.NotImplemented, "interface not implemented!")
        pass



    ############################################################################
    #
    def init_ (self) :
        """ dummy method to make sure the backend can initialize the object.
            This method should *not* be implemented in the adaptor!"""
        pass



    ############################################################################
    #
    def reinitialize (self, cpd) :
        """ 
        Re-Initialize the ComputePilot to the (new) ComputePilotDescription.

        Keyword arguments:
        cpd -- A ComputePilotDescription
        """
        raise TroyException (Error.NotImplemented, "method not implemented!")



    ############################################################################
    #
    def submit_unit (self, cud) :
        """ 
        Submit a CU to this ComputePilot.
    
        Keyword argument:
        cud -- The L{ComputeUnitDescription} from the application
    
        Return:
        L{ComputeUnit} object
        """
        raise TroyException (Error.NotImplemented, "method not implemented!")



    ############################################################################
    #
    def list_units (self) :
        """ 
        list managed L{ComputeUnit}s.

        Return value:
        A list of L{ComputeUnit} IDs
        """
        raise TroyException (Error.NotImplemented, "method not implemented!")



    ############################################################################
    #
    def get_unit (self, cu_id) :
        """ 
        Reconnect to a ComputeUnit.

        Keyword arguments:
        cu_id   -- L{ComputeUnit}'s id

        Return value:
        A L{ComputeUnit} instance
        """
        raise TroyException (Error.NotImplemented, "method not implemented!")



    ############################################################################
    #
    def wait (self) :
        """ Wait until CP enters a final state """
        raise TroyException (Error.NotImplemented, "method not implemented!")



    ############################################################################
    #
    def cancel (self) :
        """ Cancel CP.  """
        raise TroyException (Error.NotImplemented, "method not implemented!")



# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

