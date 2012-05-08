
"""

For the sake of code organization, all API classes are defined in a separate
file.  Alas, pythons module naming rules then introduce an additional element,
the file name, so that, for example, the compute pilot class would be available
as troy.pilot.compute_pilot.ComputePilot.  We thus move the symbols into the
parent namespace, which makes them available as, for example,
troy.pilot.ComputePilot.

"""

# we don't want to expose 'base'. really - that is not part of the API
# from troy.pilot.base                           import Base                         

from troy.pilot.state                          import State                        
from troy.pilot.callback                       import Callback                     
from troy.pilot.exception                      import TroyException, Error

from troy.pilot.compute_data_unit_description  import ComputeDataUnitDescription
from troy.pilot.compute_data_unit              import ComputeDataUnit            
from troy.pilot.compute_data_unit_service      import ComputeDataUnitService    

from troy.pilot.compute_pilot_description      import ComputePilotDescription    
from troy.pilot.compute_pilot                  import ComputePilot                
from troy.pilot.compute_pilot_service          import ComputePilotService        
from troy.pilot.compute_unit_description       import ComputeUnitDescription     
from troy.pilot.compute_unit                   import ComputeUnit                 
from troy.pilot.compute_unit_service           import ComputeUnitService         

from troy.pilot.data_pilot_description         import DataPilotDescription       
from troy.pilot.data_pilot                     import DataPilot                   
from troy.pilot.data_pilot_service             import DataPilotService           
from troy.pilot.data_unit_description          import DataUnitDescription        
from troy.pilot.data_unit                      import DataUnit                    
from troy.pilot.data_unit_service              import DataUnitService            

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

