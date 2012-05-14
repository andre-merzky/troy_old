
from base               import Base
from compute_unit       import ComputeUnit
from compute_scheduler  import _ComputeScheduler
    
########################################################################
#
#  ComputeUnitService
# 
class ComputeUnitService (Base) :

    """  ComputeUnitService (CUS)
    
        The ComputeUnitService is the application's interface to submit
        ComputeUnits to the Pilot-Manager in the P* Model.  It can provide the
        application with a list of ComputeUnits that are managed by the
        Pilot-Manager.

        The ComputeUnitService is linked to a set of ComputePilots for the actual 
        execution of the ComputeUnits.
    """

    # FIXME: why has this state?  What state semantics?
    # FIXME: add list_compute_units()

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
        print "cus: init"

        # init api base
        Base.__init__ (self)

        # prepare instance data
        idata = {
                  'id'        : cus_id,
                  'scheduler' : _ComputeScheduler ('Random')
                }
        self.set_idata_ (idata)

        # initialize adaptor class 
        self.get_engine_().call ('ComputeUnitService', 'init', self)

        pass


    ############################################################################
    #
    # The submit_compute_unit's implementation first tries to submit the CU via
    # the backend -- if that does not work, the call is handed of to a scheduler
    # which may be able to submit to on of the CUS' CPSs instead.
    #
    def submit_compute_unit (self, cud):
        """ Submit a CU to this ComputeUnitService.

            Keyword argument:
            cud -- The ComputeUnitDescription from the application

            Return:
            ComputeUnit object
        """

        try :
            return self.get_engine_().call ('ComputeUnitService',
                                            'submit_compute_unit', self, cud)
        except :
            # internal scheduling did not work -- invoke the scheduler
            idata = self.get_idata_ ()
            cu = idata['scheduler'].schedule (self, cud)
            return cu



    def get_id (self):
        """ get instance id """
        return self.get_engine_().call ('ComputeUnitService', 'get_id', self)


    def add_compute_pilot (self, cp):
        """ Add a ComputePilot to this CUS.

            Keyword arguments:
            cp -- The ComputePilot which this ComputeUnitService will utilize.
        """
        return self.get_engine_().call ('ComputeUnitService',
                                        'add_compute_pilot', self, cp)


    def list_compute_pilots (self):
        """ List all CPs of CUS """
        return self.get_engine_().call ('ComputeUnitService', 
                                        'list_compute_pilots', self)


    def remove_compute_pilots (self, cps):
        """ Remove a ComputePilot

            Note that it won't cancel the ComputePilot, it will just no
            longer receive new CUs.

            Keyword arguments:
            cp -- The ComputePilot to remove 
        """
        return self.get_engine_().call ('ComputeUnitService',
                                        'remove_compute_pilot', self, cp)


    def wait (self):
        """ Wait until CUS enters a final state """
        return self.get_engine_().call ('ComputeUnitService', 'wait', self)


    def cancel (self):
        """ Cancel the CUS.
            
            Cancelling the CUS also cancels all the CUS submitted to it.
        """
        return self.get_engine_().call ('ComputeUnitService', 'cancel', self)


# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

