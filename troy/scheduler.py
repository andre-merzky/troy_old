
from troy.base import Base

########################################################################
#
# Troy
#
# FIXME: do we need means to unschedule a work unit, to flush the queue, etc?
# Do we need a notion of queues in the first place?  Priorities?  Where to draw
# the line?
#
# FIXME: define inspection
#
class Scheduler (Base) :
    """  
    Scheduler (S)

    The Troy Scheduler class serves two purposes.  First, it is used as API
    class within Troy, and represents an adaptor level scheduler.  Second, it
    acts as a interface to support the implementation of schedulers on
    application, which can be handed to Troy and can be used in the same way as
    adaptor backed scheduler instances.

    The class implements exactly one method: :func:`troy.Scheduler.schedule` (self, t, ud)`,
    which accepts a :class:`troy.Troy` instance and a workload
    description (:class:`troy.ComputeUnitDescription` or
    :class:`troy.DataUnitDescription`).  The Troy instance represents the set of
    resources to be scheduled over, the workload description represents the
    workplan to be scheduled on those resources.

    The :func:`troy.Scheduler.schedule()` method MUST throw
    a :class:`troy.Exception` if scheduling is not possible, i.e. if the
    scheduler either detects contradictory scheduling constraints, or if it
    detects that applying the scheduling constraints on the set of Troy's
    resources results in an empty set.  If the method can schedule the work
    description for execution, i.e. if it hands it off to one of Troy's
    PilotFrameworks or Pilots, the Scheduler MUST return
    a :class:`troy.ComputeUnit` or :class:`troy.DataUnit` instance (depending on
    the description type).  Any other return type MAY result in the work unit
    being scheduled twice.  If the scheduler adds constraints, but can not
    conclusively schedule the unit on a pilot framework or pilot, it MUST return
    None -- not doing so may result in the work unit not being scheduled at all.

    Properties::



        - id:
          The ID can be used to connect to the Scheduler instance later on, for
          example from within a different application instance -- although the
          ability to reconnect is not guaranteed.  
          Type: String (url)

    FIXME: we might want to expose scheduler state and statistics as properties,
    for inspection and profiling?
    """

    ############################################################################
    #
    def __init__ (self, scheduler_id=None) :
        """
        Create a scheduler object

        Keyword arguments:
        scheduler_id:    string, identifying the Scheduler instance.

        The scheduler_id will in general not be an URL pointing to a remote service,
        but will rather point to an application level entity -- although there
        is technically no reason not to implement this class as a stateful
        backend service at some point.  If the ID is present, the Scheduler
        implementation MUST reconnect to that specific scheduler instance -- if
        that is not possible, init MUST fail with a BadParameter exception.
        """

        # init api base
        Base.__init__ (self)

        # RO attribute 'id'
        self.attributes_register_  ('id', scheduler_id, self.Url, self.Scalar, self.ReadOnly)

        # find an adaptor and initialize
        self._engine.call ('Scheduler', 'init_', self)



    ############################################################################
    #
    def schedule (self, t, ud) :
        """ 
        Schedule a work unit.

        A work unit description (:class:`troy.ComputeUnitDescription` or
        :class:`troy.DataUnitDescription`) is provided, and passed to the backend
        scheduler.  That one can either add constraints to the description, or
        pass it on to one of the registered pilot frameworks, or to one of their
        pilots.

        schedule() will raise a troy.exception if the scheduler cannot handle the
        work unit.  It will return a :class:`troy.ComputeUnit` or :class:`troy.DataUnit` instance if
        the scheduler can schedule the unit for execution on a pilot backend.
        It will return None if the scheduler can merely add constraints (if
        that), but not schedule the unit for execution.
            
        On success, the returned work unit is in Pending state (or moved into
        any state downstream from Pending).  The work unit instance will reveal
        on inspection to what pilot (and thus to what pilot framework) it was
        bound.

        schedule() will honor all attributes set on the description.  Attributes
        which are not explicitly set are interpreted as having default values
        (see documentation of unit descriptions), or, where default values are
        not specified, are ignored.
        """
        return self._engine.call ('Scheduler', 'schedule', self, t, ud)


# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

