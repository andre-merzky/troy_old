
from troy.base import Base


########################################################################
#
# DataUnit (DU)
#
class DataUnit (Base) :

    """ 
    DataUnit.

    This is the object that is returned by :class:`troy.Troy` or an :class:`troy.PilotFramework` when
    a new DataUnit is created based on a :class:`troy.DataUnitDescription`.

    The DataUnit object can be used by the application to keep track of
    DataUnits that are active.  A DataUnit has state, can be queried and can be
    cancelled.  
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
        self._attributes_register  ('pilot_id',       None,      self.Url,    self.Scalar, self.ReadOnly)

        # we register callbacks to pull variable object state from the backend
        # / adaptor.
        self._attributes_set_getter ('state',           self._pull_state)
        self._attributes_set_getter ('state_detail',    self._pull_state)

        # initialize id
        self.id = id

        # initialize adaptor class
        self._engine.call ('DataUnit', 'init_', self)


    ############################################################################
    #
    def _push_state (self, obj, key) :
        """
        tell the adaptor to push state changes to the backend
        """
        return self._engine.call ('DataUnit', '_push_state', self, obj, key)


    ############################################################################
    #
    def _pull_state (self, obj, key) :
        """
        tell the adaptor to pull state changes from the backend
        """
        return self._engine.call ('DataUnit', '_pull_state', self, obj, key)


    ############################################################################
    #
    def wait (self) :
        """ Wait until DU enters a final state """
        return self._engine.call ('DataUnit', 'wait', self)


    ############################################################################
    #
    def cancel (self) :
        """ Cancel the DU """
        return self._engine.call ('DataUnit', 'cancel', self)


# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

