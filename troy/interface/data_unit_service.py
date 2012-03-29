
from troy.interface.base  import iBase
from troy.pilot.exception import TroyException, Error


########################################################################
#
# DataUnitService
# 
class iDataUnitService (iBase) :

    """ DataUnitService (DUS)
    
        The DataUnitService is the application's interface to submit 
        DataUnits to the Pilot-Manager in the P* Model.

        It can provide the application with a list of DataUnits that are 
        managed by the Pilot-Manager.

        The DataUnitService is linked to a DataPilotService for the actual 
        execution of the DataUnits.
    """

    def __init__ (self, obj, adaptor, dus_id=None):
        """ Create a DataUnitService object

            Keyword arguments:
            dus_id -- Reconnect to an existing DataUnitService 
        """
        pass


    def add_data_pilot_service (self, dps):
        """ Add a DataPilotService 

            Keyword arguments:
            dps -- The DataPilotService to which this DataUnitService will connect.
        """
        raise TroyException (Error.NotImplemented, "method not implemented!")


    def list_data_pilot_services (self):
        """ List all DPSs of DUS """
        raise TroyException (Error.NotImplemented, "method not implemented!")
    

    def remove_data_pilot_service (self, dps):
        """ Remove a DataPilotService 

            Note that it won't cancel the DataPilotService, it will just no
            longer be connected to this DUS.
            
            Keyword arguments:
            dps -- The DataPilotService to remove 
        """
        raise TroyException (Error.NotImplemented, "method not implemented!")
    
    
    def submit_data_unit (self, dud):
        """ Submit a DU to this DataUnitService.

            Keyword argument:
            dud -- The DataUnitDescription from the application

            Return:
            DataUnit object
        """
        raise TroyException (Error.NotImplemented, "method not implemented!")


    def wait (self):
        """ Wait until DUS enters a final state """
        raise TroyException (Error.NotImplemented, "method not implemented!")

    
    def cancel (self):
        """ Cancel the DUS.
            
            Cancelling the DUS also cancels all the DUs submitted to it.
        """
        raise TroyException (Error.NotImplemented, "method not implemented!")


