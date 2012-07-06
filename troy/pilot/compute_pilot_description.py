
########################################################################
#
#
#
class ComputePilotDescription (dict):
    """ ComputePilotDescription.

    A ComputePilotDescription (CPD) describes a L{ComputePilot} to be
    submitted to a resource.  A well defined set of attributes can be set on
    a CPD to specify the pilot's properties, and the resource requirements
    for the pilot:

      - 'size':
          - maximum number of processes the pilot is expected to host at any point
            in time (usually translates to number of CPU process slots managed by
            the pilot).  
          - type   : integer
          - default: 1

      - 'environment':
          - a set of key/value pairs, to be exported into the environment of 
            L{ComputeUnit}s on that pilot.
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
          - a list of hostnames on any of which the pilot may be run.
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
          - the maximum time the pilot is expected to run, in hours.
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
          - pilot jobs sharing the same label are located in the same data
            center          .
          - type   : string
          - default: ""

      - 'affinity_machine_label':
          - pilot jobs sharing the same label are located on the same machine.
          - type   : string
          - default: ""


    Note that the CPD does not describe how the pilot is instantiated in
    detail (e.g.executable name of pilot instance) -- that is left to the
    backend to decide, and may (or may not) be configurable out-of-band.
      
    """

    # Class members
    __slots__ = (
        'size',                     # int
        'queue',                    # string
        'project',                  # string
        'candidate_hosts',          # string vec
        'cpu_architecture',         # string / enum
        'operating_system_type',    # string / enum
        'total_physical_memory',    # int
        'total_cpu_time',           # time
        'wall_time_limit',          # time
        'start_time',               # time
        'contact',                  # string vec
        'affinity_datacenter_label',# string
        'affinity_machine_label',   # string
    )


    def __init__ (self) :
        print "cpd: init"

        # assign defaults
        self['size'] = 1
        
        pass
    
    
    def __setattr__ (self, attr, value) :
        self[attr]=value
        
    
    def __getattr__ (self, attr) :
        return self[attr]
    
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

