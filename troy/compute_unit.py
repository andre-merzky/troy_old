
from troy.base  import Base
from troy.state import State


########################################################################
#
#  ComputeUnit (CU)
#
class ComputeUnit (Base) :
    """
    ComputeUnit

    This is the object that is returned by :class:`troy.Troy` or an :class:`troy.PilotFramework` when
    a new ComputeUnit is created based on a :class:`troy.ComputeUnitDescription`.

    The ComputeUnit object can be used by the application to keep track of
    ComputeUnits that are active.  A ComputeUnit has state, can be queried and
    can be cancelled.  


    Properties::



        - id:
          The id may be 'None' if the Unit is not yet in Running state.  The
          returned ID can be used to connect to the CU instance later on, for
          example from within a different application instance.  
          Type: string (url)



        - state:
          The state of the CU.
          Type: :func:`troy.State` (enum)



        - state_detail:
          The backend state of the CU.  The value of this property is not
          interpreted by Troy, and is up to the backend pilot framework.
          Type: string



        - description:
          The ComputeUnitDescription used to create this pilot.  That
          description is not guaranteed to be available, nor is it guaranteed to
          be complete -- in particular for reconnected CUs.  Its existence
          and completeness depends on the ability to inspect backend pilot
          instances.
          Type: :class:`troy.troy.ComputeUnitDescription`



        - pilot:
          The ID of the pilot which manages this CU.  This ID may be None if the
          CU is not yet bound to a specific pilot.
          Type: string (url)



        - framework:
          The ID of the pilot framework which manages this CU.  This ID may be 
          None if the CU is not yet bound to a specific framework
          Type: string (url)

    """

    ############################################################################
    #
    def __init__ (self, id) :

        # init api base
        Base.__init__ (self)

        # prepare supported attributes
        self._attributes_register  ('id',             None,      self.Url,    self.Scalar, self.ReadOnly)
        self._attributes_register  ('state',          State.New, self.Enum,   self.Scalar, self.ReadOnly)
        self._attributes_register  ('state_detail',   None,      self.String, self.Scalar, self.ReadOnly)
        self._attributes_register  ('description',    None,      self.Any,    self.Scalar, self.ReadOnly)
        self._attributes_register  ('pilot',          None,      self.Url,    self.Scalar, self.ReadOnly)
        self._attributes_register  ('framework',      None,      self.Url,    self.Scalar, self.ReadOnly)

        # we register callbacks to pull variable object state from the backend
        # / adaptor.
        self._attributes_set_getter ('state',           self._pull_state)
        self._attributes_set_getter ('state_detail',    self._pull_state)

        # initialize id
        self.id = id

        # initialize adaptor class
        self._engine.call ('ComputeUnit', 'init_', self)


    ############################################################################
    #
    def _push_state (self, obj, key) :
        """
        tell the adaptor to push state changes to the backend
        """
        return self._engine.call ('ComputeUnit', '_push_state', self, obj, key)


    ############################################################################
    #
    def _pull_state (self, obj, key) :
        """
        tell the adaptor to pull state changes from the backend
        """
        return self._engine.call ('ComputeUnit', '_pull_state', self, obj, key)


    ############################################################################
    #
    def wait (self) :
        """ Wait until CU enters a final state """
        return self._engine.call ('ComputeUnit', 'wait', self)


    ############################################################################
    #
    def cancel (self) :
        """ Cancel the CU """
        return self._engine.call ('ComputeUnit', 'cancel', self)


# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

