
from attributes import Attributes

########################################################################
#
#  ComuteUnitDescription
#
class ComputeUnitDescription (Attributes) :
    """
    ComputeUnitDescription (CUD)

    The ComputeUnitDescription is a job/task description based on SAGA Job
    Description.  It describes a (set of) compute activities to be enacted via
    a L{ComputeUnitService}, and to be managed by a L{ComputePilot}::

        # Action description
        'executable',           # The "action" to execute
        'arguments',            # Arguments to the "action"
        'cleanup',
        'environment',          # "environment" settings for the "action"
        'interactive',
        'contact',
        'project',
        'start_time',
        'working_directory',

        # I/O
        'input',
        'error',
        'output',
        'file_transfer',

        # Parallelism
        'number_of_processes',  # Total number of processes to start
        'processes_per_host',   # Nr of processes per host
        'threads_per_process',  # Nr of threads to start per process
        'total_core_count',     # Total number of cores requested
        'spmd_variation',       # Type and startup mechanism

        # Requirements
        'candidate_hosts',
        'cpu_architecture',
        'total_physical_memory',
        'operating_system_type',
        'total_cpu_time',
        'wall_time_limit',
        'queue'
    """


    def __init__ (self) :

        # define supported attributes

        # Action description
        self.attributes_register_ ('executable',            None, self.String, self.Scalar, self.Writable)
        self.attributes_register_ ('arguments',             None, self.String, self.Vector, self.Writable)
        self.attributes_register_ ('cleanup',               None, self.Bool,   self.Scalar, self.Writable)
        self.attributes_register_ ('environment',           None, self.String, self.Vector, self.Writable)
        self.attributes_register_ ('interactive',           None, self.Bool,   self.Scalar, self.Writable)
        self.attributes_register_ ('contact',               None, self.String, self.Vector, self.Writable)
        self.attributes_register_ ('project',               None, self.String, self.Scalar, self.Writable)
        self.attributes_register_ ('start_time',            None, self.Time,   self.Scalar, self.Writable)
        self.attributes_register_ ('working_directory',     None, self.String, self.Scalar, self.Writable)

        # I/O
        self.attributes_register_ ('input',                 None, self.Url,    self.Scalar, self.Writable)
        self.attributes_register_ ('error',                 None, self.Url,    self.Scalar, self.Writable)
        self.attributes_register_ ('output',                None, self.Url,    self.Scalar, self.Writable)
        self.attributes_register_ ('file_transfer',         None, self.String, self.Vector, self.Writable)

        # Parallelism
        self.attributes_register_ ('number_of_processes',   None, self.Int,    self.Scalar, self.Writable)
        self.attributes_register_ ('processes_per_host',    None, self.Int,    self.Scalar, self.Writable)
        self.attributes_register_ ('threads_per_process',   None, self.Int,    self.Scalar, self.Writable)
        self.attributes_register_ ('total_core_count',      None, self.Int,    self.Scalar, self.Writable)
        self.attributes_register_ ('spmd_variation',        None, self.Enum,   self.Scalar, self.Writable)

        # Requirements
        self.attributes_register_ ('candidate_hosts',       None, self.String, self.Vector, self.Writable)
        self.attributes_register_ ('cpu_architecture',      None, self.Enum,   self.Scalar, self.Writable)
        self.attributes_register_ ('operating_system_type', None, self.Enum,   self.Scalar, self.Writable)
        self.attributes_register_ ('total_physical_memory', None, self.Int,    self.Scalar, self.Writable)
        self.attributes_register_ ('total_cpu_time',        None, self.Time,   self.Scalar, self.Writable)
        self.attributes_register_ ('wall_time_limit',       None, self.Time,   self.Scalar, self.Writable)
        self.attributes_register_ ('queue',                 None, self.String, self.Scalar, self.Writable)

        # custom attributes are not allowed.
        self.attributes_extensible_ (False)



# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

