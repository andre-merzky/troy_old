
########################################################################
#
#
#
class ComputePilotDescription (dict):
    """  ComputePilotDescription.

        A ComputePilotDescription describes the ComputePilot to be submitted to
        a resource.
    """

    # Class members
    __slots__ = (
        # Pilot / Agent description
        'executable',               # string
        'arguments',                # string vec
        'cleanup',                  # bool
        'environment',              # string vec or hash
        'interactive',              # bool
        'contact',                  # string vec, unused
        'project',                  # string
        'start_time',               # time
        'working_directory',        # url
        # I/O
        'input',                    # url
        'error',                    # url
        'output',                   # url
        'file_transfer',            # string vec
        # Parallelism
        'number_of_processes',      # int, # of processes to start
        'processes_per_host',       # int, # of processes per host
        'threads_per_process',      # int, # of threads to start per process
        'total_core_count',         # int, # of cores requested
        'spmd_variation',           # string, type and startup mechanism
        
        # Requirements
        'candidate_hosts',          # string vec
        'cpu_architecture',         # string / enum
        'operating_system_type',    # string / enum
        'total_physical_memory',    # int in MB
        'total_cpu_time',           # time
        'wall_time_limit',          # time
        'queue',                    # string
        
        # Affinity
        'affinity_datacenter_label',# pilot jobs sharing the same label are located in the same data center          
        'affinity_machine_label',   # pilot jobs sharing the same label are located on the same machine
    )


    def __init__ (self):
        print "cpd: init"
        pass
    
    
    def __setattr__ (self, attr, value):
        self[attr]=value
        
    
    def __getattr__ (self, attr):
        return self[attr]
    
