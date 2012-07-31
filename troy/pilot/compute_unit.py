
from base import Base

########################################################################
#
#  ComputeUnit (CU)
#
class ComputeUnit (Base) :

    """
    ComputeUnit

    This is the object that is returned by the ComputeUnitService when a new
    ComputeUnit is created based on a ComputeUnitDescription.

    The ComputeUnit object can be used by the application to keep track of
    ComputeUnits that are active.

    A ComputeUnit has state, can be queried and can be cancelled.
    """

    def __init__ (self, cu_id) :

        # init api base
        Base.__init__ (self)

        # prepare instance data
        self.attribute_register_  ('id',             cu_id,     self.Url,    self.Scalar, self.ReadOnly)
        self.attribute_register_  ('state',          State.New, self.Enum,   self.Scalar, self.ReadOnly)
        self.attribute_register_  ('state_detail',   None,      self.String, self.Scalar, self.ReadOnly)
        self.attribute_register_  ('description',    None,      self.Any,    self.Scalar, self.ReadOnly)
        self.attribute_register_  ('service_url',    None,      self.Url,    self.Scalar, self.ReadOnly)

        self.set_idata_ ()

        # initialize adaptor class
        self.engine_.call ('ComputeUnit', 'init_', self)


    def wait (self) :
        """ Wait until CU enters a final state """
        return self.engine_.call ('ComputeUnit', 'wait', self)


    def cancel (self) :
        """ Cancel the CU """
        return self.engine_.call ('ComputeUnit', 'cancel', self)


# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

