
from base              import Base
from compute_scheduler import ComputeScheduler


########################################################################
#
#  ComputeUnitService
#
class ComputeUnitService (Base) :
    """  
    ComputeUnitService (CUS)

    The ComputeUnitService is the application's interface to submit ComputeUnits
    to Pilot-Managers in the P* Model.  The PilotManagers are represented by
    L{ComputePilotFramework} instances -- those instances can be added to
    L{ComputeUnitService} instances, and are then used for scheduling
    L{ComputeUnit}s.

    The implementation of the ComputeUnitService is generally within Troy -- as
    such, it represents and facilitates the application level scheduling
    capabilities of Troy.  The CUS will use Troy level or application provided
    scheduling algorithms to control the distribution of the L{ComputeUnit}s
    over the set of participating L{ComputePilotFramework}s and their
    L{ComputePilot}s.

    Properties::

        - id:
          The returned ID can be used to connect to the CUS instance later
          on, for example from within a different application instance.
          type: string (url)

        - policy:
          name of the scheduling policy of the CUS' scheduler
          type: string (url)

       - scheduler
         An instance of L{ComputeScheduler}, internally used by this CUS to
         distribute the CU workload over the different pilot services and
         pilots.

    FIXME: we might want to expose scheduler state and statistics as properties?
    Or expose the scheduler as opaque object which can be inspected?
    """

    ############################################################################
    #
    def __init__ (self, cus_id=None) :
        """
        Create a ComputeUnitService object

        Keyword arguments:
        cus_id:    string, identifying the CUS instance.

        The cus_id will in general not be an URL pointing to a remote service,
        but will rather point to an application level entity -- although there
        is technically no reason not to implement this class as a stateful
        backend service at some point.

        A default scheduler will be instantiated and initialized -- that
        scheduler can later be replaced by a different one via L{set_scheduler()}.
        """

        # init api base
        Base.__init__ (self)

        # FIXME: the scheduler type to be used is hard coded.  IMHO, that should
        # be variable via the API.

        # prepare supported attributes
        self.attributes_register_  ('id',        cus_id,   self.Url,    self.Scalar, self.ReadOnly)
        self.attributes_register_  ('cpf',       [],       self.Url,    self.Vector, self.Writable)
        self.attributes_register_  ('policy',    'Any',    self.String, self.Scalar, self.Writable)
        self.attributes_register_  ('scheduler', None,     self.Any,    self.Scalar, self.Writable)

        self.attributes_set_setter_ ('policy',    self.set_scheduler)
        self.attributes_set_setter_ ('scheduler', self.set_scheduler)

        # initialize adaptor class
        self.engine_.call ('ComputeUnitService', 'init_', self)

        # we set a default scheduler
        self.set_scheduler (ComputeScheduler (self.policy))



    ############################################################################
    #
    def set_scheduler (self, s) :
        """
        Set a scheduler for submitted work units

        The scheduler 's' can either be a string, identifying a backend or
        adaptor level scheduler to be used, or a class instance which derives
        from L{troy.pilot.ComputeScheduler}.

        When this method is called, the CUS will start to use the respective
        scheduler.  If any previous call to this method selected a different
        scheduler, the old instance will be discarded.  If this method is not
        called at all before submitting L{ComputeUnit}s, Troy will pick a
        default scheduler adaptor.
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
            raise MyException ("expect policy string or ComputeScheduler instance",
                               MyError.BadParameter)

        # we call the adaptor anyway, in case it wants to do some initialization
        # to sanity checking on the scheduler...
        return self.engine_.call ('ComputeUnitService', 'set_scheduler', self, s)


    ############################################################################
    #
    def submit_unit (self, cud) :
        """ 
        Submit a CU to this ComputeUnitService.

        Keyword argument:
        cud -- The ComputeUnitDescription from the application

        Return:
        ComputeUnit object
        """

        cu = self.scheduler.schedule (self, cud)
        return cu


    ############################################################################
    #
    def list_units (self) :
        """ 
        list managed L{ComputeUnit}s.

        Return value:
        A list of L{ComputeUnit} IDs

        The returned list can include units which have not been created by this
        CUS instance.  The list may be incomplete, and may not include units
        created by the CUS.  There is no guarantee that units in the returned
        list can in fact be reconnected to.  Also, an inclusion in the list does
        not have any indication about the respective unit's state.
        """
        return self.engine_.call ('ComputeUnitService', 'list_units', self)



    ############################################################################
    #
    def get_unit (self, cu_id) :
        """ 
        Reconnect to a ComputeUnit.

        Keyword arguments:
        cu_id   -- L{ComputeUnit}'s id

        Return value:
        A L{ComputeUnit} instance

        The call behaves identically to::

            cu = troy.pilot.ComputeUnit (cu_id)
        """
        return self.engine_.call ('ComputeUnitService', 'get_unit', self, cu_id)



    ############################################################################
    #
    def add_pilot_service (self, cpf) :
        """ 
        Add a ComputePilotFramework to this CUS.

        Keyword arguments:
        cpf -- The ComputePilotFramework which this ComputeUnitService will utilize.
        """
        return self.engine_.call ('ComputeUnitService', 'add_pilot_service', self, cpf)


    ############################################################################
    #
    def list_pilot_services (self) :
        """ List all CPF IDs of this CUS """
        return self.engine_.call ('ComputeUnitService', 'list_pilot_services', self)


    ############################################################################
    #
    def remove_pilot_service (self, cpf) :
        """ 
        Remove a ComputePilotFramework

        Note that it won't cancel the ComputePilotFramework's Pilots, they will just no
        longer receive new CUs.

        Keyword arguments:
        cdps -- The ComputeDataPilotFramework to remove
        """
        return self.engine_.call ('ComputeUnitService', 'remove_pilot_service', self, cp)


# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

