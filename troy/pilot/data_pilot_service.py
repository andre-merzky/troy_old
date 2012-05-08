
from base import Base


########################################################################
#
#  DataPilotService (DPS)
#
class DataPilotService (Base) :

    """ DataPilotService (DPS)

        The DataPilotService is responsible for creating and managing 
        the DataPilots.

        It is the application's interface to the Pilot-Manager in the 
        P* Model.
    """

    # FIXME: why is this stateful?

    # Class members
    __slots__ = (
        'id',           # Reference to this DPS
        'state',        # State of the DPS
        'state_detail', # Backend specific state of the DPS
    )


    def __init__ (self, dps_id=None):
        """ Create a DataPilotService object

            Keyword arguments:
            dps_id -- restore from dps_id
        """
        # FIXME: what happens on None?  needs URL?
        Base.__init__ (self)
        pass


    def create_pilot (self, rm, dpd, dp_type=None, context=None):
        """ Add a DataPilot to the DataPilotService

            Keyword arguments:
            rm      -- Contact string for the resource manager
            cpd     -- DataPilot Description
            dp_type -- backend type (optional)
            context -- Security context (optional)

            Return value:
            A DataPilot handle
        """
        return self.get_engine_().call ('DataPilotService', 'create_pilot', 
                                        self, rm, dpd, dp_type, context)


    def list_pilots (self):
        """ List all DPs """
        return self.get_engine_().call ('DataPilotService', 'list_pilots', self)


    def wait (self):
        """ Wait until DPS enters a final state """
        # FIXME
        return self.get_engine_().call ('DataPilotService', 'wait', self)


    def cancel (self):
        """ Cancel the DPS
            This also cancels all the DataPilots that were under control of this
            PDS.
        """
        # FIXME
        return self.get_engine_().call ('DataPilotService', 'cancel', self)


# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

