
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

    def __init__ (self, obj, adaptor, dps_id=None):
        """ Create a DataPilotService object

            Keyword arguments:
            dps_id -- restore from dps_id
        """
        pass


    def create_pilot (self, rm, dpd, dp_type=None, context=None):
        """ Add a DataPilot to the DataPilotService

            Keyword arguments:
            rm      -- Contact string for the resource manager
            cpd     -- DataPilot Description
            dp_type -- backend type (optional)
            context -- Security context (optional)

            Return value:
            A DataPilot handle
        """
        raise TroyException (Error.NotImplemented, "method not implemented!")


    def list_pilots (self):
        """ List all DPs """
        raise TroyException (Error.NotImplemented, "method not implemented!")


    def wait (self):
        """ Wait until DPS enters a final state """
        raise TroyException (Error.NotImplemented, "method not implemented!")


    def cancel (self):
        """ Cancel the DPS
            This also cancels all the DataPilots that were under control of this
            PDS.
        """
        raise TroyException (Error.NotImplemented, "method not implemented!")


