
from compute_unit import ComputeUnit
from data_unit    import DataUnit


########################################################################
#
# ComputeDataUnit (CDU)
#
class ComputeDataUnit (ComputeUnit, DataUnit) :

    """
    ComputeDataUnit.

    The ComputeDataUnit is a handle to a unit of (compute and/or data) workload.
    It is the object that is returned by the ComputeDataUnitService when a new
    ComputeDataUnit is created based on a ComputeDataUnitDescription.

    The ComputeDataUnit object can be used by the application to keep track of
    ComputeDataUnits that are active.

    A ComputeDataUnit has state, can be queried and can be cancelled.
    """

    def __init__ (self, cdu_id) :

        # init api base
        Base.__init__ (self)

        # prepare supported attributes
        self.attribute_register_  ('id',             cdu_id,    self.Url,    self.Scalar, self.ReadOnly)
        self.attribute_register_  ('state',          State.New, self.Enum,   self.Scalar, self.ReadOnly)
        self.attribute_register_  ('state_detail',   None,      self.String, self.Scalar, self.ReadOnly)
        self.attribute_register_  ('description',    None,      self.Any,    self.Scalar, self.ReadOnly)
        self.attribute_register_  ('service_url',    None,      self.Url,    self.Scalar, self.ReadOnly)
        self.attribute_register_  ('pilot_id',       None,      self.Url,    self.Scalar, self.ReadOnly)

        # initialize adaptor class
        self.engine_.call ('ComputeDataUnit', 'init_', self)


    def wait (self) :
        """ Wait until CDU enters a final state """
        return self.engine_.call ('ComputeDataUnit', 'wait', self)


    def cancel (self) :
        """ Cancel the CDU """
        return self.engine_.call ('ComputeDataUnit', 'cancel', self)


# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

