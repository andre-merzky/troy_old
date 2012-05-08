
from troy.interface.base  import iBase
from troy.pilot.exception import TroyException, Error
    
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


    def __init__ (self, obj, adaptor) :
        """ Create a ComputePilotService object"""
        pass



    ############################################################################
    #
    # Note that submit_compute_unit_ is not called directly by the CPS impl, but
    # instead by a scheduler class, for those implementation which don't provide
    # scheduling on CUS level.  It is thus a private call.
    #
    def submit_compute_unit_ (self, cud):
        """ Submit a CU to this ComputePilotService.
    
            Keyword argument:
            cud -- The ComputeUnitDescription from the application
    
            Return:
            ComputeUnit object
        """
        raise TroyException (Error.NotImplemented, "method not implemented!")



    def init (self) :
        """ dummy method to make sure the backend can initialize the object.
            This method should *not* be implemented in the adaptor!"""
        pass


    def get_id (self):        
        """ get instance id """
        raise TroyException (Error.NotImplemented, "method not implemented!")


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
        raise TroyException (Error.NotImplemented, "method not implemented!")


    def list_pilots (self):
        """ List all CPs """
        raise TroyException (Error.NotImplemented, "method not implemented!")


    def wait (self):
        """ Wait until CPS enters a final state """
        raise TroyException (Error.NotImplemented, "method not implemented!")


    def cancel (self):
        """ Cancel the CPS
            This also cancels all the ComputePilots that were under control of this
            CPS.
        """
        raise TroyException (Error.NotImplemented, "method not implemented!")


