
import imp

import troy
import troy.interface
from troy.pilot.exception import TroyException, Error


########################################################################
# 
# FIXME:
#
#   In order to write a functional adaptor, do the following:
#
#   - copy this file to a new location
#   - rename it to 'troy_adaptor_<backend>.py', where <backend> is 
#     the name of your pilot implementation
#   - implement the adaptor.sanity_check() method (check if the adaptor is
#     viable in the given runtime environment)
#   - in the new adaptor, replace all occurrences of 'bigjob' with <backend>
#   - implement all classes/methods
#


########################################################################
#
# main adaptor class, registers the implementation with troy upon loading
#
class adaptor (troy.interface.aBase) :
    
    def __init__ (self) :
        
        # duh!
        self.name     = 'troy_adaptor_bigjob'

        # registry maps api classes to adaptor classes implementing the
        # respective class interface.
        self.registry = {'ComputePilotService'       : 'bigjob_cps' ,
                         'ComputePilot'              : 'bigjob_cp'  ,
                         'ComputeUnitService'        : 'bigjob_cus' ,
                         'ComputeUnit'               : 'bigjob_cu'  , 

                         'DataPilotService'          : 'bigjob_dps' ,
                         'DataPilot'                 : 'bigjob_dp'  ,
                         'DataUnitService'           : 'bigjob_dus' ,
                         'DataUnit'                  : 'bigjob_du'  , 

                         'ComputeDataUnitService'    : 'bigjob_cdus',
                         'ComputeDataUnit'           : 'bigjob_cdu' }

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
class bigjob_cps (troy.interface.iComputePilotService) :

    def __init__ (self, api, adaptor) :
        raise troy.pilot.TroyException (troy.pilot.Error.NotImplemented, "method not implemented!")


    def create_pilot (self, rm, cpd, cp_type=None, context=None):
        """ Add a ComputePilot to the ComputePilotService

            Keyword arguments:
            rm      -- Contact string for the resource manager
            cpd     -- ComputePilot Description
            cp_type -- backend type (optional)
            context -- Security context (optional)

            Return value:
            A ComputePilot handle
        """
        raise troy.pilot.TroyException (troy.pilot.Error.NotImplemented, "method not implemented!")


    def list_pilots (self, api):
        """ List all CPs """
        raise troy.pilot.TroyException (troy.pilot.Error.NotImplemented, "method not implemented!")


    def wait (self):
        """ Wait until CPS enters a final state """
        raise troy.pilot.TroyException (troy.pilot.Error.NotImplemented, "method not implemented!")


    def cancel (self):
        """ Cancel the CPS
            This also cancels all the ComputePilots that were under control of this
            CPS.
        """
        raise troy.pilot.TroyException (troy.pilot.Error.NotImplemented, "method not implemented!")


########################################################################
class bigjob_cp (troy.interface.iComputePilot) :

    def __init__ (self, api, adaptor) :
        raise troy.pilot.TroyException (troy.pilot.Error.NotImplemented, "method not implemented!")


    def wait (self):
        """ Wait until CP enters a final state """
        raise troy.pilot.TroyException (troy.pilot.Error.NotImplemented, "method not implemented!")


    def cancel (self):        
        """ Remove the ComputePilot from the ComputePilot Service.
        """
        raise troy.pilot.TroyException (troy.pilot.Error.NotImplemented, "method not implemented!")


    def reinitialize (self, cpd):        
        """ Re-Initialize the ComputePilot to the (new) ComputePilotDescription.
        
            Keyword arguments:
            cpd -- A ComputePilotDescription
        """
        raise troy.pilot.TroyException (troy.pilot.Error.NotImplemented, "method not implemented!")


    def set_callback (self, member, cb):
        """ Set a callback function for a member.

            Keyword arguments:
            member -- The member to set the callback for (state / state_detail / wall_time_left).
            cb     -- The callback object to call.
        """
        raise troy.pilot.TroyException (troy.pilot.Error.NotImplemented, "method not implemented!")


    def unset_callback (self, member):
        """ Unset a callback function from a member

            Keyword arguments:
            member -- The member to unset the callback for (state / state_detail / wall_tim_left).
        """
        raise troy.pilot.TroyException (troy.pilot.Error.NotImplemented, "method not implemented!")
    



