
import imp

import troy
import troy.interface
from troy.pilot.exception import TroyException, Error


########################################################################
# 
# This TROY adaptor interfaces to peejay, a minimal P* aligned PJ (doh!) 
# implementation -- see https://github.com/andre-merzky/peejay
#


########################################################################
#
# main adaptor class, registers the implementation with troy upon loading
#
class adaptor (troy.interface.aBase) :
    
    def __init__ (self) :
        
        # registry maps api classes to adaptor classes implementing the
        # respective class interface.
        self.name     = 'troy_adaptor_peejay'
        self.registry = {'ComputePilotService'       : 'peejay_cps' ,
                         'ComputePilot'              : 'peejay_cp'  ,
                         'ComputeUnitService'        : 'peejay_cus' ,
                         'ComputeUnit'               : 'peejay_cu'  , 

                         'DataPilotService'          : 'peejay_dps' ,
                         'DataPilot'                 : 'peejay_dp'  ,
                         'DataUnitService'           : 'peejay_dus' ,
                         'DataUnit'                  : 'peejay_du'  , 

                         'ComputeDataUnitService'    : 'peejay_cdus',
                         'ComputeDataUnit'           : 'peejay_cdu' }

    def get_name (self):
        return self.name


    def get_registry (self):
        return self.registry


    def sanity_check (self):
        
        # try lo load peejay
        try :
            (f, p, d)   = imp.find_module ('peejay', ['/home/merzky/saga/peejay/'])
            self.module = imp.load_module ('peejay', f, p, d)
        except Exception as e :
            print ' ======== could not load peejay adaptor: ' + str (e)
            raise TroyException (Error.NoSuccess, 'Could not load the peejay module')

        # Hey, we can use peejay objects now!  Like this:
        # self.module.state.New


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# Compute API
#

########################################################################
class peejay_cps (troy.interface.iComputePilotService) :

    def __init__ (self, api, adaptor) :

        self.api     = api 
        self.adaptor = adaptor
        self.idata   = self.api.get_idata_ ('api')

        # we MUST interpret cps_id, if present
        if 'id' in self.idata :
            if self.idata['id'] :
                raise troy.pilot.TroyException (troy.pilot.Error.NoSuccess, 
                        "peejay cannot yet reconnect to CPS instances")

        print " === peejay cps init done"

        self.peejay  = self.adaptor.module
        self.master  = self.peejay.master ()

        # if we got this far, we can now register adaptor level instance data in
        # the api.  Well, we don't have any, yet, but anyway: that saves us from
        # checking dict keys later on
        self.api.set_idata_ (self.adaptor.get_name (), {})



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

        print ' === self     :' + str(self    ) 
        print ' === rm       :' + str(rm      ) 
        print ' === cpd      :' + str(cpd     ) 
        print ' === cp_type  :' + str(cp_type ) 
        print ' === context  :' + str(context ) 

        # FIXME: add param checks
        pilot = self.master.run_pilot ()
        ret   = troy.pilot.ComputePilot (pilot.get_id ())



    def list_pilots (self):
        return self.master.list_pilots ()

        """ List all CPs """



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
class peejay_cp (troy.interface.iComputePilot) :

    def __init__ (self, api, adaptor) :

        self.api     = api 
        self.adaptor = adaptor
        self.idata   = self.api.get_idata_ ('api')

        self.peejay  = self.adaptor.module
        self.master  = self.peejay.master ()

        # we MUST interpret cps_id, if present.  In fact, we need to have an id,
        # as creation is always done in the CPS
        have_id = False
        if 'id' in self.idata :
            if self.idata['id'] :
                self.pilot = self.peejay.pilot (self.idata['id'])
                have_id    = True

        if not have_id :
            raise troy.pilot.TroyException (troy.pilot.Error.NoSuccess, 
                    "peejay cannot needs an id to reconnect to a pilot")

        print " === peejay cp init done"

        # if we got this far, we can now register adaptor level instance data in
        # the api.  Well, we don't have any, yet, but anyway: that saves us from
        # checking dict keys later on
        self.api.set_idata_ (self.adaptor.get_name (), {})


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
class peejay_cus (troy.interface.iComputeUnitService) :

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
class peejay_cu (troy.interface.iComputeUnit) :

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
class peejay_dps (troy.interface.iDataPilotService) :

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
class peejay_dp (troy.interface.iDataPilot) :

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
class peejay_dus (troy.interface.iDataUnitService) :

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
class peejay_du (troy.interface.iDataUnit) :

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
class peejay_dcus (troy.interface.iComputeDataUnitService) :

    def __init__ (self, api, adaptor) :
        raise troy.pilot.TroyException (troy.pilot.Error.NotImplemented, "method not implemented!")




########################################################################
class peejay_dcu (troy.interface.iComputeDataUnit) :

    def __init__ (self, api, adaptor) :
        raise troy.pilot.TroyException (troy.pilot.Error.NotImplemented, "method not implemented!")



# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

