
from base            import Base
from data_unit       import DataUnit

########################################################################
#
# DataUnitService
#
class DataUnitService (Base) :

    """ DataUnitService (DUS)

        The DataUnitService is the application's interface to submit
        DataUnits to the Pilot-Manager in the P* Model.  The PilotManagers are
        represented by L{DataPilotService} instances -- those instances can
        be added to L{DataUnitService} instances, and are then used for
        scheduling L{DataUnit}s.

        The implementation of the DataUnitService is generally within Troy --
        as such, it represents and facilitates the application level scheduling
        capabilities of Troy.  The DUS will use Troy level or application
        provided scheduling algorithms to control the distribution of the
        L{DataUnit}s over the set of participating L{DataPilotService}s
        and their L{DataPilot}s.

        Properties::

          - id:
            The returned ID can be used to connect to the DPs instance later
            on, for example from within a different application instance.
            type: string (url)

        FIXME: we might want to expose scheduler state and statistics as
        properties?  Or expose the scheduler as opaque object which can be
        inspected?

    """

    def __init__ (self, dus_id) :
        """
        Create a DataUnitService object

        Keyword arguments:
        dus_id -- Reconnect to an existing DUS instance.

        Note that the dus_id will in general not be an URL pointing to a remote
        service, but will rather point to an application level entity --
        although there is technically no reason not to implement this class as
        a stateful backend service at some point.
        """

        # init api base
        Base.__init__ (self)

        # FIXME: the scheduler type to be used is hard coded.  IMHO, that should
        # be variable via the API.

        # prepare instance data
        self.attribute_register_  ('id',        cus_id,   self.Url,    self.Scalar, self.ReadOnly)
        self.attribute_register_  ('dps',       [],       self.Url,    self.Vector, self.Writeable)
        self.attribute_register_  ('scheduler', 'Random', self.String, self.Scalar, self.Writeable)

        self.set_idata_ ()

        # initialize adaptor class
        self.engine_.call ('DataUnitService', 'init_', self)

        pass


    def set_scheduler (self, s) :
        """
        Set a scheduler for submitted work units

        The scheduler 's' can either be a string, identifying a backend or
        adaptor level scheduler to be used, or a class instance which derives
        from L{troy.pilot.DataScheduler}.
        """

        return self.engine_.call ('DataUnitService', 'set_scheduler', self, s)


    def submit_data_unit (self, dud) :
        """ Submit a CU to this DataUnitService.

            Keyword argument:
            dud -- The DataUnitDescription from the application

            Return:
            DataUnit object
        """

        idata = self.get_idata_ ()
        du    = idata['scheduler'].schedule (self, dud)
        return du


    def list_data_units (self) :
        """ list managed L{DataUnit}s.

            Return value:
            A list of L{DataUnit} IDs

            The returned list can include units which have not been created by
            this DUS instance.  The list may be incomplete, and may not include
            units created by the DUS.  There is no guarantee that units in the
            returned list can in fact be reconnected to.  Also, an inclusion in
            the list does not have any indication about the respective unit's
            state.

        """
        return self.engine_.call ('DataUnitService', 'list_data_units', self)



    def get_data_unit (self, du_id) :
        """ Reconnect to a DataUnit.

            Keyword arguments:
            du_id   -- L{DataUnit}'s id

            Return value:
            A L{DataUnit} instance

            The call behaves identically to::

              du = troy.pilot.DataUnit (du_id)

        """
        return self.engine_.call ('DataUnitService', 'get_data_unit', self, du_id)



    def add_data_pilot_service (self, dps) :
        # FIXME: dp: id or instance?
        """ Add a DataPilotService to this DUS.

            Keyword arguments:
            dps -- The DataPilotService which this DataUnitService will utilize.
        """
        return self.engine_.call ('DataUnitService', 'add_data_pilot_service', self, dps)


    def list_data_pilots_services (self) :
        """ List all DPS IDs of this DUS """
        return self.engine_.call ('DataUnitService', 'list_data_pilot_services', self)


    def remove_data_pilot_service (self, dps) :
        """ Remove a DataPilotService

            Note that it won't cancel the DataPilotService's Pilots, they will just no
            longer receive new DUs.

            Keyword arguments:
            dps -- The DataPilotService to remove
        """
        return self.engine_.call ('DataUnitService', 'remove_data_pilot_service', self, dp)


# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

