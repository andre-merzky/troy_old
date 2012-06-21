
from base            import Base


########################################################################
#
#  DataPilotService (DPS)
#
class DataPilotService (Base) :

    """ DataPilotService (DPS)

        The DataPilotService is in fact a factory for DataPilots.
    """

    # FIXME: it should be named factory

    def __init__ (self) :
        """ Create a DataPilotService object """

        # init api base
        Base.__init__ (self)

        # initialize adaptor class 
        self.engine_.call ('DataPilotService', 'init_', self)



    def create_pilot (self, dpd, context=None) :
        """ Create a DataPilot.

            Keyword arguments:
            cpd     -- DataPilot Description
            context -- Security context (optional)

            Return value:
            A DataPilot handle
        """
        return self.engine_.call ('DataPilotService', 'create_pilot', 
                                        self, dpd, context)


# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

