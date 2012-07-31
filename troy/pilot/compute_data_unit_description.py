
from compute_unit_description import ComputeUnitDescription
from data_unit_description    import DataUnitDescription


########################################################################
#
# ComuteDataUnitDescription
#
class ComputeDataUnitDescription (ComputeUnitDescription, DataUnitDescription) :
    """
    ComputeDataUnitDescription (CDUD)

    The ComputeDataUnitDescription is a combination of a job/task description
    (ComputeUnitDescription) and a data set description (DataUnitDescription) --
    as such, it encapsulates the dependency between a compute and data unit.
    """

    def __init__ (self) :
        pass

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

