
from base            import Base
from data_scheduler  import _DataScheduler


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

        print "dps: init"

        # init api base
        Base.__init__ (self)

        # prepare instance data
        idata = {
                  'id'        : dps_id,
                  'scheduler' : _DataScheduler ('Random')
                }
        self.set_idata_ (idata)

        # initialize adaptor class 
        self.get_engine_().call ('DataPilotService', 'init', self)



    ############################################################################
    #
    # The submit_data_unit's implementation first tries to submit the DU via
    # the backend -- if that does not work, the call is handed of to a scheduler
    # which may be able to submit to on of the DPS' DPs instead.
    #
    # This is a private method
    #
    def submit_data_unit_ (self, dud):
        """ Submit a DU to this DataPilotService.

            Keyword argument:
            dud -- The DataUnitDescription from the application

            Return:
            ComputeUnit object
        """

        try :
            return self.get_engine_().call ('DataPilotService',
                                            'submit_data_unit_', self, dud)
        except :
            # internal scheduling did not work -- invoke the scheduler
            idata = self.get_idata_ ()
            du = idata['scheduler'].schedule (self, dud)
            return du



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

