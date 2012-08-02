
from base                    import Base
from compute_unit_service    import ComputeUnitService
from data_unit_service       import DataUnitService
from compute_data_scheduler  import ComputeDataScheduler


########################################################################
#
# ComputeDataUnitService
#
class ComputeDataUnitService (ComputeUnitService, DataUnitService) :

    """ ComputeDataUnitService.(CDUS)

        The ComputeDataUnitService provides the functionality of both the
        L{ComputeUnitService} and the L{DataUnitService} -- as such, it can
        enact a combination of L{ComputeUnit}s and L{DataUnit}s, i.e. the
        L{ComputeDataUnit}s, on a set of L{ComputePilot}s and L{DataPilot}s.

        The implementation of the ComputeDataUnitService is generally within
        Troy -- as such, it represents and facilitates the application level
        scheduling capabilities of Troy.  The CDUS will use Troy level or
        application provided scheduling algorithms to control the distribution
        of the work nits over the set of participating pilot dervices and their
        pilots.

        Properties::

          - id:
            The returned ID can be used to connect to the CDUS instance later
            on, for example from within a different application instance.
            type: string (url)

        FIXME: we might want to expose scheduler state and statistics as
        properties?  Or expose the scheduler as opaque object which can be
        inspected?

    """

    def __init__ (self, cdus_id=None) :
        """
        Create a ComputeDataUnitService object

        Keyword arguments:
        cdus_id: string identifying the CDUS instance.

        Note that the cdus_id will in general not be an URL pointing to a remote
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
        self.attribute_register_  ('cps',       [],       self.Url,    self.Vector, self.Writeable)
        self.attribute_register_  ('dps',       [],       self.Url,    self.Vector, self.Writeable)
        self.attribute_register_  ('scheduler', 'Random', self.String, self.Scalar, self.Writeable)

        self.set_idata_ ()

        # initialize adaptor class
        self.engine_.call ('ComputeDataUnitService', 'init_', self)

        pass


    def set_scheduler (self, s) :
        """
        Set a scheduler for submitted work units

        The scheduler 's' can either be a string, identifying a backend or
        adaptor level scheduler to be used, or a class instance which derives
        from L{troy.pilot.ComputeDataScheduler}.
        """

        return self.engine_.call ('ComputeDataUnitService', 'set_scheduler', self, s)


    def submit_unit (self, cdud) :
        """ Submit a CDU to this ComputeDataUnitService.

            Keyword argument:
            cdud -- The ComputeDataUnitDescription from the application

            Return:
            ComputeDataUnit object
        """

        idata = self.get_idata_ ()
        cdu   = idata['scheduler'].schedule (self, cdud)
        return cdu


    def list_units (self) :
        """ list managed L{ComputeUnit}s.

            Return value:
            A list of L{ComputeDataUnit} IDs

            The returned list can include units which have not been created by
            this CDUS instance.  The list may be incomplete, and may not include
            units created by the CDUS.  There is no guarantee that units in the
            returned list can in fact be reconnected to.  Also, an inclusion in
            the list does not have any indication about the respective unit's
            state.

        """
        return self.engine_.call ('ComputeDataUnitService', 'list_units', self)



    def get_unit (self, cdu_id) :
        """ Reconnect to a ComputeDataUnit.

            Keyword arguments:
            cdu_id   -- L{ComputeDataUnit}'s id

            Return value:
            A L{ComputeDataUnit} instance

            The call behaves identically to::

              cdu = troy.pilot.ComputeDataUnit (cdu_id)

        """
        return self.engine_.call ('ComputeDataUnitService', 'get_unit', self, cdu_id)


    # The methods for adding/removing pilot services to the CDUS are inherited
    # from the CUS and DUS.


# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

