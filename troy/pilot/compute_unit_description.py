
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
        self.attribute_register ('executable',            None, self.String, self.Scalar, self.Writable)
        self.attribute_register ('arguments',             None, self.String, self.Vector, self.Writable)
        self.attribute_register ('cleanup',               None, self.Bool,   self.Scalar, self.Writable)
        self.attribute_register ('environment',           None, self.String, self.Vector, self.Writable)
        self.attribute_register ('interactive',           None, self.Bool,   self.Scalar, self.Writable)
        self.attribute_register ('contact',               None, self.String, self.Vector, self.Writable)
        self.attribute_register ('project',               None, self.String, self.Scalar, self.Writable)
        self.attribute_register ('start_time',            None, self.Time,   self.Scalar, self.Writable)
        self.attribute_register ('working_directory',     None, self.String, self.Scalar, self.Writable)

        # I/O
        self.attribute_register ('input',                 None, self.Url,    self.Scalar, self.Writable)
        self.attribute_register ('error',                 None, self.Url,    self.Scalar, self.Writable)
        self.attribute_register ('output',                None, self.Url,    self.Scalar, self.Writable)
        self.attribute_register ('file_transfer',         None, self.String, self.Vector, self.Writable)

        # Parallelism
        self.attribute_register ('number_of_processes',   None, self.Int,    self.Scalar, self.Writable)
        self.attribute_register ('processes_per_host',    None, self.Int,    self.Scalar, self.Writable)
        self.attribute_register ('threads_per_process',   None, self.Int,    self.Scalar, self.Writable)
        self.attribute_register ('total_core_count',      None, self.Int,    self.Scalar, self.Writable)
        self.attribute_register ('spmd_variation',        None, self.Enum,   self.Scalar, self.Writable)

        # Requirements
        self.attribute_register ('candidate_hosts',       None, self.String, self.Vector, self.Writable)
        self.attribute_register ('cpu_architecture',      None, self.Enum,   self.Scalar, self.Writable)
        self.attribute_register ('operating_system_type', None, self.Enum,   self.Scalar, self.Writable)
        self.attribute_register ('total_physical_memory', None, self.int,    self.Scalar, self.Writable)
        self.attribute_register ('total_cpu_time',        None, self.Time,   self.Scalar, self.Writable)
        self.attribute_register ('wall_time_limit',       None, self.Time,   self.Scalar, self.Writable)
        self.attribute_register ('queue',                 None, self.String, self.Scalar, self.Writable)

        # custom attributes are not allowed.
        self.attribute_extensible_ (False)



# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

