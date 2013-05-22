
from troy.attributes import Attributes

########################################################################
#
#
#
class ComputePilotDescription (Attributes) :
    """ ComputePilotDescription.

    A ComputePilotDescription (CPD) describes a :class:`troy.ComputePilot` to be
    submitted to a resource.  A well defined set of attributes can be set on
    a CPD to specify the pilot's properties, and the resource requirements
    for the pilot:



      - 'size':
          - minimum number of processes the pilot is expected to manage at any
            point in time (usually translates to number of CPU process slots
            managed by the pilot).
          - type   : integer
          - default: 1


      - 'environment':
          - a set of key/value pairs, to be exported into the environment of
            any :class:`troy.ComputeUnit` on that pilot.
          - type   : dictionary
          - default: {}


      - 'queue':
          - the name of the queue the pilot should be submitted to.
          - type   : string
          - default: ""


      - 'project':
          - the project ID used for accounting of the pilot's resource
            consumption.
          - type   : string
          - default: ""


      - 'candidate_hosts':
          - a list of hostnames on any of which the pilot may be operate.
          - type   : string
          - default: ""


      - 'cpu_architecture':
          - the CPU architecture the pilot is expected to run on..
          - type   : string, values as defined by GLUE.v2
          - default: ""


      - 'operating_system_type':
          - the operating system the pilot is expected to run on.
          - type   : string, values as defined by GLUE.v2
          - default: ""


      - 'total_physical_memory':
          - the maximum amount of memory the pilot is expected to allocate, in
            total (in MByte).
          - type   : int
          - default: ""


      - 'total_cpu_time':
          - the maximum number of CPU hours the pilot is expected to consume, in
            total.
          - type   : float (number of CPU hours)
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


    Note that the CPD does not describe how the pilot is instantiated in
    detail (e.g.executable name of pilot instance) -- that is left to the
    backend to decide, and may (or may not) be configurable out-of-band.

    """

    def __init__ (self) :

        # define supported attributes
        self._attributes_register  ('size',                     1,    self.Int,    self.Scalar, self.Writable)
        self._attributes_register  ('queue',                    None, self.String, self.Scalar, self.Writable)
        self._attributes_register  ('project',                  None, self.String, self.Scalar, self.Writable)
        self._attributes_register  ('candidate_hosts',          None, self.String, self.Vector, self.Writable)
        self._attributes_register  ('cpu_architecture',         None, self.Enum,   self.Scalar, self.Writable)
        self._attributes_register  ('operating_system_type',    None, self.Enum,   self.Scalar, self.Writable)
        self._attributes_register  ('total_physical_memory',    None, self.Int,    self.Scalar, self.Writable)
        self._attributes_register  ('total_cpu_time',           None, self.Time,   self.Scalar, self.Writable)
        self._attributes_register  ('wall_time_limit',          None, self.Time,   self.Scalar, self.Writable)
        self._attributes_register  ('start_time',               None, self.Time,   self.Scalar, self.Writable)
        self._attributes_register  ('contact',                  None, self.String, self.Vector, self.Writable)
        self._attributes_register  ('affinity_datacenter_label',None, self.String, self.Scalar, self.Writable)
        self._attributes_register  ('affinity_machine_label',   None, self.String, self.Scalar, self.Writable)

        # FIXME: the attribs below are for BJ
        self._attributes_register  ('service_url',              None, self.String, self.Scalar, self.Writable)
        self._attributes_register  ('working_directory',        None, self.String, self.Scalar, self.Writable)
        self._attributes_register  ('number_of_processes',      None, self.String, self.Scalar, self.Writable)

        # custom attributes are not allowed.
        self._attributes_extensible (False)



# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