########################################################################
class bigjob_cus (troy.interface.iComputeUnitService) :

    def __init__ (self, api, adaptor) :
        raise troy.pilot.TroyException (troy.pilot.Error.NotImplemented, "method not implemented!")

    def add_compute_pilot_service (self, cps):
        """ Add a ComputePilotService to this WUS.

            Keyword arguments:
            cps -- The ComputePilot Service to which this ComputeUnitService will connect.
        """
        raise troy.pilot.TroyException (troy.pilot.Error.NotImplemented, "method not implemented!")


    def list_compute_pilot_services (self):
        """ List all CPSs of CUS """
        raise troy.pilot.TroyException (troy.pilot.Error.NotImplemented, "method not implemented!")


    def remove_compute_pilot_service (self, cps):
        """ Remove a ComputePilotService 

            Note that it won't cancel the ComputePilotService, it will just no
            longer be connected to this CUS.

            Keyword arguments:
            cps -- The ComputePilotService to remove 
        """
        raise troy.pilot.TroyException (troy.pilot.Error.NotImplemented, "method not implemented!")


    def submit_compute_unit (self, cud):
        """ Submit a CU to this ComputeUnitService.

            Keyword argument:
            cud -- The ComputeUnitDescription from the application

            Return:
            ComputeUnit object
        """
        raise troy.pilot.TroyException (troy.pilot.Error.NotImplemented, "method not implemented!")


    def wait (self):
        """ Wait until CUS enters a final state """
        raise troy.pilot.TroyException (troy.pilot.Error.NotImplemented, "method not implemented!")


    def cancel (self):
        """ Cancel the WUS.
            
            Cancelling the WUS also cancels all the WUs submitted to it.
        """
        raise troy.pilot.TroyException (troy.pilot.Error.NotImplemented, "method not implemented!")


########################################################################
class bigjob_cu (troy.interface.iComputeUnit) :

    def __init__ (self, api, adaptor) :
        raise troy.pilot.TroyException (troy.pilot.Error.NotImplemented, "method not implemented!")

    def wait (self):
        """ Wait until CU enters a final state """
        raise troy.pilot.TroyException (troy.pilot.Error.NotImplemented, "method not implemented!")


    def cancel (self):
        """ Cancel the CU """
        raise troy.pilot.TroyException (troy.pilot.Error.NotImplemented, "method not implemented!")

    
    def set_callback (self, member, cb):
        """ Set a callback function for a member.

            Keyword arguments:
            member -- The member to set the callback for (state / state_detail).
            cb     -- The callback object to call.
        """
        raise troy.pilot.TroyException (troy.pilot.Error.NotImplemented, "method not implemented!")

    
    def unset_callback (self, member):
        """ Unset a callback function from a member

            Keyword arguments:
            member -- The member to unset the callback from.
        """
        raise troy.pilot.TroyException (troy.pilot.Error.NotImplemented, "method not implemented!")


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# Data API
#

########################################################################
class bigjob_dps (troy.interface.iDataPilotService) :

    def __init__ (self, api, adaptor) :
        raise troy.pilot.TroyException (troy.pilot.Error.NotImplemented, "method not implemented!")

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
        raise troy.pilot.TroyException (troy.pilot.Error.NotImplemented, "method not implemented!")


    def list_pilots (self):
        """ List all DPs """
        raise troy.pilot.TroyException (troy.pilot.Error.NotImplemented, "method not implemented!")


    def wait (self):
        """ Wait until DPS enters a final state """
        raise troy.pilot.TroyException (troy.pilot.Error.NotImplemented, "method not implemented!")


    def cancel (self):
        """ Cancel the DPS
            This also cancels all the DataPilots that were under control of this
            PDS.
        """
        raise troy.pilot.TroyException (troy.pilot.Error.NotImplemented, "method not implemented!")


########################################################################
class bigjob_dp (troy.interface.iDataPilot) :

    def __init__ (self, api, adaptor) :
        raise troy.pilot.TroyException (troy.pilot.Error.NotImplemented, "method not implemented!")

    def wait (self):
        """ Wait until DP enters a final state """
        raise troy.pilot.TroyException (troy.pilot.Error.NotImplemented, "method not implemented!")


    def cancel (self):        
        """ Cancel DP """
        raise troy.pilot.TroyException (troy.pilot.Error.NotImplemented, "method not implemented!")


    def reinitialize (self, dpd):        
        """ Re-Initialize the DataPilot to the (new) DataPilotDescription.
        
            Keyword arguments:
            dpd -- A DataPilotDescription
        """
        raise troy.pilot.TroyException (troy.pilot.Error.NotImplemented, "method not implemented!")


    def set_callback (self, member, cb):
        """ Set a callback function for a member.

            Keyword arguments:
            member -- The member to set the callback for (state / state_detail / size_left).
            cb     -- The callback object to call.
        """
        raise troy.pilot.TroyException (troy.pilot.Error.NotImplemented, "method not implemented!")

    def unset_callback (self, member):
        """ Unset a callback function from a member

            Keyword arguments:
            member -- The member to unset the callback for (state / state_detail / sizeleft).
        """
        raise troy.pilot.TroyException (troy.pilot.Error.NotImplemented, "method not implemented!")


