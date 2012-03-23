
from base import Base
    
########################################################################
#
#
#
class ComputePilot (Base) :

    """ ComputePilot (PilotJob)
    
        This is the object that is returned by the ComputePilotService when a 
        new ComputePilot is created based on a ComputePilotDescription.

        The ComputePilot object can be used by the application to keep track 
        of ComputePilots that are active.
        
        A ComputePilot has state, can be queried, can be cancelled and be 
        re-initialized.
    """

    # Class members
    __slots__ = (
        'id',             # Reference to this CP
        'state',          # State of the ComputePilot
        'state_detail',   # Backend specific state of the ComputePilot

        'description',    # Description of ComputePilot
        'service_url',    # ComputePilotService URL

        'wall_time_left'  # Remaining time allocation
    )


    def __init__ (self, cp_id=None):
        """ Create a ComputePilot

            Keyword arguments:
            cp_id -- restore from cp_id
        """
        pass


    def wait (self):
        """ Wait until CP enters a final state """
        pass


    def cancel (self):        
        """ Remove the ComputePilot from the ComputePilot Service.
        """
        pass


    def reinitialize (self, cpd):        
        """ Re-Initialize the ComputePilot to the (new) ComputePilotDescription.
        
            Keyword arguments:
            cpd -- A ComputePilotDescription
        """
        pass


    def set_callback (self, member, cb):
        """ Set a callback function for a member.

            Keyword arguments:
            member -- The member to set the callback for (state / state_detail / wall_time_left).
            cb     -- The callback object to call.
        """
        pass

    def unset_callback (self, member):
        """ Unset a callback function from a member

            Keyword arguments:
            member -- The member to unset the callback for (state / state_detail / wall_tim_left).
        """
        pass
    

