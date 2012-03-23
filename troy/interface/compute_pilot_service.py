
from troy.interface.base  import iBase
from troy.pilot.exception import Exception, Error
    
########################################################################
#
#  ComputePilotService (CPS)
#
class iComputePilotService (iBase) :

    """  ComputePilotService (CPS)

    
        The ComputePilotService is responsible for creating and managing 
        the ComputePilots.

        It is the application's interface to the Pilot-Manager in the 
        P* Model.
    """

    def __init__ (self, cds_id=None):
        """ Create a ComputePilotService object

            Keyword arguments:
            cps_id -- restore from cps_id
        """
        pass


    def check (self, one, two, three):
        raise Exception (Error.NotImplemented, "method not implemented!")


    def create_pilot (self, rm, cpd, cp_type=None, context=None):
        """ Add a ComputePilot to the ComputePilotService

            Keyword arguments:
            rm      -- Contact string for the resource manager
            cpd     -- ComputePilot Description
            cp_type -- backend type (optional)
            context -- Security context (optional)

            Return value:
            A ComputePilot handle
        """
        raise Exception (Error.NotImplemented, "method not implemented!")


    def list_pilots (self, api):
        """ List all CPs """
        raise Exception (Error.NotImplemented, "method not implemented!")


    def wait (self):
        """ Wait until CPS enters a final state """
        raise Exception (Error.NotImplemented, "method not implemented!")


    def cancel (self):
        """ Cancel the CPS
            This also cancels all the ComputePilots that were under control of this
            CPS.
        """
        raise Exception (Error.NotImplemented, "method not implemented!")


