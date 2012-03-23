
from base          import Base
from compute_unit  import ComputeUnit
    
########################################################################
#
#  ComputeUnitService
# 
class ComputeUnitService (Base) :

    """  ComputeUnitService (CUS)
    
        The ComputeUnitService is the application's interface to submit 
        ComputeUnits to the Pilot-Manager in the P* Model.

        It can provide the application with a list of ComputeUnits that are 
        managed by the Pilot-Manager.

        The ComputeUnitService is linked to a ComputePilotService for the actual 
        execution of the ComputeUnits.
    """

    # FIXME: why is this stateful?
    # FIXME: A Pilot-Manager must thus handle multiple CUS?

    # Class members
    __slots__ = (
        'id',           # Reference to this CUS
        'state',        # State of the CUS
        'state_detail', # backend specific state of the CUS
    )


    def __init__ (self, cus_id=None):
        """ Create a ComputeUnitService object
    
            Keyword arguments:
            cus_id -- Reconnect to an existing ComputeUnitService 
        """
        # FIXME: what happens on None?  needs URL?
        print "cus: init"
        pass


    def add_compute_pilot_service (self, cps):
        """ Add a ComputePilotService to this WUS.

            Keyword arguments:
            cps -- The ComputePilot Service to which this ComputeUnitService will connect.
        """
        print "cus: add cps"
        pass


    def list_compute_pilot_services (self):
        """ List all CPSs of CUS """
        pass


    def remove_compute_pilot_service (self, cps):
        """ Remove a ComputePilotService 

            Note that it won't cancel the ComputePilotService, it will just no
            longer be connected to this CUS.

            Keyword arguments:
            cps -- The ComputePilotService to remove 
        """
        pass


    def submit_compute_unit (self, cud):
        """ Submit a CU to this ComputeUnitService.

            Keyword argument:
            cud -- The ComputeUnitDescription from the application

            Return:
            ComputeUnit object
        """
        print "cus: submit cu"
        return ComputeUnit()
        pass


    def wait (self):
        """ Wait until CUS enters a final state """
        pass


    def cancel (self):
        """ Cancel the WUS.
            
            Cancelling the WUS also cancels all the WUs submitted to it.
        """
        pass


