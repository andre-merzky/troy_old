
from base          import Base
from state         import State
from compute_pilot import ComputePilot
    
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
        # FIXME: what happens on None?  needs URL?
        print "cps: init"
        Base.__init__ (self)
        idata = {
                  'id'            : '',          # no id, yet
                  'state'         : State.New,   # state of backend instance
                  'state_detail'  : '',          # Backend specific state of the CPS
                }
        self.set_idata_ ('api', idata)
        pass


    def check (self, one, two, three):
        return self.get_engine_().call ('ComputePilotService', 'check', self, one, two, three)


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
        return ComputePilot()
        pass


    def list_pilots (self):
        """ List all CPs """
        return self.get_engine_().call ('ComputePilotService', 'list_pilots', self)
        pass


    def wait (self):
        """ Wait until CPS enters a final state """
        # FIXME
        pass


    def cancel (self):
        """ Cancel the CPS
            This also cancels all the ComputePilots that were under control of this
            CPS.
        """
        # FIXME
        pass


