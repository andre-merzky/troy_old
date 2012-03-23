
import troy
import troy.interface


########################################################################
#
#
#
class adaptor (troy.interface.aBase) :
    
    def __init__ (self):
        
        print 'adaptor: bigjob: init'
        
        # registry maps api classes to adaptor classes implementing the
        # respective class interface.
        self.name     = 'troy_adaptor_bigjob'
        self.registry = {'ComputePilotService'       : 'bj_cps' ,
                         'ComputePilot'              : 'bj_cp'  ,
                         'ComputeUnitService'        : 'bj_cus' ,
                         'ComputeUnit'               : 'bj_cu'  , 

                         'DataPilotService'          : 'bj_dps' ,
                         'DataPilot'                 : 'bj_dp'  ,
                         'DataUnitService'           : 'bj_dus' ,
                         'DataUnit'                  : 'bj_du'  , 

                         'ComputeDataUnitService'    : 'bj_cdus',
                         'ComputeDataUnit'           : 'bj_cdu' }

    def get_name (self):
        return self.name

    def get_registry (self):
        return self.registry

    def sanity_check (self):
        # version checks etc.
        return True


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# Compute API
#

########################################################################
class bj_cps (troy.interface.iComputePilotService) :

    def __init__ (self) :
        print "bj_cps:init"


    def check (self, cps, a1, a2, a3) :
        print "bj_cps: check : " + str(a1) + ", " + str(a2) + ", " + str(a3)

        # raise troy.pilot.Exception (troy.pilot.Error.NoSuccess, "oops")

        return "hello world"


########################################################################
class bj_cp (troy.interface.iComputePilot) :

    def __init__ (self) :
        print "bj_cp:init"


########################################################################
class bj_cus (troy.interface.iComputeUnitService) :

    def __init__ (self) :
        print "bj_cus:init"


########################################################################
class bj_cu (troy.interface.iComputeUnit) :

    def __init__ (self) :
        print "bj_cu:init"





#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# Data API
#

########################################################################
class bj_dps (troy.interface.iDataPilotService) :

    def __init__ (self) :
        print "bj_dps:init"


########################################################################
class bj_dp (troy.interface.iDataPilot) :

    def __init__ (self) :
        print "bj_dp:init"


########################################################################
class bj_dus (troy.interface.iDataUnitService) :

    def __init__ (self) :
        print "bj_dus:init"


########################################################################
class bj_du (troy.interface.iDataUnit) :

    def __init__ (self) :
        print "bj_du:init"



#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# Compute-Data API
#

########################################################################
class bj_dcus (troy.interface.iComputeDataUnitService) :

    def __init__ (self) :
        print "bj_dcus:init"


########################################################################
class bj_dcu (troy.interface.iComputeDataUnit) :

    def __init__ (self) :
        print "bj_dcu:init"


