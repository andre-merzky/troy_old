
from attributes import Attributes

########################################################################
#
#
#
class DataPilotDescription (Attributes) :
    """ DataPilotDescription.

    A DataPilotDescription (DPD) describes a L{DataPilot} to be
    submitted to a resource.  A well defined set of attributes can be set on
    a DPD to specify the pilot's properties, and the resource requirements
    for the pilot:

      - 'size':
          - minimum size of storage the pilot is expected to manage at any
            point in time (usually translates to number of bytes of storage
            allocated by the pilot).
          - type   : integer
          - default: 1024 * 1024 * 1024 (1GB)

      - 'project':
          - the project ID used for accounting of the pilot's resource
            consumption.
          - type   : string
          - default: ""

      - 'candidate_hosts':
          - a list of hostnames on any of which the pilot may be operate.
          - type   : string
          - default: ""

      - 'wall_time_limit':
          - the maximum time the pilot is expected to operate, in hours.
            If unspecified, the pilot is assumed to live forever.
          - type   : float (number of hours)
          - default: ""

      - 'start_time':
          - the point in time when the pilot is expected to become active.
          - type   : time (number of seconds since epoch) or class time.struct_time
          - default: ""

      - 'contact':
          - a (email, sms, IM) contact URL to notify on pilot state changes.
          - type   : string
          - default: ""



    Affinity:

    These labels should get assigned by the backend, but are exposed on API
    level for the benefit of application level schedulers::

      - 'affinity_datacenter_label':
          - pilots sharing the same label are located in the same data
            center          .
          - type   : string
          - default: ""

      - 'affinity_machine_label':
          - pilots sharing the same label are located on the same machine.
          - type   : string
          - default: ""


    Note that the DPD does not describe how the pilot is instantiated in
    detail (e.g.executable name of pilot instance) -- that is left to the
    backend to decide, and may (or may not) be configurable out-of-band.

    """

    def __init__ (self) :

        # prepare instance data
        self.attribute_register_  ('size',                     1,    self.Int,    self.Scalar, self.Writeable)
        self.attribute_register_  ('queue',                    None, self.String, self.Scalar, self.Writeable)
        self.attribute_register_  ('project',                  None, self.String, self.Scalar, self.Writeable)
        self.attribute_register_  ('candidate_hosts',          None, self.String, self.Vector, self.Writeable)
        self.attribute_register_  ('wall_time_limit',          None, self.Time,   self.Scalar, self.Writeable)
        self.attribute_register_  ('start_time',               None, self.Time,   self.Scalar, self.Writeable)
        self.attribute_register_  ('contact',                  None, self.String, self.Vector, self.Writeable)
        self.attribute_register_  ('affinity_datacenter_label',None, self.String, self.Scalar, self.Writeable)
        self.attribute_register_  ('affinity_machine_label',   None, self.String, self.Scalar, self.Writeable)

        # custom attributes are not allowed.
        self.attribute_extensible_ (False)

        self.set_idata_ ()

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

