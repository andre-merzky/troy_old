
from base import Base

########################################################################
#
#
#
class ComputeScheduler_ (Base) :

    """ ComputeScheduler_ (CS)
    
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


    def __init__ (self, policy=None) :
        """ Create a ComputeScheduler -- private, only called by CUS

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
        self.engine_.call ('ComputeScheduler', 'init_', self)


    def schedule (self, thing, cud) :
        """ Schedule a compute unit.

            A compute unit description is used to instantiate a cu on the
            resource managed by a specific compute pilot.  If 'thing' is a CP,
            the CU is instantiated on its resourced.  If 'thing' is a CUS, the
            CU is instantiated on any pilot currently registered on that CUS.
            
            If the scheduler cannot find suitable resources for the requested
            CU, a BadParameter exception is raised.  Not raising this exception
            is not a guarantee that the CU will in fact be (able to be) executed
            -- in that case, the returned CU will later be moved to Failed state.
            
            On success, the returned CU is in Pending state (or moved into any
            state downstream from Pending).

            schedule() will honor all attributes set on the cud.  Attributes
            which are not explicitly set are interpreted as having default
            values (see documentation of CUD), or, where default values are not
            specified, are ignored.

        """
        return self.engine_.call ('ComputeScheduler', 'schedule', 
                                  self, thing, cud)


# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

