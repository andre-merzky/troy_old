
from troy.interface.base  import iBase
from troy.pilot.exception import TroyException, Error
    

########################################################################
#
#
#
class iComputePilot (iBase) :

    """ ComputePilot (PilotJob)
    
        This is the object that is returned by the ComputePilotService when a 
        new ComputePilot is created based on a ComputePilotDescription.

        The ComputePilot object can be used by the application to keep track 
        of ComputePilots that are active.
        
        A ComputePilot has state, can be queried, can be cancelled and be 
        re-initialized.
    """

    def __init__ (self, obj, adaptor):
        """ Create a ComputePilot """
        pass


    def init (self) :
        """ dummy method to make sure the backend can initialize the object.
            This method should *not* be implemented in the adaptor!"""
        pass


    def wait (self):
        """ Wait until CP enters a final state """
        raise TroyException (Error.NotImplemented, "method not implemented!")


    def cancel (self):        
        """ Remove the ComputePilot from the ComputePilot Service.
        """
        raise TroyException (Error.NotImplemented, "method not implemented!")


    def reinitialize (self, cpd):        
        """ Re-Initialize the ComputePilot to the (new) ComputePilotDescription.
        
            Keyword arguments:
            cpd -- A ComputePilotDescription
        """
        raise TroyException (Error.NotImplemented, "method not implemented!")


    def set_callback (self, member, cb):
        """ Set a callback function for a member.

            Keyword arguments:
            member -- The member to set the callback for (state / state_detail / wall_time_left).
            cb     -- The callback object to call.
        """
        raise TroyException (Error.NotImplemented, "method not implemented!")


    def unset_callback (self, member):
        """ Unset a callback function from a member

            Keyword arguments:
            member -- The member to unset the callback for (state / state_detail / wall_tim_left).
        """
        raise TroyException (Error.NotImplemented, "method not implemented!")
    

