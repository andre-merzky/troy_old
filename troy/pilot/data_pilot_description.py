
########################################################################
# 
#
#
class DataPilotDescription (dict) :
    """ DataPilotDescription.

        A DataPilotDescription describes the DataPilot to be submitted to
        a resource.
    """
    
    # Class members
    __slots__ = (
        # Pilot / Agent description
        'service_url', # "ssh://localhost/tmp/datapilot/",
        'size',        # 100, size in MegaByte
            
        # Affinity labels
        'affinity_datacenter_label',    # DataPilot sharing that label are located in the same data center
        'affinity_machine_label',       # DataPilot sharing that label are located on the same machine
    )


    def __init__ (self):
        pass
    

    def __setattr__ (self, attr, value):
        self[attr]=value
        
    
    def __getattr__ (self, attr):
        return self[attr]


