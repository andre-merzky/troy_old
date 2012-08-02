
from troy.interface.base  import iBase
from troy.pilot.exception import TroyException, Error


########################################################################
# 
#
#
class iDataPilot (iBase) :

    """ 
    L{DataPilot} interface
    """

    ############################################################################
    #
    def __init__ (self, obj, adaptor) :
        """ Create a DataPilot """
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
    def reinitialize (self, dpd) :
        """ 
        Re-Initialize the DataPilot to the (new) DataPilotDescription.
        
        Keyword arguments:
        dpd -- A DataPilotDescription
        """
        raise TroyException (Error.NotImplemented, "method not implemented!")



    ############################################################################
    #
    def submit_unit (self, dud) :
        """ 
        Submit a DU to this ComputePilot.
    
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

