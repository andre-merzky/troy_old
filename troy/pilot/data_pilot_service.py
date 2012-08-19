
from base               import Base


########################################################################
#
#  DataPilotFramework (DPS)
#
class DataPilotFramework (Base) :
    """  
    DataPilotFramework (DPS)

    The DataPilotFramework is a DataPilot manager.

    A DPS acts as the interface to an underlying pilot data framework -- it
    creates and manages L{DataPilot} instances within that framework, and can
    scheduler L{DataUnit}s amongst those pilots.

    The class is stateful, and instances are identified by an url, and can be
    reconnected to.  A DPS can be added to a L{DataUnitService}, whose scheduler
    will then be able to utilize the DPS's pilots for L{DataUnit} enaction.

    Properties::

        - id:
          The returned ID can be used to connect to the DPs instance later on,
          for example from within a different application instance.  type:
          string (url) 
    """

    ############################################################################
    #
    def __init__ (self) :
        """ 
        Create a DataPilotFramework object

        Keyword arguments:
        url: url identifying the backend DPS.

        Note that the URL may be incomplete, if a new DPS instance is to be
        created -- for example, it may contain only a hint about what pilot
        framework is to be used on what resource.  On inspection, the DPS will
        always return a fully qualified URL, which will not change over the
        lifetime of the DPS.
        """

        # init api base
        Base.__init__ (self)

        # prepare supported attributes
        self.attributes_register_  ('id', None,  self.Url, self.Scalar, self.ReadOnly)

        # initialize adaptor class
        self.engine_.call ('DataPilotFramework', 'init_', self)


    ############################################################################
    #
    def submit_pilot (self, dpd) :
        """ 
        Create a DataPilot.

        Keyword arguments:
        dpd -- L{DataPilotDescription}

        Return value:
        A L{DataPilot} instance

        If the resource requirements defined in the dpd cannot be met by the
        DPS, a BadParameter exception is raised.  Not raising this exception is,
        however, not a guarantee that the DP will in fact be (able to be)
        executed -- in that case, the returned DP will be moved to Failed state.

        On success, the returned DP is in Pending state (or moved into any state
        downstream from Pending).

        submit_pilot() will honor all attributes set on the DPD.  Attributes
        which are not explicitly set are interpreted as having default values
        (see documentation of L{DataPilotDescription}), or, where default values
        are not specified, are ignored.
        """
        return self.engine_.call ('DataPilotFramework', 'submit_pilot', self, dpd)


    ############################################################################
    #
    def list_pilots (self) :
        """ 
        list managed L{DataPilot}s.

        Return value:
        A list of L{DataPilot} IDs

        The returned list can include pilots which have not been created by this
        DPS instance.  The list may be incomplete, and may not include pilots
        created by the DPS.  There is no guarantee that pilots in the returned
        list can in fact be reconnected to.  Also, an inclusion in the list does
        not have any indication about the respective pilot's state.
        """
        return self.engine_.call ('DataPilotFramework', 'list_pilots', self)


    ############################################################################
    #
    def get_pilot (self, dp_id) :
        """ 
        Reconnect to a DataPilot.

        Keyword arguments:
        dp_id   -- L{DataPilot}'s id

        Return value:
        A L{DataPilot} instance

        The call behaves identically to::

            dp = troy.pilot.DataPilot (dp_id)
        """
        return self.engine_.call ('DataPilotFramework', 'get_pilot', self, dp_id)


    ############################################################################
    #
    def submit_unit (self, dud) :
        """ 
        Submit a DU to this DataPilotFramework.

        Keyword argument:
        dud -- The L{DataUnitDescription} from the application

        Return:
        L{DataUnit} object

        The DUD is (possibly translated and) passed on to the DPS backend, which
        will attempt to instantiate the described workload process on any of its
        data pilots.  If no suitable pilot is found, a L{Error.BadParameter}
        exception is raised.  Not raising this exception is not a guarantee that
        the DU will in fact be (able to be) executed -- in that case, the
        returned DU will later be moved to Failed state.

        On success, the returned DU is in Pending state (or moved into any state
        downstream from Pending).

        The call will will honor all attributes set on the dud.  Attributes
        which are not explicitly set are interpreted as having default values
        (see documentation of DUD), or, where default values are not specified,
        are ignored.
        """
        return self.engine_.call ('DataPilotFramework', 'submit_unit', self, dud)


    ############################################################################
    #
    def list_units (self) :
        """ 
        list managed L{DataUnit}s.

        Return value:
        A list of L{DataUnit} IDs

        The returned list can include units which have not been created by this
        DPS instance.  The list may be incomplete, and may not include units
        created by the DPS.  There is no guarantee that units in the returned
        list can in fact be reconnected to.  Also, an inclusion in the list does
        not have any indication about the respective unit's state.
        """
        return self.engine_.call ('DataPilotFramework', 'list_units', self)


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
        return self.engine_.call ('DataPilotFramework', 'get_unit', self, du_id)


# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

