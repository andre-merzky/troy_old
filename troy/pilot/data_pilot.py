
from base            import Base
from data_scheduler  import _DataScheduler


########################################################################
# 
#
#
class DataPilot (Base) :

    """ DataPilot (PilotStore)

        This is the object that is returned by the DataPilotService when a 
        new DataPilot is created based on a DataPilotDescription.

        The DataPilot object can be used by the application to keep track 
        of DataPilots that are active.
        
        A DataPilot has state, can be queried, can be cancelled and 
        re-initialized.
    """

    # Class members
    __slots__ = (
        'id',           # Reference to this DP
        'state',        # State of the DataPilot
        'state_detail', # Backend specific state of the DataPilot

        'description',  # Description of DataPilot
        'service_url',  # DataPilotService URL

        'space_left'    # Remaining space allocation
    )


    def __init__ (self, dp_id=None) :
        """ Create a DataPilot

            Keyword arguments:
            dp_id -- restore from dp_id
        """

        # init api base
        Base.__init__ (self)

        # prepare instance data
        idata = {
                  'id'        : dp_id,
                  'scheduler' : _DataScheduler ('Random')
                }
        self.set_idata_ (idata)

        # initialize adaptor class 
        self.engine_.call ('DataPilot', 'init_', self)


    ############################################################################
    #
    def submit_data_unit (self, dud) :
        """ Submit a DU to this DataPilot.

            Keyword argument:
            dud -- The DataUnitDescription from the application

            Return:
            DataUnit object
        """

        return self.engine_.call ('DataPilot',
                                        'submit_data_unit', self, dud)




    def wait (self) :
        """ Wait until DP enters a final state """
        return self.engine_.call ('DataPilot', 'wait', self)


    def cancel (self) :
        """ Cancel DP """
        return self.engine_.call ('DataPilot', 'cancel', self)


    def reinitialize (self, dpd) :
        """ Re-Initialize the DataPilot to the (new) DataPilotDescription.
        
            Keyword arguments:
            dpd -- A DataPilotDescription
        """
        return self.engine_.call ('DataPilot', 'reinitialize', self, dpd)


    def set_callback (self, member, cb) :
        """ Set a callback function for a member.

            Keyword arguments:
            member -- The member to set the callback for (state / state_detail / size_left).
            cb     -- The callback object to call.
        """
        return self.engine_.call ('DataPilot', 'set_callback', 
                                        self, member, cb)

    def unset_callback (self, member) :
        """ Unset a callback function from a member

            Keyword arguments:
            member -- The member to unset the callback for (state / state_detail / sizeleft).
        """
        return self.engine_.call ('DataPilot', 'unset_callback', 
                                        self, member)


# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

