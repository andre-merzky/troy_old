
import troy
import troy.interface

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
#   - in the new adaptor, replace all occurrences of 'xyz' with <backend>
#   - implement all classes/methods
#


########################################################################
#
# main adaptor class, registers the implementation with troy upon loading
#
class adaptor (troy.interface.aBase) :
    
    def __init__ (self) :
        
        # duh!
        self.name     = 'troy_adaptor_xyz'

        # registry maps api classes to adaptor classes implementing the
        # respective class interface.
        self.registry = {'ComputePilotService'       : 'xyz_cps' ,
                         'ComputePilot'              : 'xyz_cp'  ,
                         'ComputeUnitService'        : 'xyz_cus' ,
                         'ComputeUnit'               : 'xyz_cu'  , 

                         'DataPilotService'          : 'xyz_dps' ,
                         'DataPilot'                 : 'xyz_dp'  ,
                         'DataUnitService'           : 'xyz_dus' ,
                         'DataUnit'                  : 'xyz_du'  , 

                         'ComputeDataUnitService'    : 'xyz_cdus',
                         'ComputeDataUnit'           : 'xyz_cdu' }

    def get_name (self) :
        return self.name

    def get_registry (self) :
        return self.registry

    def get_order (self) :
        return 3

    def sanity_check (self) :
        # version checks etc.
        pass


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# Compute API
#

########################################################################
class xyz_cps (troy.interface.iComputePilotService) :

    def __init__ (self, api, adaptor) :
        raise troy.pilot.TroyException (troy.pilot.Error.NotImplemented, "method not implemented!")


    def create_pilot (self, cpd, context=None) :
        """ Create a ComputePilot.

            Keyword arguments:
            cpd     -- ComputePilot Description
            context -- Security context (optional)

            Return value:
            A ComputePilot handle
        """
        raise troy.pilot.TroyException (troy.pilot.Error.NotImplemented, "method not implemented!")



########################################################################
class xyz_cp (troy.interface.iComputePilot) :

    def __init__ (self, api, adaptor) :
        raise troy.pilot.TroyException (troy.pilot.Error.NotImplemented, "method not implemented!")


    def wait (self) :
        """ Wait until CP enters a final state """
        raise troy.pilot.TroyException (troy.pilot.Error.NotImplemented, "method not implemented!")


    def cancel (self) :
        """ Remove the ComputePilot from the ComputePilot Service.
        """
        raise troy.pilot.TroyException (troy.pilot.Error.NotImplemented, "method not implemented!")


    def reinitialize (self, cpd) :
        """ Re-Initialize the ComputePilot to the (new) ComputePilotDescription.
        
            Keyword arguments:
            cpd -- A ComputePilotDescription
        """
        raise troy.pilot.TroyException (troy.pilot.Error.NotImplemented, "method not implemented!")


    def set_callback (self, member, cb) :
        """ Set a callback function for a member.

            Keyword arguments:
            member -- The member to set the callback for (state / state_detail / wall_time_left).
            cb     -- The callback object to call.
        """
        raise troy.pilot.TroyException (troy.pilot.Error.NotImplemented, "method not implemented!")


    def unset_callback (self, member) :
        """ Unset a callback function from a member

            Keyword arguments:
            member -- The member to unset the callback for (state / state_detail / wall_tim_left).
        """
        raise troy.pilot.TroyException (troy.pilot.Error.NotImplemented, "method not implemented!")
    



########################################################################
class xyz_cus (troy.interface.iComputeUnitService) :

    def __init__ (self, api, adaptor) :
        raise troy.pilot.TroyException (troy.pilot.Error.NotImplemented, "method not implemented!")

    def add_compute_pilot (self, cp) :
        """ Add a ComputePilot to this CUS.

            Keyword arguments:
            cp -- The ComputePilot to which this ComputeUnitService will connect.
        """
        raise troy.pilot.TroyException (troy.pilot.Error.NotImplemented, "method not implemented!")


    def list_compute_pilots (self) :
        """ List all CPs of CUS """
        raise troy.pilot.TroyException (troy.pilot.Error.NotImplemented, "method not implemented!")


    def remove_compute_pilot (self, cp) :
        """ Remove a ComputePilot

            Note that it won't cancel the ComputePilot, it will just no longer
            receive any CUs

            Keyword arguments:
            cp -- The ComputePilot to remove 
        """
        raise troy.pilot.TroyException (troy.pilot.Error.NotImplemented, "method not implemented!")


    def submit_compute_unit (self, cud) :
        """ Submit a CU to this ComputeUnitService.

            Keyword argument:
            cud -- The ComputeUnitDescription from the application

            Return:
            ComputeUnit object
        """
        raise troy.pilot.TroyException (troy.pilot.Error.NotImplemented, "method not implemented!")


########################################################################
class xyz_cu (troy.interface.iComputeUnit) :

    def __init__ (self, api, adaptor) :
        raise troy.pilot.TroyException (troy.pilot.Error.NotImplemented, "method not implemented!")

    def wait (self) :
        """ Wait until CU enters a final state """
        raise troy.pilot.TroyException (troy.pilot.Error.NotImplemented, "method not implemented!")


    def cancel (self) :
        """ Cancel the CU """
        raise troy.pilot.TroyException (troy.pilot.Error.NotImplemented, "method not implemented!")

    
    def set_callback (self, member, cb) :
        """ Set a callback function for a member.

            Keyword arguments:
            member -- The member to set the callback for (state / state_detail).
            cb     -- The callback object to call.
        """
        raise troy.pilot.TroyException (troy.pilot.Error.NotImplemented, "method not implemented!")

    
    def unset_callback (self, member) :
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
class xyz_dps (troy.interface.iDataPilotService) :

    def __init__ (self, api, adaptor) :
        raise troy.pilot.TroyException (troy.pilot.Error.NotImplemented, "method not implemented!")

    def create_pilot (self, dpd, context=None) :
        """ Create a DataPilot.

            Keyword arguments:
            cpd     -- DataPilot Description
            context -- Security context (optional)

            Return value:
            A DataPilot handle
        """
        raise troy.pilot.TroyException (troy.pilot.Error.NotImplemented, "method not implemented!")


