
from attributes import Attributes

########################################################################
#
# DataUnitDescription
#
class DataUnitDescription (Attributes) :
    """
    DataUnitDescription (DUD)

    The DataUnitDescription describes a set of data items which are expected to
    share locality properties.  The data items are referenced by URLs, so, in
    some sense, the DUD is a list of URLs.

    The description is used via a L{DataUnitService} to instantiate
    L{DataUnit}s, i.e. physical data representations, which are managed by
    a L{DataPilot}.

    Currently, no directory URLs are supported.
    """

    def __init__ (self) :

        # prepare instance data
        self.attribute_register_  ('urls', [], self.Url, self.Vector, self.Writeable)

        self.set_idata_ ()


    def __setattr__ (self, attr, value) :
        # TODO: key checks, type checks
        self[attr]=value


    def __getattr__ (self, attr) :
        return self[attr]

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

