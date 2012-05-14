
import imp

import troy
import troy.interface
from   troy.pilot.exception import TroyException, Error

from   bigjob import bigjob, subjob, description


COORDINATION_URL = "advert://localhost/?dbtype=sqlite3"


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

        self.api     = api 
        self.adaptor = adaptor
        self.idata   = self.api.get_idata_ ()

        # if we got this far, we can now register adaptor level instance data in
        # the api.  
        self.adata = self.adaptor.register_adata (self.api)


    def create_pilot (self, cpd, context=None):
        """ Create a ComputePilot

            Keyword arguments:
            cpd     -- ComputePilot Description
            context -- Security context (optional)

            Return value:
            A ComputePilot handle
        """
        pilot = bigjob (COORDINATION_URL)
        pilot.start_pilot_job (cpd['rm'],
                               None,
                               cpd['number_of_processes'],
                               cpd['queue'],
                               cpd['project'],
                               cpd['workingdirectory'],
                               cpd['userproxy'],
                               cpd['walltime'],
                               cpd['processes_per_node'])
        pilot_url = pilot.pilot_url
        self.adata['cp'][pilot_url] = pilot

        return pilot_url


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

    def add_compute_pilot (self, cp):
        """ Add a ComputePilot to this CUS.

            Keyword arguments:
            cps -- The ComputePilot to which this ComputeUnitService will connect.
        """
        raise troy.pilot.TroyException (troy.pilot.Error.NotImplemented, "method not implemented!")


    def list_compute_pilots (self):
        """ List all CPs of CUS """
        raise troy.pilot.TroyException (troy.pilot.Error.NotImplemented, "method not implemented!")


    def remove_compute_pilot (self, cp):
        """ Remove a ComputePilot

            Note that it won't cancel the ComputePilot, it will just not receive
            any CUs anynmore.

            Keyword arguments:
            cp -- The ComputePilot to remove 
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
        """ Cancel the CUS.
            
            Cancelling the CUS also cancels all the CUS submitted to it.
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

    def create_pilot (self, dpd, context=None):
        """ Create a DataPilot.

            Keyword arguments:
            cpd     -- DataPilot Description
            context -- Security context (optional)

            Return value:
            A DataPilot handle
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

    def add_data_pilot (self, dp):
        """ Add a DataPilot

            Keyword arguments:
            dp -- The DataPilot to which this DataUnitService will connect.
        """
        raise troy.pilot.TroyException (troy.pilot.Error.NotImplemented, "method not implemented!")


    def list_data_pilots (self):
        """ List all DPs of DUS """
        raise troy.pilot.TroyException (troy.pilot.Error.NotImplemented, "method not implemented!")
    

    def remove_data_pilot (self, dp):
        """ Remove a DataPilot 

            Note that it won't cancel the DataPilot, it will just not receive
            any DUs anymore.
            
            Keyword arguments:
            dp -- The DataPilot to remove 
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