########################################################################
class xyz_dp (troy.interface.iDataPilot) :

    def __init__ (self, api, adaptor) :
        raise troy.pilot.TroyException (troy.pilot.Error.NotImplemented, "method not implemented!")

    def wait (self) :
        """ Wait until DP enters a final state """
        raise troy.pilot.TroyException (troy.pilot.Error.NotImplemented, "method not implemented!")


    def cancel (self) :
        """ Cancel DP """
        raise troy.pilot.TroyException (troy.pilot.Error.NotImplemented, "method not implemented!")


    def reinitialize (self, dpd) :
        """ Re-Initialize the DataPilot to the (new) DataPilotDescription.
        
            Keyword arguments:
            dpd -- A DataPilotDescription
        """
        raise troy.pilot.TroyException (troy.pilot.Error.NotImplemented, "method not implemented!")


    def set_callback (self, member, cb) :
        """ Set a callback function for a member.

            Keyword arguments:
            member -- The member to set the callback for (state / state_detail / size_left).
            cb     -- The callback object to call.
        """
        raise troy.pilot.TroyException (troy.pilot.Error.NotImplemented, "method not implemented!")

    def unset_callback (self, member) :
        """ Unset a callback function from a member

            Keyword arguments:
            member -- The member to unset the callback for (state / state_detail / sizeleft).
        """
        raise troy.pilot.TroyException (troy.pilot.Error.NotImplemented, "method not implemented!")


########################################################################
class xyz_dus (troy.interface.iDataUnitService) :

    def __init__ (self, api, adaptor) :
        raise troy.pilot.TroyException (troy.pilot.Error.NotImplemented, "method not implemented!")

    def add_data_pilot (self, dp) :
        """ Add a DataPilot

            Keyword arguments:
            dp -- The DataPilotto which this DataUnitService will connect.
        """
        raise troy.pilot.TroyException (troy.pilot.Error.NotImplemented, "method not implemented!")


    def list_data_pilots (self) :
        """ List all DPs of DUS """
        raise troy.pilot.TroyException (troy.pilot.Error.NotImplemented, "method not implemented!")
    

    def remove_data_pilot (self, dp) :
        """ Remove a DataPilot 

            Note that it won't cancel the DataPilot, it will just no longer
            receive any DUs
            
            Keyword arguments:
            dp -- The DataPilot to remove 
        """
        raise troy.pilot.TroyException (troy.pilot.Error.NotImplemented, "method not implemented!")
    
    
    def submit_data_unit (self, dud) :
        """ Submit a DU to this DataUnitService.

            Keyword argument:
            dud -- The DataUnitDescription from the application

            Return:
            DataUnit object
        """
        raise troy.pilot.TroyException (troy.pilot.Error.NotImplemented, "method not implemented!")



########################################################################
class xyz_du (troy.interface.iDataUnit) :

    def __init__ (self, api, adaptor) :
        raise troy.pilot.TroyException (troy.pilot.Error.NotImplemented, "method not implemented!")


    def wait (self) :
        """ Wait until DU enters a final state """
        raise troy.pilot.TroyException (troy.pilot.Error.NotImplemented, "method not implemented!")


    def cancel (self) :
        """ Cancel the DU """
        raise troy.pilot.TroyException (troy.pilot.Error.NotImplemented, "method not implemented!")


    def set_callback (self, member, cb) :
        """ Set a callback function for a member.

            Keyword arguments:
            member -- The member to set the callback for (state / state_detail).
            cb     -- The callback object to call.
        """
        raise troy.pilot.TroyException (troy.pilot.Error.NotImplemented, "method not implemented!")

    
    def unset_callback (self, member) :
        """ Unset a callback function from a member

            Keyword arguments:
            member -- The member to unset the callback from.
        """
        raise troy.pilot.TroyException (troy.pilot.Error.NotImplemented, "method not implemented!")


    def list_files (self) :
        """ list files managed by the DU """
        raise troy.pilot.TroyException (troy.pilot.troy.pilot.troy.pilot.Error.NotImplemented, "method not implemented!")
    

    def data_export (self, target_directory) :
        """ copies content of DU to a directory on the local machine"""
        raise troy.pilot.TroyException (troy.pilot.Error.NotImplemented, "method not implemented!")

        
    def data_import (self, src_directory) :
        """ copies content from a directory on the local machine to DU"""
        raise troy.pilot.TroyException (troy.pilot.Error.NotImplemented, "method not implemented!")


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# Compute-Data API
#

########################################################################
class xyz_dcus (troy.interface.iComputeDataUnitService) :

    def __init__ (self, api, adaptor) :
        raise troy.pilot.TroyException (troy.pilot.Error.NotImplemented, "method not implemented!")




########################################################################
class xyz_dcu (troy.interface.iComputeDataUnit) :

    def __init__ (self, api, adaptor) :
        raise troy.pilot.TroyException (troy.pilot.Error.NotImplemented, "method not implemented!")


