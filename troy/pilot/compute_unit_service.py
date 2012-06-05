
from base               import Base
from compute_unit       import ComputeUnit
    
########################################################################
#
#  ComputeUnitService
# 
class ComputeUnitService (Base) :

    """  ComputeUnitService (CUS)
    
        The ComputeUnitService is the application's interface to submit
        ComputeUnits to the Pilot-Manager in the P* Model.  It can provide the
        application with a list of ComputeUnits that are managed by the
        Pilot-Manager.

        The ComputeUnitService is linked to a set of ComputePilots for the actual 
        execution of the ComputeUnits.
    """

    # FIXME: add list_compute_units ()

    # Class members
    __slots__ = (
        'id' # Reference to this CUS
    )


    def __init__ (self, cus_id=None) :
        """ Create a ComputeUnitService object
    
            Keyword arguments:
            cus_id -- Reconnect to an existing ComputeUnitService 
        """
        print "cus: init"

        # init api base
        Base.__init__ (self)

        # prepare instance data
        # FIXME: the scheduler type to be used is hard coded.  IMHO, that should
        # be variable via the API.
        idata = {
                  'id'        : cus_id,
                  'pilots'    : [],
                  'scheduler' : 'Random'
                }
        self.set_idata_ (idata)

        # initialize adaptor class 
        self.engine_.call ('ComputeUnitService', 'init_', self)

        pass


    def submit_compute_unit (self, cud) :
        """ Submit a CU to this ComputeUnitService.

            Keyword argument:
            cud -- The ComputeUnitDescription from the application

            Return:
            ComputeUnit object
        """

        return self.engine_.call ('ComputeUnitService', 
                'submit_compute_unit', self, cud)


    def get_id (self) :
        """ get instance id """
        return self.engine_.call ('ComputeUnitService', 'get_id', self)


    def add_compute_pilot (self, cp) :
        """ Add a ComputePilot to this CUS.

            Keyword arguments:
            cp -- The ComputePilot which this ComputeUnitService will utilize.
        """
        return self.engine_.call ('ComputeUnitService',
                                        'add_compute_pilot', self, cp)


    def list_compute_pilots (self) :
        """ List all CPs of CUS """
        return self.engine_.call ('ComputeUnitService', 
                                        'list_compute_pilots', self)


    def remove_compute_pilots (self, cps) :
        """ Remove a ComputePilot

            Note that it won't cancel the ComputePilot, it will just no
            longer receive new CUs.

            Keyword arguments:
            cp -- The ComputePilot to remove 
        """
        return self.engine_.call ('ComputeUnitService',
                                        'remove_compute_pilot', self, cp)


# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