########################################################################
class bigjob_dus (troy.interface.iDataUnitService) :

    def __init__ (self, api, adaptor) :
        raise troy.pilot.TroyException (troy.pilot.Error.NotImplemented, "method not implemented!")

    def add_data_pilot_service (self, dps):
        """ Add a DataPilotService 

            Keyword arguments:
            dps -- The DataPilotService to which this DataUnitService will connect.
        """
        raise troy.pilot.TroyException (troy.pilot.Error.NotImplemented, "method not implemented!")


    def list_data_pilot_services (self):
        """ List all DPSs of DUS """
        raise troy.pilot.TroyException (troy.pilot.Error.NotImplemented, "method not implemented!")
    

    def remove_data_pilot_service (self, dps):
        """ Remove a DataPilotService 

            Note that it won't cancel the DataPilotService, it will just no
            longer be connected to this DUS.
            
            Keyword arguments:
            dps -- The DataPilotService to remove 
        """
        raise troy.pilot.TroyException (troy.pilot.Error.NotImplemented, "method not implemented!")
    
    
    def submit_data_unit (self, dud):
        """ Submit a DU to this DataUnitService.

            Keyword argument:
            dud -- The DataUnitDescription from the application

            Return:
            DataUnit object
        """
        raise troy.pilot.TroyException (troy.pilot.Error.NotImplemented, "method not implemented!")


    def wait (self):
        """ Wait until DUS enters a final state """
        raise troy.pilot.TroyException (troy.pilot.Error.NotImplemented, "method not implemented!")

    
    def cancel (self):
        """ Cancel the DUS.
            
            Cancelling the DUS also cancels all the DUs submitted to it.
        """
        raise troy.pilot.TroyException (troy.pilot.Error.NotImplemented, "method not implemented!")


########################################################################
class bigjob_du (troy.interface.iDataUnit) :

    def __init__ (self, api, adaptor) :
        raise troy.pilot.TroyException (troy.pilot.Error.NotImplemented, "method not implemented!")


    def wait (self):
        """ Wait until DU enters a final state """
        raise troy.pilot.TroyException (troy.pilot.Error.NotImplemented, "method not implemented!")


    def cancel (self):
        """ Cancel the DU """
        raise troy.pilot.TroyException (troy.pilot.Error.NotImplemented, "method not implemented!")


    def set_callback (self, member, cb):
        """ Set a callback function for a member.

            Keyword arguments:
            member -- The member to set the callback for (state / state_detail).
            cb     -- The callback object to call.
        """
        raise troy.pilot.TroyException (troy.pilot.Error.NotImplemented, "method not implemented!")

    
    def unset_callback (self, member):
        """ Unset a callback function from a member

            Keyword arguments:
            member -- The member to unset the callback from.
        """
        raise troy.pilot.TroyException (troy.pilot.Error.NotImplemented, "method not implemented!")


    def list_files (self):
        """ list files managed by the DU """
        raise troy.pilot.TroyException (troy.pilot.troy.pilot.troy.pilot.Error.NotImplemented, "method not implemented!")
    

    def data_export (self, target_directory):
        """ copies content of DU to a directory on the local machine"""
        raise troy.pilot.TroyException (troy.pilot.Error.NotImplemented, "method not implemented!")

        
    def data_import (self, src_directory):
        """ copies content from a directory on the local machine to DU"""
        raise troy.pilot.TroyException (troy.pilot.Error.NotImplemented, "method not implemented!")


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# Compute-Data API
#

########################################################################
class bigjob_dcus (troy.interface.iComputeDataUnitService) :

    def __init__ (self, api, adaptor) :
        raise troy.pilot.TroyException (troy.pilot.Error.NotImplemented, "method not implemented!")




########################################################################
class bigjob_dcu (troy.interface.iComputeDataUnit) :

    def __init__ (self, api, adaptor) :
        raise troy.pilot.TroyException (troy.pilot.Error.NotImplemented, "method not implemented!")



# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

