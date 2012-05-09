
from troy.interface.base  import iBase
from troy.pilot.exception import TroyException, Error
    
########################################################################
#
#  ComputeUnitService
# 
class iComputeUnitService (iBase) :

    """  ComputeUnitService (CUS)
    
        The ComputeUnitService is the application's interface to submit 
        ComputeUnits to the Pilot-Manager in the P* Model.

        It can provide the application with a list of ComputeUnits that are 
        managed by the Pilot-Manager.

        The ComputeUnitService is linked to a ComputePilotService for the actual 
        execution of the ComputeUnits.
    """

    def __init__ (self, obj, adaptor):
        """ Create a ComputeUnitService object
        """
        pass


    def init (self):
        """ dummy method to make sure the backend can initialize the object
        """
        pass


    def add_compute_pilot_service (self, cps):
        """ Add a ComputePilotService to this WUS.

            Keyword arguments:
            cps -- The ComputePilot Service to which this ComputeUnitService will connect.
        """
        raise TroyException (Error.NotImplemented, "method not implemented!")


    def list_compute_pilot_services (self):
        """ List all CPSs of CUS """
        raise TroyException (Error.NotImplemented, "method not implemented!")


    def remove_compute_pilot_service (self, cps):
        """ Remove a ComputePilotService 

            Note that it won't cancel the ComputePilotService, it will just no
            longer be connected to this CUS.

            Keyword arguments:
            cps -- The ComputePilotService to remove 
        """
        raise TroyException (Error.NotImplemented, "method not implemented!")


    ############################################################################
    #
    # Note that submit_compute_unit *is* called directly by the CUS impl, in
    # case the backend provides CUS level scheduling.  If not, then this call
    # will raise an exception, and the scheduler class will take over
    #
    def submit_compute_unit (self, cud):
        """ Submit a CU to this ComputeUnitService.
    
            Keyword argument:
            cud -- The ComputeUnitDescription from the application
    
            Return:
            ComputeUnit object
        """
        raise TroyException (Error.NotImplemented, "method not implemented!")



    def get_id (self):        
        """ get instance id """
        raise TroyException (Error.NotImplemented, "method not implemented!")


    def wait (self):
        """ Wait until CUS enters a final state """
        raise TroyException (Error.NotImplemented, "method not implemented!")


    def cancel (self):
        """ Cancel the WUS.
            
            Cancelling the WUS also cancels all the WUs submitted to it.
        """
        raise TroyException (Error.NotImplemented, "method not implemented!")


