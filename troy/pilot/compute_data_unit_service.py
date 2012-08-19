
from base                    import Base
from compute_unit_service    import ComputeUnitService


########################################################################
#
# ComputeDataUnitService
#
class ComputeDataUnitService (Base) :
    """ 
    ComputeDataUnitService.(CDUS)

    The ComputeDataUnitService provides the functionality of both the
    L{ComputeUnitService} and the L{DataUnitService} -- as such, it can enact
    a combination of L{ComputeUnit}s and L{DataUnit}s, i.e. the
    L{ComputeDataUnit}s, on a set of L{ComputePilot}s and L{DataPilot}s.

    The implementation of the ComputeDataUnitService is generally within Troy --
    as such, it represents and facilitates the application level scheduling
    capabilities of Troy.  The CDUS will use Troy level or application provided
    scheduling algorithms to control the distribution of the work units over the
    set of participating pilot dervices and their pilots.

    Properties::

        - id:
          The returned ID can be used to connect to the CDUS instance later
          on, for example from within a different application instance.
          type: string (url)

        - policy:
          name of the scheduling policy of the CDUS' scheduler
          type: string (url)

        - scheduler
          An instance of L{ComputeDataScheduler}, internally used by this CDUS 
          to distribute the CDU workload over the different pilot services and
          pilots.

    FIXME: we might want to expose scheduler state and statistics as properties?
    Or expose the scheduler as opaque object which can be inspected?
    """

    ############################################################################
    #
    def __init__ (self, cdus_id=None) :
        """
        Create a ComputeDataUnitService object

        Keyword arguments:
        cdus_id: string identifying the CDUS instance.

        Note that the cdus_id will in general not be an URL pointing to a remote
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
        self.attributes_register_   ('id',        cus_id,   self.Url,    self.Scalar, self.ReadOnly)
        self.attributes_register_   ('cpf',       [],       self.Url,    self.Vector, self.Writable)
        self.attributes_register_   ('policy',    'Any',    self.String, self.Scalar, self.Writable)
        self.attributes_register_   ('scheduler', None,     self.Any,    self.Scalar, self.Writable)

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
        from L{troy.pilot.ComputeDataScheduler}.

        When this method is called, the CDUS will start to use the respective
        scheduler.  If any previous call to this method selected a different
        scheduler, the old instance will be discarded.  If this method is not
        called at all before submitting L{ComputeDataUnit}s, Troy will pick a
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
            raise MyException ("expect policy string or ComputeDataScheduler instance",
                               MyError.BadParameter)

        # we call the adaptor anyway, in case it wants to do some initialization
        # to sanity checking on the scheduler...
        return self.engine_.call ('ComputeDataUnitService', 'set_scheduler', self, s)


    ############################################################################
    #
    def submit_unit (self, cdud) :
        """ 
        Submit a CDU to this ComputeDataUnitService.

        Keyword argument:
        cdud -- The ComputeDataUnitDescription from the application

        Return:
        ComputeDataUnit object
        """

        cdu   = self.scheduler.schedule (self, cdud)
        return cdu


    ############################################################################
    #
    def list_units (self) :
        """ 
        list managed L{ComputeDataUnit}s.

        Return value:
        A list of L{ComputeDataUnit} IDs

        The returned list can include units which have not been created by this
        CDUS instance.  The list may be incomplete, and may not include units
        created by the CDUS.  There is no guarantee that units in the returned
        list can in fact be reconnected to.  Also, an inclusion in the list does
        not have any indication about the respective unit's state.
        """
        return self.engine_.call ('ComputeDataUnitService', 'list_units', self)



    ############################################################################
    #
    def get_unit (self, cdu_id) :
        """ 
        Reconnect to a ComputeDataUnit.

        Keyword arguments:
        cdu_id   -- L{ComputeDataUnit}'s id

        Return value:
        A L{ComputeDataUnit} instance

        The call behaves identically to::

        cdu = troy.pilot.ComputeDataUnit (cdu_id)
        """
        return self.engine_.call ('ComputeDataUnitService', 'get_unit', self, cdu_id)



    ############################################################################
    #
    def add_pilot_service (self, cpf) :
        """ 
        Add a ComputeDataPilotFramework to this CDUS.

        Keyword arguments:
        cpds -- The ComputeDataPilotFramework which this ComputeDataUnitService will utilize.
        """
        return self.engine_.call ('ComputeDataUnitService', 'add_pilot_service', self, cpf)


    ############################################################################
    #
    def list_pilot_services (self) :
        """ List all CDPS IDs of this CDUS """
        return self.engine_.call ('ComputeDataUnitService', 'list_pilot_services', self)


    ############################################################################
    #
    def remove_pilot_service (self, cpf) :
        """ 
        Remove a ComputeDataPilotFramework

        Note that it won't cancel the ComputeDataPilotFramework's Pilots, they will just no
        longer receive new CDUs.

        Keyword arguments:
        cdps -- The ComputeDataPilotFramework to remove
        """
        return self.engine_.call ('ComputeDataUnitService', 'remove_pilot_service', self, cp)


# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

