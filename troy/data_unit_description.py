
from troy.attributes import Attributes

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

    The description is used via :class:`troy.Troy` or an
    :class:`troy.PilotFramework` to instantiate :class:`troy.DataUnit`
    instances, i.e.  physical data representations, which are managed by
    a :class:`troy.DataPilot`.

    Currently, no directory URLs are supported.
    """

    def __init__ (self) :

        # define supported attributes
        self._attributes_register  ('urls', [], self.Url, self.Vector, self.Writable)



# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

