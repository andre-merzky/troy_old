
from base import Base

########################################################################
#
#
#
class _ComputeScheduler (Base) :

    """ _ComputeScheduler (CS)
    
        The CS is a troy-internal object which provides scheduling capabilities
        to Troy.  In particular, it will schedule compute units over a set of
        compute pilots.  To do that, the scheduler implementation (adaptor) will
        need to pull various information from the backend.
    """

    # Class members
    __slots__ = (
        'id',             # Reference to this CS
        'service_url',    # ComputeScheduler URL
    )


    def __init__ (self, policy=None):
        """ Create a ComputeScheduler -- private, only called by CUS

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
        self.get_engine_().call ('ComputeScheduler', 'init', self)


    def schedule (self, thing, cud):
        """

        This is the main method: for a given 'thing', schedule a given
        ComputeUnit.  A thing can be a CUS, CPS or CP.
        
        The method returns the CU, which is at that point scheduled (bound) to
        a specific CPS or CP.
        
        On Error (no scheduling possible), 'None' is returned.  
        """
        return self.get_engine_().call ('ComputeScheduler', 'schedule', 
                                        self, thing, cud)


# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

