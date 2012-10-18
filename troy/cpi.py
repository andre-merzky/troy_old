""" 

This module contains the CPI for the TROY PilotJob Framework.
It needs to be implemented by PilotJob backends.

"""

#
# TROY CPI Adaptor
#
class TroyAdaptor(object):

    def __init__(self):
        raise NotImplementedError

    def start_pilotjob(self, rm, pj_desc, context=None):
        """ Request a new pilot job from the adaptor """
        raise NotImplementedError

    def cancel_pilotjob(self):
        """ Cancel the pilot job that is managed by this adaptor. """
        raise NotImplementedError

    def reconfigure_pilotjob(self, pilotjob):
        """ Reconfigure an already started pilot job. """
        raise NotImplementedError

    def submit_schedunit(self, wu):
        """ Submit a scheduling unit to this pilot job. """
        raise NotImplementedError

    def cancel_schedunit(self, wu):
        """ Cancel a scheduling unit that was submitted to this pilot job. """
        raise NotImplementedError

    def list_workunits(self):
        """ List the scheduling units that are submitted to this pilot job. """
        raise NotImplementedError
    
    def set_pilotjob_callback(self, member, cb):
        """ Set a callback to a member of the pilot job. """
        raise NotImplementedError

    def unset_pilotjob_callback(self, member):
        """ Unset a callback from a member of the pilot job. """
        raise NotImplementedError

    def set_schedunit_callback(self, wu, member, cb):
        """ Set a callback to a member of a scheduling unit. """ 
        raise NotImplementedError

    def unset_schedunit_callback(self, wu, member):
        """ Unset a callback from a member of a scheduling unit. """ 
        raise NotImplementedError
