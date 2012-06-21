
from base import Base

########################################################################
#
#
#
class DataScheduler_ (Base) :

    """ DataScheduler_ (DS)
    
        The DS is a troy-internal object which provides scheduling capabilities
        to Troy.  In particular, it will schedule data units over a set of
        data pilots.  To do that, the scheduler implementation (adaptor) will
        need to pull various information from the backend.
    """

    # Class members
    __slots__ = (
        'id',             # Reference to this DS
        'service_url',    # DataScheduler URL
    )


    def __init__ (self, policy=None):
        """ Create a DataScheduler -- private, only called by DUS

            Keyword arguments:
            policy -- scheduling policy to be provided

            The given policy determines what backend (adaptor) should be used
            for scheduling.  'None' leaves the scheduler selection to the
            implementation.

        """

        # init api base
        Base.__init__ (self)

        # prepare instance data
        idata = {
                  'policy' : policy,
                }
        self.set_idata_ (idata)

        # initialize adaptor class 
        self.engine_.call ('DataScheduler', 'init', self)


    def schedule (self, thing, dud):
        """

        This is the main method: for a given 'thing', schedule a given
        DataUnit.  A thing can be a DUS, DPS or DP.
        
        The method returns the DU, which is at that point bound to (i.e.
        scheduled on) a specific DPS or DP.
        
        On Error (no scheduling possible), 'None' is returned.  
        """
        return self.engine_.call ('DataScheduler', 'schedule', 
                                        self, thing, dud)


# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

