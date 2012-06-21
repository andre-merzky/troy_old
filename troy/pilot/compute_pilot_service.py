
from base               import Base
from state              import State
from compute_pilot      import ComputePilot
    
########################################################################
#
#  ComputePilotService (CPS)
#
class ComputePilotService (Base) :

    """  ComputePilotService (CPS)

        The ComputePilotService is a factory for ComputePilots.  
        
        A CPS instance represents a specific resource or set of resources,
        identified by the ctor's rm url parameter.  The CPS can be asked to
        instantiate a CP, according to a CP description.  A CPS can also be
        asked to list (the IDs) of pilots on its (set of) resources.  Finally,
        the CPS can reconnect to a pilot on these resources.
        
    """

    # FIXME: it should be names factory
    # FIXME: mirror the API on DPS

    # Class members


    def __init__ (self, rm="") :
        """ Create a ComputePilotService object
        """

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

            A compute pilot description is used to instantiate a CP on the
            CPS's resources.
            
            If those resources are not suitable to run the requested CP,
            a BadParameter exception is raised.  Not raising this exception is
            not a guarantee that the CP will in fact be (able to be) executed --
            in that case, the returned CP will be moved to Failed state.
            
            On success, the returned CP is in Pending state (or moved into any
            state downstream from Pending).

            create_pilot will honor all attributes set on the CPD.  Attributes which
            are not explicitly set are interpreted as having default values (see
            documentation of CPD), or, where default values are not specified,
            are ignored.

        """
        return self.engine_.call ('ComputePilotService', 'create_pilot', 
                                  self, cpd, context)


    def list_pilots (self, context=None) :
        """ list known ComputePilots.

            Keyword arguments:
            context -- Security context (optional)

            Return value:
            A list of ComputePilot IDs

            The returned list can include pilots which have not been created by
            this CPS instance, but also may be incomplete, and not include
            pilots created by the CPS.  There is no guarantee that pilots in the
            returned list can in fact be reconnected to.  Also, an inclusion in
            the list does not have any indication about the respective pilot's
            state.

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

            The call behaves identically to::

              cp = troy.pilot.ComputePilot (id, context)

        """
        return self.engine_.call ('ComputePilotService', 'get_pilot', 
                                         self, cp_id, context)

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

