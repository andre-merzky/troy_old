
from base            import Base


########################################################################
#
#
#
class DataPilot (Base) :

    """ DataPilot (PilotStore)

        This is the object that is returned by the DataPilotService when a
        new DataPilot is created based on a DataPilotDescription.

        The DataPilot object can be used by the application to keep track
        of DataPilots that are active.

        A DataPilot has state, can be queried, can be cancelled and
        re-initialized.


        Properties::

          - state:
            The state of the pilot.
            type: L{troy.pilot.State} (enum)

          - state_detail:
            The backend state of the pilot.  The value of this property is not
            interpreted by Troy, and is up to the backend pilot framework.
            type: string

          - id:
            The id may be 'None' if the Pilot is not yet in Running state.
            The returned ID can be used to connect to the DP instance later
            on, for example from within a different application instance.
            type: string (url)

          - description:
            The DataPilotDescription used to create this pilot.
            That description is not guaranteed to be available, nor is it
            guaranteed to be complete -- in particular for reconnected pilots.
            Its existence and completeness depends on the ability to inspect
            backend pilot instances.
            type: L{troy.pilot.DataPilotDescription}

          - service_url:
            The ID of the L{DataPilotService} which manages this pilot.
            type: string (url)

          - wall_time_left:
            The estimated remaining life time of this pilot.
            The availability of this property is not guaranteed, and depends on
            both the backend pilot framework, and on the type of pilot (not all
            pilots have a finite lifetime).
            A value of 'None' indicates that the remaining wall time is unknown.
            A negative value indicates that the pilot has an unlimited lifetime.
            type: int
    """

    def __init__ (self, dp_id) :
        """ Create a DataPilot

            Keyword arguments:
            dp_id   -- restore from dp_id

            The implementation will attempt to reconnect to the DP instance
            referenced by the ID.  If that instance got reinitialized meanwhile,
            the implementation may attempt to connect to the reinitialized
            instance.  If that is not possible, or if the instance matching
            dp_id cannot be found for other reasons, a BadParameter exception is
            raised.

        """

        # init api base
        Base.__init__ (self)

        # prepare instance data
        self.attribute_register_  ('id',             dp_id,     self.Url,    self.Scalar, self.ReadOnly)
        self.attribute_register_  ('state',          State.New, self.Enum,   self.Scalar, self.ReadOnly)
        self.attribute_register_  ('state_detail',   None,      self.String, self.Scalar, self.ReadOnly)
        self.attribute_register_  ('description',    None,      self.Any,    self.Scalar, self.ReadOnly)
        self.attribute_register_  ('service_url',    None,      self.Url,    self.Scalar, self.ReadOnly)
        self.attribute_register_  ('space_left',     -1,        self.Int,    self.Scalar, self.ReadOnly)

        # custom attributes are not allowed.
        self.attribute_extensible_ (False)

        self.set_idata_ ()

        # initialize adaptor class
        self.engine_.call ('DataPilot', 'init_', self)



    ############################################################################
    #
    def reinitialize (self, dpd) :
        """ Re-Initialize the DataPilot to the (new) DataPilotDescription.

            Keyword arguments:
            dpd -- A DataPilotDescription

            The reinitialize method is intended to change the amount of
            resources available to a pilot, without changing the pilot's state
            otherwise.  The method can be called in any non-final state, and
            will automatically move the pilot to 'Pending' state (if
            successful).  If reinitialization fails (for example, because no
            suitable resources have been found), the pilot is moved to 'Failed'
            state.

            It is up to the backend is the pilot's ID changes during the call to
            reinitialize(), but the implementation SHOULD attempt to keep the ID
            constant.

            Any data units running on the pilot remain running -- but the
            backend may achieve this by aborting the units, and resubmitting
            them to the re-initialized pilot.
        """
        return self.engine_.call ('DataPilot', 'reinitialize', self, dpd)


    def submit_data_unit (self, dud) :
        """ Submit a DU to this DataPilot.

            Keyword argument:
            dud -- The DataUnitDescription from the application

            Return:
            L{DataUnit} object

            The DUD is (possibly translated and) passed on to the DPS backend,
            which will attempt to instantiate the described data unit on
            the DataPilot.  If the pilot's resource is not suitable to create
            the requested DU, a L{Error.BadParameter} exception is raised.  Not
            raising this exception is not a guarantee that the DU will in fact
            be (able to be) executed -- in that case, the returned DU will later
            be moved to Failed state.

            On success, the returned DU is in Pending state (or moved into any
            state downstream from Pending).

            The call will will honor all attributes set on the dud.  Attributes which
            are not explicitly set are interpreted as having default values (see
            documentation of DUD), or, where default values are not specified,
            are ignored.
        """
        return self.engine_.call ('DataPilot', 'submit_data_unit', self, dud)



    def list_data_units (self) :
        """ list managed L{DataUnit}s.

            Return value:
            A list of L{DataUnit} IDs

            The returned list can include units which have not been created by
            this DP instance.  The list may be incomplete, and may not include
            units created by the DP.  There is no guarantee that units in the
            returned list can in fact be reconnected to.  Also, an inclusion in
            the list does not have any indication about the respective unit's
            state.

        """
        return self.engine_.call ('DataPilot', 'list_data_units', self)



    def get_data_unit (self, du_id) :
        """ Reconnect to a DataUnit.

            Keyword arguments:
            du_id   -- L{DataUnit}'s id

            Return value:
            A L{DataUnit} instance

            The call behaves identically to::

              du = troy.pilot.DataUnit (du_id)

        """
        return self.engine_.call ('DataPilot', 'get_data_unit', self, du_id)



    def wait (self) :
        """ Wait until DP enters a final state

        It is not an error to call wait() in a final state -- the call simply
        returns immediately.

        """
        return self.engine_.call ('DataPilot', 'wait', self)



    def cancel (self) :
        """ Move the pilot into Canceled state, releasing all resources.

        The will block until the pilot reaches Canceled state and resources have
        been released.

        It is not an error to call the method in a final state -- it will simple
        return immediately.  The pilot's state will not be changed in that case
        though.

        """
        return self.engine_.call ('DataPilot', 'cancel', self)


# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

