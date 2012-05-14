
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

    # Class members


    def __init__ (self):
        """ Create a ComputePilotService object
        """

        print "cps: init"

        # init api base
        Base.__init__ (self)

        # prepare instance data
        idata = { }
        self.set_idata_ (idata)

        # initialize adaptor class 
        self.get_engine_().call ('ComputePilotService', 'init', self)


    def create_pilot (self, cpd, context=None):
        """ Create a ComputePilot.

            Keyword arguments:
            cpd     -- ComputePilot Description
            context -- Security context (optional)

            Return value:
            A ComputePilot handle
        """
        return self.get_engine_().call ('ComputePilotService', 'create_pilot', 
                                         self, cpd, context)

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

