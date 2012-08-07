
from base import Base

########################################################################
#
#
#
class ComputeDataScheduler (Base) :

    """
    ComputeDataScheduler (CDS)

    The CS is a troy-internal object which provides scheduling capabilities to
    Troy.  In particular, it will schedule compute_data units over a set of compute_data
    pilots.  To do that, the scheduler implementation (adaptor) will need to
    pull various information from the backend.
    """

    def __init__ (self, policy=None) :
        """
        Create a ComputeDataScheduler -- private, only called by CDUS

        Keyword arguments:
        policy -- scheduling policy to be provided

        The given policy determines what backend (adaptor) should be used for
        scheduling.  'None' leaves the scheduler selection to the
        implementation.
        """

        # init api base
        Base.__init__ (self)

        # prepare supported attributes
        self.attribute_register_  ('id',     None,  self.Url,    self.Scalar, self.ReadOnly)
        self.attribute_register_  ('policy', None,  self.String, self.Scalar, self.ReadOnly)

        # initialize adaptor class
        self.engine_.call ('ComputeDataScheduler', 'init_', self)


    def schedule (self, cdus, cdud) :
        """
        Schedule a compute data unit.

        A compute data unit description is used to instantiate a CDU on the
        resource managed by a specific set of compute and data pilots.  The
        scheduler can operate over all pilot services known to the CDUS, and
        their pilots.

        If the scheduler cannot find suitable resources for the requested CDU,
        a BadParameter exception is raised.  Not raising this exception is not
        a guarantee that the CDU will in fact be (able to be) enacted -- in that
        case, the returned CDU will later be moved to Failed state.

        On success, the returned CDU is in Pending state (or moved into any state
        downstream from Pending).

        schedule() will honor all attributes set on the cdud.  Attributes which
        are not explicitly set are interpreted as having default values (see
        documentation of CDUD), or, where default values are not specified, are
        ignored.
        """
        return self.engine_.call ('ComputeDataScheduler', 'schedule', self, cdus, cdud)


# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

