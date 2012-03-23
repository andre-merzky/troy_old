
from troy.interface.base  import iBase
from troy.pilot.exception import Exception, Error


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

    def __init__ (self, dp_id=None):
        """ Create a DataPilot

            Keyword arguments:
            dp_id -- restore from dp_id
        """
        pass


    def wait (self, obj):
        """ Wait until DP enters a final state """
        raise Exception (Error.NotImplemented, "method not implemented!")


    def cancel (self, obj):        
        """ Cancel DP """
        raise Exception (Error.NotImplemented, "method not implemented!")


    def reinitialize (self, obj, dpd):        
        """ Re-Initialize the DataPilot to the (new) DataPilotDescription.
        
            Keyword arguments:
            dpd -- A DataPilotDescription
        """
        raise Exception (Error.NotImplemented, "method not implemented!")


    def set_callback (self, obj, member, cb):
        """ Set a callback function for a member.

            Keyword arguments:
            member -- The member to set the callback for (state / state_detail / size_left).
            cb     -- The callback object to call.
        """
        raise Exception (Error.NotImplemented, "method not implemented!")

    def unset_callback (self, obj, member):
        """ Unset a callback function from a member

            Keyword arguments:
            member -- The member to unset the callback for (state / state_detail / sizeleft).
        """
        raise Exception (Error.NotImplemented, "method not implemented!")


