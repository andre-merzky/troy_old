
from compute_unit_service import ComputeUnitService
from data_unit_service    import DataUnitService


########################################################################
#
#
#
class ComputeDataUnitService (ComputeUnitService, DataUnitService) :

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

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

