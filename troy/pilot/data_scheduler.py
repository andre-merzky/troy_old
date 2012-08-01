
from base import Base

########################################################################
#
#
#
class DataScheduler (Base) :

    """ 
    DataScheduler (DS)
    
    The DS is a troy-internal object which provides scheduling capabilities to
    Troy.  In particular, it will schedule data units over a set of data 
    pilots. To do that, the scheduler implementation (adaptor) will need to 
    pull various information from the backend.  
    """

    def __init__ (self, policy=None):
        """ 
        Create a DataScheduler -- private, only called by DUS

        Keyword arguments:
        policy -- scheduling policy to be provided

        The given policy determines what backend (adaptor) should be used for
        scheduling.  'None' leaves the scheduler selection to the
        implementation.
        """

        # init api base
        Base.__init__ (self)

        # prepare instance data
        self.attribute_register_  ('id',     None,  self.Url,    self.Scalar, self.ReadOnly)
        self.attribute_register_  ('policy', None,  self.String, self.Scalar, self.ReadOnly)

        self.set_idata_ ()

        # initialize adaptor class 
        self.engine_.call ('DataScheduler', 'init', self)


    def schedule (self, dus, dud):
        """ 
        Schedule a data unit.

        A data unit description is used to instantiate a DU on the resource
        managed by a specific data pilot.  The scheduler can operate over all
        pilot services known to the DUS, and their pilots.
        
        If the scheduler cannot find suitable resources for the requested DU,
        a BadParameter exception is raised.  Not raising this exception is not
        a guarantee that the DU will in fact be (able to be) enacted -- in that
        case, the returned DU will later be moved to Failed state.
        
        On success, the returned DU is in Pending state (or moved into any state
        downstream from Pending).

        schedule() will honor all attributes set on the dud.  Attributes which
        are not explicitly set are interpreted as having default values (see
        documentation of DUD), or, where default values are not specified, are
        ignored.
        """
        return self.engine_.call ('DataScheduler', 'schedule', self, dus, dud)


# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

