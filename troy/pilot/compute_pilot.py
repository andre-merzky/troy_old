
from base               import Base
    
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


    def __init__ (self, cp_id=None, context=None) :
        """ Create a ComputePilot

            Keyword arguments:
            cp_id   -- restore from cp_id
            context -- Security context (optional)

            If a cp_id is specified, the implementation will attempt to
            reconnect to the CP instance referenced by the ID.  If that instance
            got reinitialized meanwhile, the implementation may attempt to
            connect to the reinitialized instance.  If that is not possible, or
            if the instance matching cp_id cannot be found for other reasons,
            a BadParameter exception is raised.

        """

        # init api base
        Base.__init__ (self)

        # prepare instance data
        idata = {
                  'id'        : cp_id,
                  'context'   : context,
                }
        self.set_idata_ (idata)

        # initialize adaptor class 
        self.engine_.call ('ComputePilot', 'init_', self)


    ############################################################################
    #
    # The submit_compute_unit's implementation tries to submit the CU via
    # the backend -- if that does not work, no scheduler can help anymore, so an
    # exception is raised (falls through really)
    #
    def submit_compute_unit (self, cud) :
        """ Submit a CU to this ComputePilot.

            Keyword argument:
            cud -- The ComputeUnitDescription from the application

            Return:
            ComputeUnit object

            A compute unit description is used to instantiate a cu on the
            resource managed by the pilot.  
            
            If the pilot's resource is not suitable to run the requested CU,
            a BadParameter exception is raised.  Not raising this exception is
            not a guarantee that the CU will in fact be (able to be) executed --
            in that case, the returned CU will later be moved to Failed state.
            
            On success, the returned CU is in Pending state (or moved into any
            state downstream from Pending).

            submit() will honor all attributes set on the cud.  Attributes which
            are not explicitly set are interpreted as having default values (see
            documentation of CUD), or, where default values are not specified,
            are ignored.

        """

        return self.engine_.call ('ComputePilot', 'submit_compute_unit', self, cud)



    def get_id (self) :
        """ get instance id 
        
        This call may return 'None' if the Pilot is not yet in Running state.

        The returned ID can be used to connect to the CP instance later on, for
        example from within a different application instance.  
        
        """
        return self.engine_.call ('ComputePilot', 'get_id', self)


    def wait (self) :
        """ Wait until CP enters a final state 

        It is not an error to call wait() in a final state -- the call simply
        returns immediately.
        
        """
        return self.engine_.call ('ComputePilot', 'wait', self)


    def cancel (self) :
        """ Move the pilot into Canceled state, releasing all resources.

        The will block until the pilot reaches Canceled state and resources have
        been released.  

        It is not an error to call the method in a final state -- it will simple
        return immediately.  The pilot's state will not be changed in that case
        though.
        
        """
        return self.engine_.call ('ComputePilot', 'cancel', self)


    def reinitialize (self, cpd) :
        """ Re-Initialize the ComputePilot to the (new) ComputePilotDescription.
        
            Keyword arguments:
            cpd -- A ComputePilotDescription

            The reinitialize method is intended to change the amount of
            resources available to a pilot, without changing the pilot's state
            otherwise.  The method can be called in any non-final state, and
            will automatically move the pilot to 'Pending' state (if
            successful).  If reinitialization fails (for example, because no
            suitable resources have been found), the pilot is moved to 'Failed'
            state.

            It is up to the backend is the pilot's ID changes during the call to
            reinitialize(), but the implementation SHOULD attempt to keep the ID
            constant.

            Any compute units running on the pilot remain running -- but the
            backend may achieve this by aborting the units, and resubmitting
            them to the re-initialized pilot.
        """
        return self.engine_.call ('ComputePilot', 'reinitialize', 
                                  self, cpd)


    def set_callback (self, member, cb) :
        """ Set a callback function for a member.

            Keyword arguments:
            member -- The member to set the callback for (state / state_detail / wall_time_left).
            cb     -- The callback object to call.

            Setting the callback does not guarantee that all changes of the
            watched member cause a callback invocation.  For example,
            wall_time_left will be a continuously changing member, but the
            callback may be invoked at regular or non-regular intervals.  The
            implementation will, however, invoke the callback on a best-effort
            basis.


            It is not an error to call this method if a callback is already
            registered -- the call will then replace the callback, and behave
            like::

                def set_callback (self, member, cb) :
                  
                  if self.has_callback () :
                      unset_callback  (member)

                  self.set_callback (member, cb)

        """
        return self.engine_.call ('ComputePilot', 'set_callback', 
                                        self, member, cb)

    def unset_callback (self, member) :
        """ Unset a callback function from a member

            Keyword arguments:
            member -- The member to unset the callback for (state / state_detail / wall_tim_left).

            A callback may still be invoked during the unset_call, but it is
            guaranteed that no invocation will happen after the call finishes.

            It is not an error to call this method if no callback is registered
            -- the call will simply return immediately.
        """
        return self.engine_.call ('ComputePilot', 'unset_callback', 
                                        self, member)
    

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

