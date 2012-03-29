
from troy.interface.compute_unit import iComputeUnit
from troy.interface.data_unit    import iDataUnit

from troy.interface.base         import iBase
from troy.pilot.exception        import TroyException, Error

########################################################################
#
#
#
class iComputeDataUnit (iComputeUnit, iDataUnit) :

    """ ComputeDataUnit.
    
        The ComputeDataUnit is the application's interface to submit 
        ComputeDataUnits to the Pilot-Manager 
        in the P* Model.        
    """
   

    def __init__ (self, cdu_id = None):
        """ Create a Compute Data Unit  object.

            Keyword arguments:
            cdu_id -- Reconnect to an existing CDU (optional).
        """
        pass   


