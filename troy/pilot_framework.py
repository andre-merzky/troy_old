
from troy.base import Base

########################################################################
#
#  PilotFramework (PF)
#
# FIXME: needs cancel, which will free all resources, and discard all unfinished
# work units.
#
class PilotFramework (Base) :
    """  
    PilotFramework (PF)

    A PF acts as the interface to an underlying pilot job framework -- that
    backend creates and manages pilot instances (L{ComputePilot}, L{DataPilot}),
    and can schedule work unit amongst those pilots (L{ComputeUnit},
    L{DataUnit}).

    Class instances are identified by an url, and can be reconnected to.  A PF
    can be added to a L{Troy} instance, which will then be able to utilize the
    PF's pilots for work unit scheduling and execution.

    Properties::

        - id:
          The returned ID can be used to connect to the PF instance later on,
          for example from within a different application instance.
          type: string (url)
    """

    ############################################################################
    #
    def __init__ (self, url) :
        """ 
        Create a PilotFramework object

        Keyword arguments:
        url: url identifying the backend PF.

        Note that the URL may be incomplete, if a new PF instance is to be
        created -- for example, it may contain only a hint about what pilot
        framework is to be used on what resource.  On inspection, the PF will
        always return a fully qualified URL, which will not change over the
        lifetime of the PF.

        """

        # init api base
        Base.__init__ (self)

        # prepare supported attributes
        self.attributes_register_  ('id', None,  self.Url, self.Scalar, self.ReadOnly)
        self.id = url

        # initialize adaptor class
        self.engine_.call ('PilotFramework', 'init_', self)


    ############################################################################
    #
    def submit_pilot (self, pd) :
        """ 
        Create a Pilot.

        Keyword arguments:
        pd -- PilotDescription

        Return value:
        A L{ComputePilot} or a L{DataPilot} instance, depending on type of pilot
        description.

        If the resource requirements defined in the pd cannot be met by the PF,
        a BadParameter exception is raised.  Not raising this exception is,
        however, not a guarantee that the pilot will in fact be (able to be)
        executed -- in that case, the returned pilot will be moved to Failed
        state.

        On success, the returned pilot is in Pending state (or moved into any
        state downstream from Pending).

        submit_pilot() will honor all attributes set on the PD.  Attributes
        which are not explicitly set are interpreted as having default values
        (see documentation of L{ComputePilotDescription} and
        L{DataPilotDescription}), or, where default values are not specified,
        are ignored.

        Note: compared to the Pilot API, this PF combines the functionality of
        the UnitServices and the PilotServices.  Any backend level decomposition
        is considered a PF implementation detail, and, if needed, used only on
        adaptor level.
        """ 
        return self.engine_.call ('PilotFramework', 'submit_pilot', self, pd)


    ############################################################################
    #
    def list_pilots (self) :
        """ 
        List managed pilots.

        Return value:
        A list of L{ComputePilot} and L{DataPilot} IDs.

        The returned list can include pilots which have not been created by this
        PF instance.  The list may be incomplete, and may not include pilots
        created by the PF.  There is no guarantee that pilots in the returned
        list can in fact be reconnected to.  Also, an inclusion in the list does
        not have any indication about the respective pilot's state.
        """
        return self.engine_.call ('PilotFramework', 'list_pilots', self)



    ############################################################################
    #
    def submit_unit (self, ud) :
        """ 
        Submit a work unit to this PilotFramework.

        Keyword argument:
        ud -- L{ComputeUnitDescription} or L{DataUnitDescription} to be enacted.

        Return:
        L{ComputeUnit} or L{DataUnit} instance, depending on type of
        description.

        The UD is passed on to the PF backend, which will attempt to instantiate
        the described workload on any of its pilots.  If no suitable pilot is
        found, a L{Error.BadParameter} exception is raised.  Not raising this
        exception is not a guarantee that the work unit will in fact be (able to
        be) executed -- in that case, the returned work unit will later be moved
        to Failed state.

        On success, the returned work unit is in Pending state (or moved into
        any state downstream from Pending).

        The call will will honor all attributes set on the UD.  Attributes which
        are not explicitly set are interpreted as having default values (see
        documentation of UD), or, where default values are not specified, are
        ignored.

        """
        return self.engine_.call ('PilotFramework', 'submit_unit', self, ud)


    ############################################################################
    #
    def list_units (self) :
        """ 
        list managed work units.

        Return value:
        A list of L{ComputeUnit} and L{DataUnit} IDs

        The returned list can include units which have not been created by this
        PF instance.  The list may be incomplete, and may not include units
        created by the PF.  There is no guarantee that units in the returned
        list can in fact be reconnected to.  Also, an inclusion in the list does
        not have any indication about the respective unit's state.
        """
        return self.engine_.call ('PilotFramework', 'list_units', self)


    ############################################################################
    #
    def cancel (self) :
        """ 
        Cancel all work units, cancel all pilots, free all resources.  
        
        The call will block until the above has been achieved.  It is not an
        error to call the method twice -- it will then simply return
        immediately.
        """
        return self.engine_.call ('PilotFramework', 'cancel', self)


# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

