
from troy.base  import Base


########################################################################
#
#
#
class DataPilot (Base) :
    """ 
    DataPilot (PilotStore)

    This is the object that is returned by the :class:`troy.PilotFramework` when a new
    DataPilot is created based on a DataPilotDescription.

    The DataPilot object can be used by the application to keep track of
    DataPilots that are active.  A DataPilot has state, can be queried, can be
    cancelled and re-initialized.


    Properties::



        - id:
          The id may be 'None' if the Pilot is not yet in Running state.  The
          returned ID can be used to connect to the CP instance later on, for
          example from within a different application instance.  
          Type: string (url)



        - state:
          The state of the pilot.
          Type: :func:`troy.State` (enum)



        - state_detail:
          The backend state of the pilot.  The value of this property is not
          interpreted by Troy, and is up to the backend pilot framework.
          Type: string



        - description:
          The DataPilotDescription used to create this pilot.  That description
          is not guaranteed to be available, nor is it guaranteed to be complete
          -- in particular for reconnected pilots.  Its existence and
          completeness depends on the ability to inspect backend pilot
          instances.
          Type: :class:`troy.troy.DataPilotDescription`



        - framework:
          The ID of the :class:`troy.PilotFramework` which manages this pilot.
          Type: string (url)



        - units:
          A list of :class:`troy.DataUnit` IDs, representing compute units managed by this
          pilot.
          Type: string (url)



        - wall_time_left:
          The estimated remaining life time of this pilot.
          The availability of this property is not guaranteed, and depends on
          both the backend pilot framework, and on the type of pilot (not all
          pilots have a finite lifetime).
          A value of 'None' indicates that the remaining wall time is unknown.
          A negative value indicates that the pilot has an unlimited lifetime.
          Type: int
    """

    ############################################################################
    #
    def __init__ (self, dp_id) :
        """ 
        Create a DataPilot

        Keyword arguments:
        dp_id   -- restore from dp_id

        The implementation will attempt to reconnect to the DP instance
        referenced by the ID.  If that instance got reinitialized meanwhile, the
        implementation may attempt to connect to the reinitialized instance.  If
        that is not possible, or if the instance matching dp_id cannot be found
        for other reasons, a BadParameter exception is raised.
        """

        # init api base
        Base.__init__ (self)

        # prepare supported attributes
        self.attributes_register_  ('id',             dp_id,     self.Url,    self.Scalar, self.ReadOnly)
        self.attributes_register_  ('state',          State.New, self.Enum,   self.Scalar, self.ReadOnly)
        self.attributes_register_  ('state_detail',   None,      self.String, self.Scalar, self.ReadOnly)
        self.attributes_register_  ('description',    None,      self.Any,    self.Scalar, self.ReadOnly)
        self.attributes_register_  ('framework',      None,      self.Url,    self.Scalar, self.ReadOnly)
        self.attributes_register_  ('units',          None,      self.Url,    self.Vector, self.ReadOnly)
        self.attributes_register_  ('space_left',     -1,        self.Int,    self.Scalar, self.ReadOnly)

        # custom attributes are not allowed.
        self.attributes_extensible_ (False)

        # we register callbacks to pull variable object state from the backend
        # / adaptor.
        self.attributes_set_getter_ ('state',        self._pull_state)
        self.attributes_set_getter_ ('state_detail', self._pull_state)
        self.attributes_set_getter_ ('space_left',   self._pull_state)

        # initialize adaptor class
        self._engine.call ('DataPilot', 'init_', self)


    ############################################################################
    #
    def _push_state (self, obj, key) :
        """
        tell the adaptor to push state changes to the backend
        """
        return self._engine.call ('DataPilot', '_push_state', self, obj, key)


    ############################################################################
    #
    def _pull_state (self, obj, key) :
        """
        tell the adaptor to pull state changes from the backend
        """
        return self._engine.call ('DataPilot', '_pull_state', self, obj, key)


    ############################################################################
    #
    def reinitialize (self, dpd) :
        """ 
        Re-Initialize the DataPilot to the (new) DataPilotDescription.

        Keyword arguments:
        dpd -- A DataPilotDescription

        The reinitialize method is intended to change the amount of resources
        available to a pilot, without changing the pilot's state otherwise.  The
        method can be called in any non-final state, and will automatically move
        the pilot to 'Pending' state (if successful).  If reinitialization fails
        (for example, because no suitable resources have been found), the pilot
        is moved to 'Failed' state.

        It is up to the backend is the pilot's ID changes during the call to
        reinitialize(), but the implementation SHOULD attempt to keep the ID
        constant.

        Any data units running on the pilot remain running -- but the backend
        may achieve this by aborting the units, and resubmitting them to the
        re-initialized pilot.
        """
        return self._engine.call ('DataPilot', 'reinitialize', self, dpd)


    ############################################################################
    #
    def submit_unit (self, dud) :
        """ 
        Submit a DU to this DataPilot.

        Keyword argument:
        dud -- The DataUnitDescription from the application

        Return:
        :class:`troy.DataUnit` object

        The DUD is (possibly translated and) passed on to the PF backend, which
        will attempt to instantiate the described data workload unit on the
        DataPilot.  If the pilot's resource is not suitable to create the
        requested DU, a :attribute:`troy.Error.BadParameter` exception is raised.  Not raising
        this exception is not a guarantee that the DU will in fact be (able to
        be) executed -- in that case, the returned DU will later be moved to
        Failed state.

        On success, the returned DU is in Pending state (or moved into any state
        downstream from Pending).

        The call will will honor all attributes set on the dud.  Attributes
        which are not explicitly set are interpreted as having default values
        (see documentation of DUD), or, where default values are not specified,
        are ignored.
        """
        return self._engine.call ('DataPilot', 'submit_unit', self, dud)


    ############################################################################
    #
    def list_units (self) :
        """ 
        list managed :class:`troy.DataUnit` instances.

        Return value:
        A list of :class:`troy.DataUnit` IDs

        The returned list can include units which have not been created by this
        DP instance.  The list may be incomplete, and may not include units
        created by the DP.  There is no guarantee that units in the returned
        list can in fact be reconnected to.  Also, an inclusion in the list does
        not have any indication about the respective unit's state.
        """
        return self._engine.call ('DataPilot', 'list_units', self)


    ############################################################################
    #
    def wait (self) :
        """ 
        Wait until DP enters a final state

        It is not an error to call wait() in a final state -- the call simply
        returns immediately.
        """
        return self._engine.call ('DataPilot', 'wait', self)


    ############################################################################
    #
    def cancel (self) :
        """ 
        Move the pilot into Canceled state, releasing all resources.

        The will block until the pilot reaches Canceled state and resources have
        been released.

        It is not an error to call the method in a final state -- it will simple
        return immediately.  The pilot's state will not be changed in that case
        though.

        """
        return self._engine.call ('DataPilot', 'cancel', self)


# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

