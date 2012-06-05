
from troy.interface.base  import iBase
from troy.pilot.exception import TroyException, Error
    
########################################################################
#
#  ComputePilotService (CPS)
#
class iComputePilotService (iBase) :

    """  ComputePilotService (CPS)

        The ComputePilotService is in fact a factory for ComputePilots.
    """


    def __init__ (self, obj, adaptor) :
        """ Create a ComputePilotService object"""
        pass



    def create_pilot (self, cpd, context=None) :
        """ Create a ComputePilot

            Keyword arguments:
            cpd     -- ComputePilot Description
            context -- Security context (optional)

            Return value:
            A ComputePilot handle
        """
        raise TroyException (Error.NotImplemented, "method not implemented!")

