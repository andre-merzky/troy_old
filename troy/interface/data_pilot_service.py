
from troy.interface.base  import iBase
from troy.pilot.exception import Exception, Error


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

    def __init__ (self, dps_id=None):
        """ Create a DataPilotService object

            Keyword arguments:
            dps_id -- restore from dps_id
        """
        pass


    def create_pilot (self, obj, rm, dpd, dp_type=None, context=None):
        """ Add a DataPilot to the DataPilotService

            Keyword arguments:
            rm      -- Contact string for the resource manager
            cpd     -- DataPilot Description
            dp_type -- backend type (optional)
            context -- Security context (optional)

            Return value:
            A DataPilot handle
        """
        raise Exception (Error.NotImplemented, "method not implemented!")


    def list_pilots (self, obj):
        """ List all DPs """
        raise Exception (Error.NotImplemented, "method not implemented!")


    def wait (self, obj):
        """ Wait until DPS enters a final state """
        raise Exception (Error.NotImplemented, "method not implemented!")


    def cancel (self, obj):
        """ Cancel the DPS
            This also cancels all the DataPilots that were under control of this
            PDS.
        """
        raise Exception (Error.NotImplemented, "method not implemented!")


