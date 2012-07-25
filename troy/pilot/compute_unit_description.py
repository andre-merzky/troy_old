
########################################################################
#
#  ComuteUnitDescription
# 
class ComputeUnitDescription (dict) :
    """  ComputeUnitDescription.
    
        The ComputeUnitDescription is a job/task/call description based on 
        SAGA Job Description. 
        
    """

    # Class members
    __slots__ = (
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
    )


    def __init__ (self) :
        pass


    def __setattr__ (self, attr, value) :
        # TODO: key checks, type checks
        self[attr]=value
        
    
    def __getattr__ (self, attr) :
        return self[attr]

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

