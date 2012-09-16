
from troy.base  import Base
from troy.state import State


########################################################################
#
#
#
class ComputePilot (Base) :
    """ 
    ComputePilot (PilotJob)

    This is the object that is returned the :class:`troy.PilotFramework` when a new
    ComputePilot is created based on a :class:`troy.ComputePilotDescription`.

    The ComputePilot object can be used by the application to keep track of
    ComputePilots that are active.  A ComputePilot has state, can be queried,
    can be cancelled and be re-initialized.


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
          The ComputePilotDescription used to create this pilot.  That
          description is not guaranteed to be available, nor is it guaranteed to
          be complete -- in particular for reconnected pilots.  Its existence
          and completeness depends on the ability to inspect backend pilot
          instances.
          Type: :class:`troy.troy.ComputePilotDescription`



        - framework:
          The ID of the :class:`troy.PilotFramework` which manages this pilot.
          Type: string (url)



        - units:
          A list of :class:`troy.ComputeUnit` IDs, representing compute units managed by
          this pilot.
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
    def __init__ (self, cp_id) :
        """ 
        Create a ComputePilot

        Keyword arguments:
        cp_id   -- restore from cp_id

        The implementation will attempt to reconnect to the CP instance
        referenced by the ID.  If that instance got reinitialized meanwhile, the
        implementation may attempt to connect to the reinitialized instance.  If
        that is not possible, or if the instance matching cp_id cannot be found
        for other reasons, a BadParameter exception is raised.
        """

        # init api base
        Base.__init__ (self)

        # prepare supported attributes
        self.attributes_register_ ('id',             cp_id,     self.Url,    self.Scalar, self.ReadOnly)
        self.attributes_register_ ('state',          State.New, self.Enum,   self.Scalar, self.ReadOnly)
        self.attributes_register_ ('state_detail',   None,      self.String, self.Scalar, self.ReadOnly)
        self.attributes_register_ ('description',    None,      self.Any,    self.Scalar, self.ReadOnly)
        self.attributes_register_ ('framework',      None,      self.Url,    self.Scalar, self.ReadOnly)
        self.attributes_register_ ('units',          None,      self.Url,    self.Vector, self.ReadOnly)
        self.attributes_register_ ('wall_time_left', -1,        self.Time,   self.Scalar, self.ReadOnly)

        # custom attributes are not allowed.
        self.attributes_extensible_ (False)

        # we register callbacks to pull variable object state from the backend
        # / adaptor.
        self.attributes_set_getter_ ('state',           self._pull_state)
        self.attributes_set_getter_ ('state_detail',    self._pull_state)
        self.attributes_set_getter_ ('wall_time_left',  self._pull_state)


        #initialize id
        self.id    = cp_id
        self.state = State.New

        # initialize adaptor class
        self.engine_.call ('ComputePilot', 'init_', self)



    ############################################################################
    #
    def _push_state (self, obj, key) :
        """
        tell the adaptor to push state changes to the backend
        """
        return self.engine_.call ('ComputePilot', '_push_state', self, obj, key)


    ############################################################################
    #
    def _pull_state (self, obj, key) :
        """
        tell the adaptor to pull state changes from the backend
        """
        return self.engine_.call ('ComputePilot', '_pull_state', self, obj, key)


    ############################################################################
    #
    def reinitialize (self, cpd) :
        """ 
        Re-Initialize the ComputePilot to the (new) ComputePilotDescription.

        Keyword arguments:
        cpd -- A ComputePilotDescription

        The reinitialize method is intended to change the amount of resources
        available to a pilot, without changing the pilot's state otherwise.  The
        method can be called in any non-final state, and will automatically move
        the pilot to 'Pending' state (if successful).  If reinitialization fails
        (for example, because no suitable resources have been found), the pilot
        is moved to 'Failed' state.

        It is up to the backend is the pilot's ID changes during the call to
        reinitialize(), but the implementation SHOULD attempt to keep the ID
        constant.

        Any compute units running on the pilot remain running -- but the backend
        may achieve this by aborting the units, and resubmitting them to the
        re-initialized pilot.
        """
        return self.engine_.call ('ComputePilot', 'reinitialize', self, cpd)



    ############################################################################
    #
    def submit_unit (self, cud) :
        """ 
        Submit a CU to this ComputePilot.

        Keyword argument:
        cud -- The :class:`troy.ComputeUnitDescription` from the application

        Return:
        :class:`troy.ComputeUnit` object

        The CUD is (possibly translated and) passed on to the PF backend, which
        will attempt to instantiate the described workload process on the
        ComputePilot.  If the pilot's resource is not suitable to create the
        requested CU, a :class:`troy.Error.BadParameter` exception is raised.  Not raising
        this exception is not a guarantee that the CU will in fact be (able to
        be) executed -- in that case, the returned CU will later be moved to
        Failed state.

        On success, the returned CU is in Pending state (or moved into any state
        downstream from Pending).

        The call will will honor all attributes set on the cud.  Attributes
        which are not explicitly set are interpreted as having default values
        (see documentation of CUD), or, where default values are not specified,
        are ignored.
        """
        return self.engine_.call ('ComputePilot', 'submit_unit', self, cud)



    ############################################################################
    #
    def list_units (self) :
        """ 
        list managed :class:`troy.ComputeUnit`s.

        Return value:
        A list of :class:`troy.ComputeUnit` IDs

        The returned list can include units which have not been created by this
        CP instance.  The list may be incomplete, and may not include units
        created by the CP.  There is no guarantee that units in the returned
        list can in fact be reconnected to.  Also, an inclusion in the list does
        not have any indication about the respective unit's state.
        """
        return self.engine_.call ('ComputePilot', 'list_units', self)


    ############################################################################
    #
    def wait (self) :
        """ 
        Wait until CP enters a final state

        It is not an error to call wait() in a final state -- the call simply
        returns immediately.
        """
        return self.engine_.call ('ComputePilot', 'wait', self)


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
        return self.engine_.call ('ComputePilot', 'cancel', self)


# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

