
from troy.interface.base  import iBase
from troy.pilot.exception import TroyException, Error


########################################################################
# 
#
#
class iDataPilot (iBase) :

    """ DataPilot (PilotStore)

        This is the object that is returned by the DataPilotService when a 
        new DataPilot is created based on a DataPilotDescription.

        The DataPilot object can be used by the application to keep track 
        of DataPilots that are active.
        
        A DataPilot has state, can be queried, can be cancelled and 
        re-initialized.
    """

    def __init__ (self, obj, adaptor, dp_id=None) :
        """ Create a DataPilot

            Keyword arguments:
            dp_id -- restore from dp_id
        """
        pass


    ############################################################################
    #
    def submit_data_unit (self, dud) :
        """ Submit a DU to this ComputePilot.
    
            Keyword argument:
            dud -- The DataUnitDescription from the application
    
            Return:
            DataUnit object
        """
        raise TroyException (Error.NotImplemented, "method not implemented!")



    def wait (self) :
        """ Wait until DP enters a final state """
        raise TroyException (Error.NotImplemented, "method not implemented!")


    def cancel (self) :
        """ Cancel DP """
        raise TroyException (Error.NotImplemented, "method not implemented!")


    def reinitialize (self, dpd) :
        """ Re-Initialize the DataPilot to the (new) DataPilotDescription.
        
            Keyword arguments:
            dpd -- A DataPilotDescription
        """
        raise TroyException (Error.NotImplemented, "method not implemented!")


    def set_callback (self, member, cb) :
        """ Set a callback function for a member.

            Keyword arguments:
            member -- The member to set the callback for (state / state_detail / size_left).
            cb     -- The callback object to call.
        """
        raise TroyException (Error.NotImplemented, "method not implemented!")

    def unset_callback (self, member) :
        """ Unset a callback function from a member

            Keyword arguments:
            member -- The member to unset the callback for (state / state_detail / sizeleft).
        """
        raise TroyException (Error.NotImplemented, "method not implemented!")


