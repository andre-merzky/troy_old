
from compute_unit_service import iComputeUnitService
from data_unit_service    import iDataUnitService

from troy.interface.base  import iBase
from troy.pilot.exception import Exception, Error

########################################################################
#
#
#
class iComputeDataUnitService (iComputeUnitService, iDataUnitService) :

    """ ComputeDataUnitService.
    
        The ComputeDataUnitService is the application's interface to submit 
        ComputeDataUnits to the Pilot-Manager 
        in the P* Model.        
    """
   

    def __init__ (self, cdus_id = None):
        """ Create a Compute Data Unit Service object.

            Keyword arguments:
            cdus_id -- Reconnect to an existing CDUS (optional).
        """
        pass   

