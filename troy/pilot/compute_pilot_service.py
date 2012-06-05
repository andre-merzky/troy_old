
from base               import Base
from state              import State
from compute_pilot      import ComputePilot
    
########################################################################
#
#  ComputePilotService (CPS)
#
class ComputePilotService (Base) :

    """  ComputePilotService (CPS)

        The ComputePilotService is in fact a factory for ComputePilots.
    """

    # FIXME: it should be names factory
    # FIXME: mirror the API on DPS

    # Class members


    def __init__ (self, rm="") :
        """ Create a ComputePilotService object
        """

        # FIXME: should we in fact allow ctor w/o rm?

        print "cps: init " + rm

        # init api base
        Base.__init__ (self)

        # prepare instance data
        idata = { 'rm' : rm } 
        self.set_idata_ (idata)

        # initialize adaptor class 
        self.engine_.call ('ComputePilotService', 'init_', self)


    def create_pilot (self, cpd, context=None) :
        """ Create a ComputePilot.

            Keyword arguments:
            cpd     -- ComputePilot Description
            context -- Security context (optional)

            Return value:
            A ComputePilot handle
        """
        return self.engine_.call ('ComputePilotService', 'create_pilot', 
                                         self, cpd, context)


    def list_pilots (self, context=None) :
        """ list known ComputePilots.

            Keyword arguments:
            context -- Security context (optional)

            Return value:
            A list of ComputePilot IDs
        """
        return self.engine_.call ('ComputePilotService', 'list_pilots', 
                                         self, context)


    def get_pilot (self, cp_id, context=None) :
        """ Reconnect to a ComputePilot.

            Keyword arguments:
            cp_id   -- ComputePilot's id
            context -- Security context (optional)

            Return value:
            A ComputePilot handle
        """
        return self.engine_.call ('ComputePilotService', 'get_pilot', 
                                         self, cp_id, context)

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

