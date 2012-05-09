
from base import Base

########################################################################
#
#
#
class _ComputeDataScheduler (Base) :

    """ _ComputeDataScheduler (CDS)
    
        The CS is a troy-internal object which provides scheduling capabilities
        to Troy.  In particular, it will schedule compute_data units over a set of
        compute_data pilots.  To do that, the scheduler implementation (adaptor) will
        need to pull various information from the backend.
    """

    # Class members
    __slots__ = (
        'id',             # Reference to this CDS
        'service_url',    # ComputeDataScheduler URL
    )


    def __init__ (self, policy=None):
        """ Create a ComputeDataScheduler -- private, only called by CDUS

            Keyword arguments:
            policy -- scheduling policy to be provided
        """

        # init api base
        Base.__init__ (self)

        # prepare instance data
        idata = {
                  'policy' : policy,
                }
        self.set_idata_ (idata)

        # initialize adaptor class 
        self.get_engine_().call ('ComputeDataScheduler', 'init', self)


    def schedule (self, thing, dud):
        """

        This is the main method: for a given 'thing', schedule a given
        ComputeDataUnit.  A thing can be a CDUS.
        
        The method returns the CDU, which is at that point scheduled (bound) to
        a specific resource.
        
        On Error (no scheduling possible), 'None' is returned.  
        """
        return self.get_engine_().call ('ComputeDataScheduler', 'schedule', 
                                        self, thing, dud)


# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

