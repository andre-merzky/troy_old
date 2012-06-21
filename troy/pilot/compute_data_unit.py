
from compute_unit import ComputeUnit
from data_unit    import DataUnit


########################################################################
#
#
#
class ComputeDataUnit (ComputeUnit, DataUnit) :

    """ ComputeDataUnit.
    
        The ComputeDataUnit is a handle to a unit of (sompute and/or data)
        workload.
    """
   

    def __init__ (self, cdu_id=None) :
        """ Create a Compute Data Unit  object.

            Keyword arguments:
            cdu_id -- Reconnect to an existing CDU (optional).
        """
        pass   


# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

