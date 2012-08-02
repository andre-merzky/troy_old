
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
        pass



    ############################################################################
    #
    def init_ (self) :
        """ dummy method to make sure the backend can initialize the object.
            This method should *not* be implemented in the adaptor!"""
        pass


    ############################################################################
    #
    def add_pilot (self, cp) :
        """ 
        Add a ComputePilot to this CUS.

        Keyword arguments:
        cp -- The ComputePilot to which this ComputeUnitService will connect.
        """
        raise TroyException (Error.NotImplemented, "method not implemented!")


    ############################################################################
    #
    def list_pilots (self) :
        """ List all CPs of CUS """
        raise TroyException (Error.NotImplemented, "method not implemented!")


    ############################################################################
    #
    def remove_pilot (self, cp) :
        """ 
        Remove a ComputePilot

        Keyword arguments:
        cp -- The ComputePilot to remove 
        """
        raise TroyException (Error.NotImplemented, "method not implemented!")



    ############################################################################
    #
    def submit_unit (self, cud) :
        """ 
        Submit a CU to this ComputeUnitService.
    
        Keyword argument:
        cud -- The ComputeUnitDescription from the application
    
        Return:
        ComputeUnit object
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



# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

