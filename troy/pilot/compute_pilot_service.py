
from base               import Base
from state              import State
from compute_pilot      import ComputePilot
from compute_scheduler  import _ComputeScheduler
    
########################################################################
#
#  ComputePilotService (CPS)
#
class ComputePilotService (Base) :

    """  ComputePilotService (CPS)

    
        The ComputePilotService is responsible for creating and managing 
        the ComputePilots.

        It is the application's interface to the Pilot-Manager in the 
        P* Model.
    """

    # FIXME: why is this stateful?

    # Class members


    def __init__ (self, cds_id=None):
        """ Create a ComputePilotService object

            Keyword arguments:
            cps_id -- restore from cps_id
        """

        print "cps: init"

        # init api base
        Base.__init__ (self)

        # prepare instance data
        idata = {
                  'id'        : cds_id,
                  'scheduler' : _ComputeScheduler ('Random')
                }
        self.set_idata_ (idata)

        # initialize adaptor class 
        self.get_engine_().call ('ComputePilotService', 'init', self)



    ############################################################################
    #
    # The submit_compute_unit's implementation first tries to submit the CU via
    # the backend -- if that does not work, the call is handed of to a scheduler
    # which may be able to submit to on of the CPS' CPs instead.
    #
    # This is a private method
    #
    def submit_compute_unit_ (self, cud):
        """ Submit a CU to this ComputePilotService.

            Keyword argument:
            cud -- The ComputeUnitDescription from the application

            Return:
            ComputeUnit object
        """

        try :
            return self.get_engine_().call ('ComputePilotService',
                                            'submit_compute_unit_', self, cud)
        except :
            # internal scheduling did not work -- invoke the scheduler
            idata = self.get_idata_ ()
            cu = idata['scheduler'].schedule (self, cud)
            return cu



    def get_id (self):
        """ get instance id """
        return self.get_engine_().call ('ComputePilotService', 'get_id', self)


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
        print "cps: create pilot"
        return self.get_engine_().call ('ComputePilotService', 'create_pilot', 
                                         self, rm, cpd, cp_type, context)


    def list_pilots (self):
        """ List all CPs """
        return self.get_engine_().call ('ComputePilotService', 'list_pilots', self)


    def wait (self):
        """ Wait until CPS enters a final state """
        return self.get_engine_().call ('ComputePilotService', 'wait', self)


    def cancel (self):
        """ Cancel the CPS
            This also cancels all the ComputePilots that were under control of this
            CPS.
        """
        return self.get_engine_().call ('ComputePilotService', 'cancel', self)


# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

