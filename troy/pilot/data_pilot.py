
from base import Base


########################################################################
# 
#
#
class DataPilot (Base) :

    """ DataPilot (PilotStore)

        This is the object that is returned by the DataPilotService when a 
        new DataPilot is created based on a DataPilotDescription.

        The DataPilot object can be used by the application to keep track 
        of DataPilots that are active.
        
        A DataPilot has state, can be queried, can be cancelled and 
        re-initialized.
    """

    # Class members
    __slots__ = (
        'id',           # Reference to this DP
        'state',        # State of the DataPilot
        'state_detail', # Backend specific state of the DataPilot

        'description',  # Description of DataPilot
        'service_url',  # DataPilotService URL

        'space_left'    # Remaining space allocation
    )


    def __init__ (self, dp_id=None):
        """ Create a DataPilot

            Keyword arguments:
            dp_id -- restore from dp_id
        """
        pass


    def wait (self):
        """ Wait until DP enters a final state """
        pass


    def cancel (self):        
        """ Cancel DP """
        pass


    def reinitialize (self, dpd):        
        """ Re-Initialize the DataPilot to the (new) DataPilotDescription.
        
            Keyword arguments:
            dpd -- A DataPilotDescription
        """
        pass


    def set_callback (self, member, cb):
        """ Set a callback function for a member.

            Keyword arguments:
            member -- The member to set the callback for (state / state_detail / size_left).
            cb     -- The callback object to call.
        """
        pass

    def unset_callback (self, member):
        """ Unset a callback function from a member

            Keyword arguments:
            member -- The member to unset the callback for (state / state_detail / sizeleft).
        """
        pass


