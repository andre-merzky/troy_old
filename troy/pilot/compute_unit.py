
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

    def __init__ (self, cu_id=None):
        print "cu : init"

        # init api base
        Base.__init__ (self)

        # prepare instance data
        idata = {
                  'id' : cu_id,
                }
        self.set_idata_ ('api', idata)

        # initialize adaptor class 
        self.get_engine_().call ('ComputeUnit', 'init', self)


    
    def wait (self):
        """ Wait until CU enters a final state """
        return self.get_engine_().call ('ComputeUnit', 'wait', self)


    def cancel (self):
        """ Cancel the CU """
        return self.get_engine_().call ('ComputeUnit', 'cancel', self)

    
    def set_callback (self, member, cb):
        """ Set a callback function for a member.

            Keyword arguments:
            member -- The member to set the callback for (state / state_detail).
            cb     -- The callback object to call.
        """
        return self.get_engine_().call ('ComputeUnit', 'set_callback', 
                                        self, member, cb)

    
    def unset_callback (self, member):
        """ Unset a callback function from a member

            Keyword arguments:
            member -- The member to unset the callback from.
        """
        return self.get_engine_().call ('ComputeUnit', 'unset_callback', 
                                        self, member)
        pass

