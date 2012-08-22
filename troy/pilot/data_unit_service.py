
from base            import Base


########################################################################
#
# DataUnitService
#
class DataUnitService (Base) :
    """ 
    DataUnitService (DUS)

    The DataUnitService is the application's interface to submit DataUnits to
    the Pilot-Manager in the P* Model.  The PilotManagers are represented by
    L{DataPilotFramework} instances -- those instances can be added to
    L{DataUnitService} instances, and are then used for scheduling L{DataUnit}s.

    The implementation of the DataUnitService is generally within Troy -- as
    such, it represents and facilitates the application level scheduling
    capabilities of Troy.  The DUS will use Troy level or application provided
    scheduling algorithms to control the distribution of the L{DataUnit}s over
    the set of participating L{DataPilotFramework}s and their L{DataPilot}s.

    Properties::

        - id:
          The returned ID can be used to connect to the DPs instance later on,
          for example from within a different application instance.  type:
          string (url)

        - policy:
          name of the scheduling policy of the CUS' scheduler
          type: string (url)

       - scheduler
         An instance of L{ComputeScheduler}, internally used by this CUS to
         distribute the CU workload over the different pilot services and
         pilots.

     FIXME: we might want to expose scheduler state and statistics as
     properties?  Or expose the scheduler as opaque object which can be
     inspected?
    """

    ############################################################################
    #
    def __init__ (self, dus_id=None) :
        """
        Create a DataUnitService object

        Keyword arguments:
        dus_id -- Reconnect to an existing DUS instance.

        Note that the dus_id will in general not be an URL pointing to a remote
        service, but will rather point to an application level entity --
        although there is technically no reason not to implement this class as
        a stateful backend service at some point.

        A default scheduler will be instantiated and initialized -- that
        scheduler can later be replaced by a different one via L{set_scheduler()}.
        """

        # init api base
        Base.__init__ (self)

        # FIXME: the scheduler type to be used is hard coded.  IMHO, that should
        # be variable via the API.

        # prepare supported attributes
        self.attributes_register_  ('id',        cus_id,   self.Url,    self.Scalar, self.ReadOnly)
        self.attributes_register_  ('dpf',       [],       self.Url,    self.Vector, self.Writable)
        self.attributes_register_  ('policy',    'Any',    self.String, self.Scalar, self.Writable)
        self.attributes_register_  ('scheduler', None,     self.Any,    self.Scalar, self.Writable)

        self.attributes_set_setter_ ('policy',    self.set_scheduler)
        self.attributes_set_setter_ ('scheduler', self.set_scheduler)

        # initialize adaptor class
        self.engine_.call ('DataUnitService', 'init_', self)

        # we set a default scheduler
        self.set_scheduler (ComputeScheduler (self.policy))



    ############################################################################
    #
    def set_scheduler (self, s) :
        """
        Set a scheduler for submitted work units

        The scheduler 's' can either be a string, identifying a backend or
        adaptor level scheduler to be used, or a class instance which derives
        from L{troy.pilot.DataScheduler}.

        When this method is called, the DUS will start to use the respective
        scheduler.  If any previous call to this method selected a different
        scheduler, the old instance will be discarded.  If this method is not
        called at all before submitting L{DataUnit}s, Troy will pick a default 
        scheduler adaptor.
        """

        if isinstance (s, basestring) :
            if s != self.policy :
                self.policy    = s
                self.scheduler = ComputeDataScheduler (self.policy)
        elif isinstance (s, troy.pilot.ComputeDataScheduler) :
            if s != self.scheduler :
                self.scheduler = s
                self.pollicy   = s.policy
        else :
            raise MyException ("expect policy string or DataScheduler instance",
                               MyError.BadParameter)

        # we call the adaptor anyway, in case it wants to do some initialization
        # to sanity checking on the scheduler...
        return self.engine_.call ('DataUnitService', 'set_scheduler', self, s)


    ############################################################################
    #
    def submit_unit (self, dud) :
        """ 
        Submit a CU to this DataUnitService.

        Keyword argument:
        dud -- The DataUnitDescription from the application

        Return:
        DataUnit object
        """

        du    = self.scheduler.schedule (self, dud)
        return du


    ############################################################################
    #
    def list_units (self) :
        """ 
        list managed L{DataUnit}s.

        Return value:
        A list of L{DataUnit} IDs

        The returned list can include units which have not been created by this
        DUS instance.  The list may be incomplete, and may not include units
        created by the DUS.  There is no guarantee that units in the returned
        list can in fact be reconnected to.  Also, an inclusion in the list does
        not have any indication about the respective unit's state.
        """
        return self.engine_.call ('DataUnitService', 'list_units', self)



    ############################################################################
    #
    def get_unit (self, du_id) :
        """ 
        Reconnect to a DataUnit.

        Keyword arguments:
        du_id   -- L{DataUnit}'s id

        Return value:
        A L{DataUnit} instance

        The call behaves identically to::

            du = troy.pilot.DataUnit (du_id)
        """
        return self.engine_.call ('DataUnitService', 'get_unit', self, du_id)



    ############################################################################
    #
    def add_pilot_framework (self, dpf) :
        """ 
        Add a DataPilotFramework to this DUS.

        Keyword arguments:
        dpf -- The DataPilotFramework which this DataUnitService will utilize.
        """
        return self.engine_.call ('DataUnitService', 'add_pilot_framework', self, dpf)


    ############################################################################
    #
    def list_pilot_frameworks (self) :
        """ List all DPF IDs of this DUS """
        return self.engine_.call ('DataUnitService', 'list_pilot_frameworks', self)


    ############################################################################
    #
    def remove_pilot_framework (self, dpf) :
        """ 
        Remove a DataPilotFramework

        Note that it won't cancel the DataPilotFramework's Pilots, they will just
        no longer receive new DUs.

        Keyword arguments:
        dpf -- The DataPilotFramework to remove
        """
        return self.engine_.call ('DataUnitService', 'remove_pilot_framework', self, dp)


# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

