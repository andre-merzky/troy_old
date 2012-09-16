
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
        self.attributes_register_  ('id',             None,      self.Url,    self.Scalar, self.ReadOnly)
        self.attributes_register_  ('state',          State.New, self.Enum,   self.Scalar, self.ReadOnly)
        self.attributes_register_  ('state_detail',   None,      self.String, self.Scalar, self.ReadOnly)
        self.attributes_register_  ('description',    None,      self.Any,    self.Scalar, self.ReadOnly)
        self.attributes_register_  ('pilot_id',       None,      self.Url,    self.Scalar, self.ReadOnly)

        # we register callbacks to pull variable object state from the backend
        # / adaptor.
        self.attributes_set_getter_ ('state',           self._pull_state)
        self.attributes_set_getter_ ('state_detail',    self._pull_state)

        # initialize id
        self.id = id

        # initialize adaptor class
        self.engine_.call ('DataUnit', 'init_', self)


    ############################################################################
    #
    def _push_state (self, obj, key) :
        """
        tell the adaptor to push state changes to the backend
        """
        return self.engine_.call ('DataUnit', '_push_state', self, obj, key)


    ############################################################################
    #
    def _pull_state (self, obj, key) :
        """
        tell the adaptor to pull state changes from the backend
        """
        return self.engine_.call ('DataUnit', '_pull_state', self, obj, key)


    ############################################################################
    #
    def wait (self) :
        """ Wait until DU enters a final state """
        return self.engine_.call ('DataUnit', 'wait', self)


    ############################################################################
    #
    def cancel (self) :
        """ Cancel the DU """
        return self.engine_.call ('DataUnit', 'cancel', self)


# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

