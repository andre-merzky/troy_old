
from base import Base

########################################################################
#
#
#
class ComputeDataScheduler_ (Base) :

    """ ComputeDataScheduler_ (CDS)
    
        The CS is a troy-internal object which provides scheduling capabilities
        to Troy.  In particular, it will schedule compute_data units over a set of
        compute_data pilots.  To do that, the scheduler implementation (adaptor) will
        need to pull various information from the backend.  See adaptor level 
        documentation for more details (TODO: link).
    """

    # Class members
    __slots__ = (
        'id',             # Reference to this    CDS
        'policy',         # scheduler policy
    )


    def __init__ (self, policy=None) :
        """ Create a ComputeDataScheduler -- private, only called by CDUS

            Keyword arguments:
            policy -- scheduling policy to be provided

            The given policy determines what backend (adaptor) should be used
            for scheduling.  'None' leaves the scheduler selection to the Troy
            implementation.

        """

        # init api base
        Base.__init__ (self)

        # prepare instance data
        idata = {
                  'id'     : None,
                  'policy' : policy,
                }
        self.set_idata_ (idata)

        # initialize adaptor class 
        self.engine_.call ('ComputeDataScheduler', 'init_', self)


    def schedule (self, thing, cdud) :
        """

        This is the main method: for a given 'thing', schedule a given
        ComputeDataUnit.  A thing can actually only be a CDUS in this case.
        
        The method returns the CDU, which is at that point bound to (i.e.
        scheduled on) a specific resource.
        
        On Error (no scheduling possible), 'None' is returned.  
        """
        return self.engine_.call ('ComputeDataScheduler', 'schedule', 
                                  self, thing, cdud)


# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

