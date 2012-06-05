
from base            import Base
from data_scheduler  import _DataScheduler


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

        The DataUnitService is linked to a set of DataPilots for the actual 
        execution of the DataUnits.
    """

    # FIXME: why does it has a state attribute?  What semantics?
   
    # Class members
    __slots__ = (
        'id',           # Reference to this DUS
        'state',        # State of the DUS
        'state_detail', # backend specific state of the DUS
    )


    def __init__ (self, dus_id=None) :
        """ Create a DataUnitService object
    
            Keyword arguments:
            dus_id -- Reconnect to an existing DataUnitService 
        """
        # init api base
        Base.__init__ (self)

        # prepare instance data
        idata = {
                  'id'        : dus_id,
                  'scheduler' : _DataScheduler ('Random')
                }
        self.set_idata_ (idata)

        # initialize adaptor class 
        self.engine_.call ('DataUnitService', 'init_', self)

        pass




    ############################################################################
    #
    # The submit_data_unit's implementation first tries to submit the DU via
    # the backend -- if that does not work, the call is handed of to a scheduler
    # which may be able to submit to on of the DUS' DPSs instead.
    #
    def submit_data_unit (self, dud) :
        """ Submit a CU to this DataUnitService.

            Keyword argument:
            cud -- The DataUnitDescription from the application

            Return:
            DataUnit object
        """

        try :
            return self.engine_.call ('DataUnitService',
                                            'submit_data_unit', self, dud)
        except :
            # internal scheduling did not work -- invoke the scheduler
            idata = self.get_idata_ ()
            du = idata['scheduler'].schedule (self, dud)
            return du



    def add_data_pilot (self, dp) :
        """ Add a DataPilot 

            Keyword arguments:
            dp -- The DataPilot to which this DataUnitService will connect.
        """
        return self.engine_.call ('DataUnitService',
                                         'add_data_pilot', self, dp)


    def list_data_pilots (self) :
        """ List all DPs of DUS """
        return self.engine_.call ('DataUnitService',
                                         'list_data_pilots', self)
    

    def remove_data_pilot (self, dp) :
        # FIXME: dp: id or instance?
        """ Remove a DataPilotService 

            Note that it won't cancel the DataPilot, it will simply not receive
            DUs anymore.
            
            Keyword arguments:
            dp -- The DataPilot to remove 
        """
        return self.engine_.call ('DataUnitService',
                                         'remove_data_pilot', self, dp)
    
    
    def submit_data_unit (self, dud) :
        """ Submit a DU to this DataUnitService.

            Keyword argument:
            dud -- The DataUnitDescription from the application

            Return:
            DataUnit object
        """
        return self.engine_.call ('DataUnitService',
                                         'submit_data_unit', self, dud)


    def wait (self) :
        """ Wait until DUS enters a final state """
        return self.engine_.call ('DataUnitService', 'wait', self)

    
    def cancel (self) :
        """ Cancel the DUS.
            
            Cancelling the DUS also cancels all the DUs submitted to it.
        """
        return self.engine_.call ('DataUnitService', 'cancel', self)


# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

