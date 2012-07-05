
from troy.interface.base  import iBase
from troy.pilot.exception import TroyException, Error


########################################################################
#
#  DataPilotService (DPS)
#
class iDataPilotService (iBase) :

    """ DataPilotService (DPS)

        The DataPilotService is responsible for creating and managing 
        the DataPilots.

        It is the application's interface to the Pilot-Manager in the 
        P* Model.
    """

    def __init__ (self, obj, adaptor) :
        """ Create a DataPilotService object

            Keyword arguments:
            dps_id -- restore from dps_id
        """
        pass


    def create_pilot (self, dpd) :
        """ Create a DataPilot.

            Keyword arguments:
            cpd     -- DataPilot Description

            Return value:
            A DataPilot handle
        """
        raise TroyException (Error.NotImplemented, "method not implemented!")

