
from base import Base


########################################################################
#
# DataUnitService
# 
class DataUnitService (Base) :

    """ DataUnitService (DUS)
    
        The DataUnitService is the application's interface to submit 
        DataUnits to the Pilot-Manager in the P* Model.

        It can provide the application with a list of DataUnits that are 
        managed by the Pilot-Manager.

        The DataUnitService is linked to a DataPilotService for the actual 
        execution of the DataUnits.
    """

    # FIXME: why is this stateful?
    # FIXME: A Pilot-Manager must thus handle multiple DUS?
   
    # Class members
    __slots__ = (
        'id',           # Reference to this DUS
        'state',        # State of the DUS
        'state_detail', # backend specific state of the DUS
    )


    def __init__ (self, dus_id=None):
        """ Create a DataUnitService object

            Keyword arguments:
            dus_id -- Reconnect to an existing DataUnitService 
        """
        # FIXME: what happens on None?  needs URL?
        pass


    def add_data_pilot_service (self, dps):
        """ Add a DataPilotService 

            Keyword arguments:
            dps -- The DataPilotService to which this DataUnitService will connect.
        """
        pass


    def list_data_pilot_services (self):
        """ List all DPSs of DUS """
        pass
    

    def remove_data_pilot_service (self, dps):
        """ Remove a DataPilotService 

            Note that it won't cancel the DataPilotService, it will just no
            longer be connected to this DUS.
            
            Keyword arguments:
            dps -- The DataPilotService to remove 
        """
        pass
    
    
    def submit_data_unit (self, dud):
        """ Submit a DU to this DataUnitService.

            Keyword argument:
            dud -- The DataUnitDescription from the application

            Return:
            DataUnit object
        """
        pass


    def wait (self):
        """ Wait until DUS enters a final state """
        pass

    
    def cancel (self):
        """ Cancel the DUS.
            
            Cancelling the DUS also cancels all the DUs submitted to it.
        """
        pass


