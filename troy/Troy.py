
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
class Troy (Base) :
    """
    This class, L{troy.Troy}, is the user (or application) facing component of Troy.
    Its purpose is to manage a set of pilot systems (and their pilot resources), and
    to manage a set of scheduling subprocesses which perform scheduling over the
    pilot resources, as described above.  As such, L{troy.Troy} has three distinct
    sets of methods: to manage pilot resources, to manage scheduling subprocesses,
    and to handle workplans to be scheduled on the pilot resources.

    Properties::

        - id:
          The returned ID can be used to connect to the Service instance later
          on, for example from within a different application instance.  
          type: String (url)

        - pilot_frameworks
          An set of L{PilotFramework} instances, representing the set of
          resources over which Troy can schedule work items.
          type: Any

        - schedulers
          An set of L{iScheduler} interface instances, internally used by this
          Scheduler to distribute the workload over the different pilot
          frameworks.
          type: Any

    FIXME: we might want to expose scheduler state and statistics as properties,
    for inspection and profiling?
    """

    ############################################################################
    #
    def __init__ (self, troy_id=None) :
        """
        Create a Troy object

        Keyword arguments:
        troy_id:    string, identifying the Troy instance.

        The troy_id will in general not be an URL pointing to a remote service,
        but will rather point to an application level entity -- although there
        is technically no reason not to implement this class as a stateful
        backend service at some point.
        """

        # init api base
        Base.__init__ (self)

        # RO attribute 'id'
        self.attributes_register_  ('id', troy_id, self.Url,    
                                    self.Scalar, self.ReadOnly)

        # instance data: set of registered pilot frameworks
        self.attributes_register_  ('pilot_frameworks', [], self.Any, self.Vector,    
                                    self.Writable)

        # instance data: set of registered schedulers
        self.attributes_register_  ('schedulers', [], self.Any, self.Vector,    
                                    self.Writable)

        # find an adaptor and initialize
        self.engine_.call ('Troy', 'init_', self)



    ############################################################################
    #
    def add_scheduler (self, s) :
        """
        Add a scheduler for submitted work units.  
        
        FIXME: Allow registration of callables or Scheduler instances
        FIXME: determine if we should have a default scheduler if this method
        is not called...

        The scheduler 's' can either be a string, identifying a backend or
        adaptor level scheduler to be used, or a class instance which derives
        from L{troy.iScheduler}.  For any later call on
        L{troy.Scheduler.schedule()}, the registered scheduler instances are
        invoked in order of registration.  
        
        """ 
        return self.engine_.call ('Troy', 'add_scheduler', self, s)


    ############################################################################
    #
    def list_schedulers (self) :
        """
        return array of registered scheduler instances

        Note that this call is not returning IDs, as scheduler instances are not
        reconnectable.

        # FIXME: change?
        """
        return self.engine_.call ('Troy', 'list_schedulers', self)


    ############################################################################
    #
    def remove_scheduler (self, s) :
        """
        remove a previously registered scheduler instance
        """
        return self.engine_.call ('Troy', 'remove_scheduler', self, s)



    ############################################################################
    #
    def add_pilot_framework (self, pf) :
        """ 
        Add a PilotFramework to this Troy instance.

        Keyword arguments:
        pf -- The PilotFramework which this Troy instance will utilize.
        """
        return self.engine_.call ('Troy', 'add_pilot_framework', self, pf)


    ############################################################################
    #
    def list_pilot_frameworks (self) :
        """ List all PF IDs of this Troy instance """
        return self.engine_.call ('Troy', 'list_pilot_frameworks', self)


    ############################################################################
    #
    def remove_pilot_framework (self, pf) :
        """ 
        Remove a PilotFramework

        Note that it won't cancel the PilotFramework nor its Pilots -- it will
        just no longer receive new work units from this Troy instance.

        Keyword arguments:
        pf -- The PilotFramework to remove (either id or instance)
        """
        return self.engine_.call ('Troy', 'remove_pilot_framework', self, pf)


    ############################################################################
    #
    def submit_unit (self, ud) :
        """ 
        Schedule a work unit.

        A work unit description work (L{ComputeUnitDescription} or
        L{DataUnitDescription}) is provided, and passed to the registered
        schedulers.  Those can either add constraints to the description, or
        pass it on to one of the registered pilot frameworks, or to one of their
        pilots.
            
        If the scheduler cannot find suitable resources for the requested work
        unit, a BadParameter exception is raised.  Not raising this exception is
        not a guarantee that the work unit will in fact be (able to be) enacted
        -- in that case, the returned work unit will later be moved to Failed
        state.
            
        On success, the returned work unit is in Pending state (or moved into
        any state downstream from Pending).

        schedule() will honor all attributes set on the description.  Attributes
        which are not explicitly set are interpreted as having default values
        (see documentation of unit descriptions), or, where default values are
        not specified, are ignored.
        """
        return self.engine_.call ('Troy', 'submit_unit', self, ud)


    ############################################################################
    #
    def list_units (self) :
        """ 
        list managed work units.

        Return value:
        A list of work unit IDs

        The returned list can include units which have not been created by this
        Troy instance.  The list may be incomplete, and may not include units
        created by Troy.  There is no guarantee that units in the returned list
        can in fact be reconnected to.  Also, an inclusion in the list does not
        have any indication about the respective unit's state.
        """
        return self.engine_.call ('Troy', 'list_units', self)


# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

