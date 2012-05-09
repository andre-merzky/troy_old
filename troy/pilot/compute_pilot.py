
from base               import Base
from compute_scheduler  import _ComputeScheduler
    
########################################################################
#
#
#
class ComputePilot (Base) :

    """ ComputePilot (PilotJob)
    
        This is the object that is returned by the ComputePilotService when a 
        new ComputePilot is created based on a ComputePilotDescription.

        The ComputePilot object can be used by the application to keep track 
        of ComputePilots that are active.
        
        A ComputePilot has state, can be queried, can be cancelled and be 
        re-initialized.
    """

    # Class members
    __slots__ = (
        'id',             # Reference to this CP
        'state',          # State of the ComputePilot
        'state_detail',   # Backend specific state of the ComputePilot

        'description',    # Description of ComputePilot
        'service_url',    # ComputePilotService URL

        'wall_time_left'  # Remaining time allocation
    )


    def __init__ (self, cp_id=None):
        """ Create a ComputePilot

            Keyword arguments:
            cp_id -- restore from cp_id
        """

        # init api base
        Base.__init__ (self)

        # prepare instance data
        idata = {
                  'id'        : cp_id,
                  'scheduler' : _ComputeScheduler ('Random')
                }
        self.set_idata_ (idata)

        # initialize adaptor class 
        self.get_engine_().call ('ComputePilot', 'init', self)


    ############################################################################
    #
    # The submit_compute_unit's implementation tries to submit the CU via
    # the backend -- if that does not work, no scheduler can help anymore, so an
    # exception is raised (falls through really)
    #
    # This is a private method
    #
    def submit_compute_unit_ (self, cud):
        """ Submit a CU to this ComputePilot.

            Keyword argument:
            cud -- The ComputeUnitDescription from the application

            Return:
            ComputeUnit object
        """

        return self.get_engine_().call ('ComputePilot',
                                        'submit_compute_unit_', self, cud)



    def get_id (self):
        """ get instance id """
        return self.get_engine_().call ('ComputePilot', 'get_id', self)


    def wait (self):
        """ Wait until CP enters a final state """
        return self.get_engine_().call ('ComputePilot', 'wait', self)


    def cancel (self):        
        """ Remove the ComputePilot from the ComputePilot Service. """
        return self.get_engine_().call ('ComputePilot', 'cancel', self)


    def reinitialize (self, cpd):        
        """ Re-Initialize the ComputePilot to the (new) ComputePilotDescription.
        
            Keyword arguments:
            cpd -- A ComputePilotDescription
        """
        return self.get_engine_().call ('ComputePilot', 'reinitialize', 
                                        self, cpd)


    def set_callback (self, member, cb):
        """ Set a callback function for a member.

            Keyword arguments:
            member -- The member to set the callback for (state / state_detail / wall_time_left).
            cb     -- The callback object to call.
        """
        return self.get_engine_().call ('ComputePilot', 'set_callback', 
                                        self, member, cb)

    def unset_callback (self, member):
        """ Unset a callback function from a member

            Keyword arguments:
            member -- The member to unset the callback for (state / state_detail / wall_tim_left).
        """
        return self.get_engine_().call ('ComputePilot', 'unset_callback', 
                                        self, member)
    

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

