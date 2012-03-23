
from compute_unit_description import ComputeUnitDescription
from data_unit_description    import DataUnitDescription


########################################################################
#
#
#
class ComputeDataUnitDescription (ComputeUnitDescription, DataUnitDescription) :

    """ ComputeDataUnitDescription.
        
          # Data - input/output data flow for ComputeUnit
          'input_data' : [<data unit url>, ... ],      
          'output_data': [<data unit url>, ... ]
        
    """
    
    def __setattr__ (self, attr, value):
        self[attr]=value
    
    def __getattr__ (self, attr):
        return self[attr]

