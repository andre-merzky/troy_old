
from troy.base import Base


########################################################################
#
# DataUnit (DU)
#
class DataUnit (Base) :

    """ 
    DataUnit.

    This is the object that is returned by L{Troy} or an L{PilotFramework} when
    a new DataUnit is created based on a L{DataUnitDescription}.

    The DataUnit object can be used by the application to keep track of
    DataUnits that are active.  A DataUnit has state, can be queried and can be
    cancelled.  
    """


    ############################################################################
    #
    def __init__ (self, du_id) :

        # init api base
        Base.__init__ (self)

        # prepare supported attributes
        self.attributes_register_  ('id',             du_id,     self.Url,    self.Scalar, self.ReadOnly)
        self.attributes_register_  ('state',          State.New, self.Enum,   self.Scalar, self.ReadOnly)
        self.attributes_register_  ('state_detail',   None,      self.String, self.Scalar, self.ReadOnly)
        self.attributes_register_  ('description',    None,      self.Any,    self.Scalar, self.ReadOnly)
        self.attributes_register_  ('pilot_id',       None,      self.Url,    self.Scalar, self.ReadOnly)

        # initialize adaptor class
        self.engine_.call ('DataUnit', 'init_', self)


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

