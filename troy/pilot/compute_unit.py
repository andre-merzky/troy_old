
from base import Base
    

########################################################################
#
#  ComputeUnit (CU)
# 
class ComputeUnit (Base) :

    """ ComputeUnit
    
        This is the object that is returned by the ComputeUnitService when a 
        new ComputeUnit is created based on a ComputeUnitDescription.

        The ComputeUnit object can be used by the application to keep track 
        of ComputeUnits that are active.

        A ComputeUnit has state, can be queried and can be cancelled.
    """

    # Class members
    __slots__ = (
        'id',           # Reference 
        'state',        # State
        'state_detail', # Backend specific state of the DataUnit

        'description',  # Description
    )

    def __init__ (self):
        print "cu : init"
        pass

    
    def wait (self):
        """ Wait until CU enters a final state """
        pass


    def cancel (self):
        """ Cancel the CU """
        pass

    
    def set_callback (self, member, cb):
        """ Set a callback function for a member.

            Keyword arguments:
            member -- The member to set the callback for (state / state_detail).
            cb     -- The callback object to call.
        """
        pass

    
    def unset_callback (self, member):
        """ Unset a callback function from a member

            Keyword arguments:
            member -- The member to unset the callback from.
        """
        pass

