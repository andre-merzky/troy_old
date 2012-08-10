
from base          import Base


########################################################################
#
#  ComputePilotService (CPS)
#
class ComputePilotService (Base) :
    """  ComputePilotService (CPS)

        The ComputePilotService is a ComputePilot manager.

        A CPS acts as the interface to an underlying pilot job framework -- it
        creates and manages L{ComputePilot} instances within that framework, and
        can scheduler L{ComputeUnit}s amongst those pilots.

        The class is stateful, and instances are identified by an url, and can
        be reconnected to.  A CPS can be added to a L{ComputeUnitService}, whose
        scheduler will then be able to utilize the CPS's pilots for
        L{ComputeUnit} execution.

        Properties::

          - id:
            The returned ID can be used to connect to the CPs instance later
            on, for example from within a different application instance.
            type: string (url)
    """

    ############################################################################
    #
    def __init__ (self, url) :
        """ Create a ComputePilotService object

        Keyword arguments:
        url: url identifying the backend CPS.

        Note that the URL may be incomplete, if a new CPS instance is to be
        created -- for example, it may contain only a hint about what pilot
        framework is to be used on what resource.  On inspection, the CPS will
        always return a fully qualified URL, which will not change over the
        lifetime of the CPS.

        """

        # init api base
        Base.__init__ (self)

        # prepare supported attributes
        self.attributes_register_  ('id', None,  self.Url, self.Scalar, self.ReadOnly)
        self.id = url

        # initialize adaptor class
        self.engine_.call ('ComputePilotService', 'init_', self)


    ############################################################################
    #
    def submit_pilot (self, cpd) :
        """ Create a ComputePilot.

            Keyword arguments:
            cpd -- L{ComputePilotDescription}

            Return value:
            A L{ComputePilot} instance

            If the resource requirements defined in the cpd cannot be met by the
            CPS, a BadParameter exception is raised.  Not raising this exception
            is, however, not a guarantee that the CP will in fact be (able to
            be) executed -- in that case, the returned CP will be moved to
            Failed state.

            On success, the returned CP is in Pending state (or moved into any
            state downstream from Pending).

            create_compute_pilot() will honor all attributes set on the CPD.
            Attributes which are not explicitly set are interpreted as having
            default values (see documentation of L{ComputePilotDescription}),
            or, where default values are not specified, are ignored.

        """
        return self.engine_.call ('ComputePilotService', 'submit_pilot', self, cpd)


    ############################################################################
    #
    def list_pilots (self) :
        """ list managed L{ComputePilot}s.

            Return value:
            A list of L{ComputePilot} IDs

            The returned list can include pilots which have not been created by
            this CPS instance.  The list may be incomplete, and may not include
            pilots created by the CPS.  There is no guarantee that pilots in the
            returned list can in fact be reconnected to.  Also, an inclusion in
            the list does not have any indication about the respective pilot's
            state.

        """
        return self.engine_.call ('ComputePilotService', 'list_pilots', self)


    ############################################################################
    #
    def get_pilot (self, cp_id) :
        """ Reconnect to a ComputePilot.

            Keyword arguments:
            cp_id   -- L{ComputePilot}'s id

            Return value:
            A L{ComputePilot} instance

            The call behaves identically to::

              cp = troy.pilot.ComputePilot (cp_id)

        """
        return self.engine_.call ('ComputePilotService', 'get_pilot', self, cp_id)


    ############################################################################
    #
    def submit_unit (self, cud) :
        """ Submit a CU to this ComputePilotService.

            Keyword argument:
            cud -- The L{ComputeUnitDescription} from the application

            Return:
            L{ComputeUnit} object

            The CUD is (possibly translated and) passed on to the CPS backend,
            which will attempt to instantiate the described workload process on
            any of its compute pilots.  If no suitable pilot is found,
            a L{Error.BadParameter} exception is raised.  Not raising this
            exception is not a guarantee that the CU will in fact be (able to
            be) executed -- in that case, the returned CU will later be moved to
            Failed state.

            On success, the returned CU is in Pending state (or moved into any
            state downstream from Pending).

            The call will will honor all attributes set on the cud.  Attributes which
            are not explicitly set are interpreted as having default values (see
            documentation of CUD), or, where default values are not specified,
            are ignored.

        """
        return self.engine_.call ('ComputePilotService', 'submit_unit', self, cud)


    ############################################################################
    #
    def list_units (self) :
        """ list managed L{ComputeUnit}s.

            Return value:
            A list of L{ComputeUnit} IDs

            The returned list can include units which have not been created by
            this CPS instance.  The list may be incomplete, and may not include
            units created by the CPS.  There is no guarantee that units in the
            returned list can in fact be reconnected to.  Also, an inclusion in
            the list does not have any indication about the respective unit's
            state.

        """
        return self.engine_.call ('ComputePilotService', 'list_units', self)


    ############################################################################
    #
    def get_unit (self, cu_id) :
        """ Reconnect to a ComputeUnit.

            Keyword arguments:
            cu_id   -- L{ComputeUnit}'s id

            Return value:
            A L{ComputeUnit} instance

            The call behaves identically to::

              cu = troy.pilot.ComputeUnit (cu_id)

        """
        return self.engine_.call ('ComputePilotService', 'get_unit', self, cu_id)


# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

