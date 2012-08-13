
########################################################################
#
#
#
class State ():
    """
    The State class is really an enum, or what python uses as an enum.  That
    enum describes the state model for various components of the P* model, and
    thus of the pilot API, and is exposed as property of the following classes::

        troy.pilot.compute_pilot
        troy.pilot.compute_unit
        troy.pilot.data_pilot
        troy.pilot.data_unit
        troy.pilot.compute_data_unit

    For example, an L{ComputePilot} instance is created via a creation request::

        cpd = troy.pilot.compute_pilot_description ()
        cps = troy.pilot.compute_pilot_service ()
        cp  = cps.create_compute_pilot (cpd)

    That compute pilot has, at this point, the state 'New', so the Troy
    implementation has accepted the creation request, but it was not necessarily
    passed on to a backend which actually instantiates a compute pilot on some
    resource.

    Once the request is passed on to the backend, and was accepted by it, the cp
    will have 'Pending' state.  That state will eventually transition to
    'Running', when the backend instantiated the compute pilot process/agent/...
    Resources are only consumed during the 'Running' state,

    There are three options to leave the 'Running' state: 'Done', as successful
    and planned end of operation of the instance; 'Failed', as premature or
    unexpected end of operation (e.g. due to an error condition); and
    'Canceled', as premature and expected end of operation, due to user request.

    Note that all stateful objects of the Pilot API will, additionally to the
    state enum, expose a 'state_detail' (string), which is, in general, the
    native backend state -- Troy does not assume any semantic meaning on
    state_detail values.

    Available states::

        - Unknown
          The state of the backend instance is not known.  Duh! 

        - New         
          The creation request was accepted, but did not yet reach the backend. 

        - Pending     
          The backend accepted a creation request, but did not yet enact it. 

        - Running     
          The backend instance is created and active. 

        - Done        
          The backend instance finished successfully. 

        - Canceled    
          The backend instance finished due to a user request. 

        - Failed      
          The backend instance finished on an error condition. 
    """

    Unknown  = "Unknown"
    New      = "New"
    Pending  = "Pending"
    Running  = "Running"
    Done     = "Done"
    Canceled = "Canceled"
    Failed   = "Failed"

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

