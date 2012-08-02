
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
        pass



    ############################################################################
    #
    def init_ (self) :
        """ dummy method to make sure the backend can initialize the object.
            This method should *not* be implemented in the adaptor!"""
        pass


    ############################################################################
    #
    def add_pilot (self, dp) :
        """ 
        Add a DataPilot to this DUS.

        Keyword arguments:
        dp -- The DataPilot to which this DataUnitService will connect.
        """
        raise TroyException (Error.NotImplemented, "method not implemented!")


    ############################################################################
    #
    def list_pilots (self) :
        """ List all DPs of DUS """
        raise TroyException (Error.NotImplemented, "method not implemented!")
    

    ############################################################################
    #
    def remove_pilot (self, dp) :
        """ 
        Remove a DataPilot
            
        Keyword arguments:
        dp -- The DataPilot to remove 
        """
        raise TroyException (Error.NotImplemented, "method not implemented!")
    
    

    ############################################################################
    #
    def submit_unit (self, dud) :
        """ 
        Submit a DU to this DataUnitService.

        Keyword argument:
        dud -- The DataUnitDescription from the application

        Return:
        DataUnit object
        """
        raise TroyException (Error.NotImplemented, "method not implemented!")



    ############################################################################
    #
    def list_units (self) :
        """ 
        list managed L{DataUnit}s.

        Return value:
        A list of L{DataUnit} IDs
        """
        raise TroyException (Error.NotImplemented, "method not implemented!")



    ############################################################################
    #
    def get_unit (self, cu_id) :
        """ 
        Reconnect to a DataUnit.

        Keyword arguments:
        cu_id   -- L{DataUnit}'s id

        Return value:
        A L{DataUnit} instance
        """
        raise TroyException (Error.NotImplemented, "method not implemented!")



# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

