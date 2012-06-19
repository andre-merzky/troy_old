
from base                    import Base
from compute_unit_service    import ComputeUnitService
from data_unit_service       import DataUnitService
from compute_data_scheduler  import _ComputeDataScheduler


########################################################################
#
#
#
class ComputeDataUnitService (ComputeUnitService, DataUnitService) :

    """ ComputeDataUnitService.
    
        The ComputeDataUnitService is the application's interface to submit 
        ComputeDataUnits to the Pilot-Manager 
        in the P* Model.        
    """
   

    def __init__ (self, cdus_id=None) :
        """ Create a ComputeDataUnitService object
    
            Keyword arguments:
            cdus_id -- Reconnect to an existing ComputeDataUnitService 
        """
        print "cdus: init"

        # init api base
        Base.__init__ (self)

        # prepare instance data
        idata = {
                  'id'        : cdus_id,
                  'scheduler' : _ComputeDataScheduler ('Random')
                }
        self.set_idata_ (idata)

        # initialize adaptor class 
        self.engine_.call ('ComputeDataUnitService', 'init_', self)

        pass



    ############################################################################
    #
    # The submit_compute_data_unit's implementation first tries to submit the 
    # CDU via the backend -- if that does not work, the call is handed of to a 
    # scheduler which may be able to handle it, somehow?
    #
    def submit_compute_data_unit (self, cdud) :
        """ Submit a CDU to this ComputeDataUnitService.

            Keyword argument:
            cdud -- The ComputeDataUnitDescription from the application

            Return:
            ComputeDataUnit object
        """

        try :
            return self.engine_.call ('ComputeDataUnitService',
                                            'submit_compute_data_unit', self, cdud)
        except :
            # internal scheduling did not work -- invoke the scheduler
            idata = self.get_idata_ ()
            cdu   = idata['scheduler'].schedule (self, cdud)
            return cdu


# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

