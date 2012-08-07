
import imp
import urlparse

import troy
import troy.interface
from   troy.pilot.exception import TroyException, Error


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
        
        # duh!
        self.name     = 'troy_adaptor_peejay'

        # The registry maps api interface classes to the adaptor classes 
        # implementing them:
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
        
        # The adaptor_data keeps links between all id's and backend instances.
        # It is also use to maintain any other adaptor level state.
        self.adata = { 'cps' : {},
                       'cp'  : {}, 
                       'cus' : {},
                       'cu'  : {} }


    def get_name (self) :
        return self.name

    def get_registry (self) :
        return self.registry

    def get_order (self) :
        return 2

    def sanity_check (self) :
        # raise TroyException (Error.NoSuccess, "adaptor disabled")
        
        # try lo load peejay
        try :
            (f, p, d)   = imp.find_module ('peejay', ['/home/merzky/saga/peejay/'])
            self.module = imp.load_module ('peejay', f, p, d)
        except Exception as e :
            print ' ======== could not load peejay adaptor: ' + str (e)
            raise TroyException (Error.NoSuccess, 'Could not load the peejay module')

        # Hey, we can use peejay objects now!  Like this:
        # self.module.state.New

        # FIXME: disable module for now, so that we can test bigjob :P
        # raise TroyException (Error.NoSuccess, 'disabling peejay adaptor')
    

    # for each api object, we register our adaptor data.  That way, the adata
    # will be available in all adaptor level calls (each belonging to exactly
    # one api class instance).
    def register_adata (self, api) :

        self.api.idata_[self.get_name ()] = self.adata
        return self.adata


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# Compute API
#

########################################################################
class peejay_cps (troy.interface.iComputePilotService) :

    def __init__ (self, api, adaptor) :

        self.api     = api 
        self.adaptor = adaptor
        self.peejay  = self.adaptor.module

        # we MUST interpret cps_id, if present
        self.master  = self.peejay.master ()

        print "idata: " + str (self.api)

        if 'rm' in self.api.idata_ :
            self.rm = self.api.idata_['rm']
        else :
            self.rm = ''

        elems = urlparse.urlparse (self.rm)
        if elems.scheme != 'peejay' :
            raise troy.pilot.TroyException (troy.pilot.Error.BadParameter, 
                  "can only handle peejay:// URLs, not " + elems.scheme + "://")


        print " === peejay cps init done"

        # if we got this far, we can now register adaptor level instance data in
        # the api.  
        self.adata = self.adaptor.register_adata (self.api)


    def create_pilot (self, cpd) :
        """ Add a ComputePilot to the ComputePilotService

            Keyword arguments:
            cpd     -- ComputePilot Description

            Return value:
            A ComputePilot handle
        """

        print ' === self     :' + str (self    ) 
        print ' === cpd      :' + str (cpd     ) 

        # FIXME: add param checks
        pilot     = self.master.run_pilot ()
        pilot_id  = str (pilot.get_id ())

        # register pilot for later use
        self.adata['cp'][pilot_id] = pilot

        return troy.pilot.ComputePilot (pilot_id)



########################################################################
class peejay_cp (troy.interface.iComputePilot) :

    def __init__ (self, api, adaptor) :

        self.api     = api 
        self.adaptor = adaptor
        self.peejay  = self.adaptor.module

        # we MUST interpret cps_id, if present.  In fact, we need to have an id,
        # as creation is always done in the CPS
        if not 'id' in self.api.idata_ :
            raise troy.pilot.TroyException (troy.pilot.Error.NoSuccess, 
                    "peejay needs an id to reconnect to a pilot")

        self.id      = self.api.idata_['id']
        self.pilot   = self.peejay.pilot (self.id)
        self.running = 1

        print " === peejay cp init done"

        # if we got this far, we can now register adaptor level instance data in
        # the api.  
        self.adata = self.adaptor.register_adata (self.api)


    def get_id (self) :
        return self.id
   

    def submit_compute_unit (self, cud) :
        """ Submit a CU to this Pilot.

            Keyword argument:
            cud -- The ComputeUnitDescription from the application

            Return:
            ComputeUnit object
        """
        # build command from cud
        cmd = ""

        if not 'executable' in cud :
            raise troy.pilot.TroyException (troy.pilot.Error.NoSuccess, 
                    "executable missing in compute unit description!")


        if 'environment' in cud :
            cmd += '/bin/env'
            for env in cud['environment'] :
                cmd += ' ' + env
            cmd += ' '

        cmd += cud['executable']

        if 'arguments' in cud :
            for arg in cud['arguments'] :
                cmd += ' ' + arg

        job      = self.pilot.job_submit (cmd)
        job_id   = str (job.get_id ())

        # register cu for later state checks etc.
        self.adata['cu'][job_id] = job

        return troy.pilot.ComputeUnit (job_id)


    def wait (self) :
        """ Wait until CP enters a final state """
        if not self.running :
            return

        self.pilot.wait ()
        self.running = 0


    def cancel (self) :
        """ Remove the ComputePilot from the ComputePilot Service.
        """
        if not self.running :
            return

        self.pilot.kill ()
        self.running = 0


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
        if not self.running :
            raise troy.pilot.TroyException (troy.pilot.Error.IncorrectState, 
                    "cannot attach callback to dead pilot!")

        raise troy.pilot.TroyException (troy.pilot.Error.NotImplemented, "method not implemented!")


    def unset_callback (self, member) :
        """ Unset a callback function from a member

            Keyword arguments:
            member -- The member to unset the callback for (state / state_detail / wall_tim_left).
        """
        if not self.running :
            raise troy.pilot.TroyException (troy.pilot.Error.IncorrectState, 
                    "cannot remove callback from dead pilot!")

        raise troy.pilot.TroyException (troy.pilot.Error.NotImplemented, "method not implemented!")
    



########################################################################
class peejay_cus (troy.interface.iComputeUnitService) :

    cus_index = 0

    def __init__ (self, api, adaptor) :

        self.api     = api 
        self.adaptor = adaptor
        self.peejay  = self.adaptor.module
        self.cp      = []  # list of associated compute pilots


        peejay_cus.cus_index += 1
        self.id      = str (peejay_cus.cus_index)

        # we MUST interpret cus_id, if present.  But in fact, peejay does not
        # have a CUS, so we cannot, ever, reconnect to a CUS.  So, we have to
        # throw if an id is present
        # as creation is always done in the CPS
        if 'id' in self.api.idata_ :
            if self.api.idata_['id'] :
                raise troy.pilot.TroyException (troy.pilot.Error.NoSuccess, "peejay cannot reconnect to CUS!")

        print " === peejay cus init done"

        # we need a scheduler.  There is no way for the API to re-init or
        # re-assign a scheduler after the CUS has been created -- the scheduler
        # is fully internal -- so we can just create it here.  For now, we use
        # the 'Random' scheduler
        self.scheduler = troy.pilot.ComputeScheduler_ ('Random')

        # if we got this far, we can now register adaptor level instance data in
        # the api.  
        self.adata = self.adaptor.register_adata (self.api)

        # register the pilot after creation
        self.adata ['cus'][self.id] = self



    def get_id (self) :
        return self.id



    def add_compute_pilot (self, cp) :
        """ Add a ComputePilot to this CUS.

            Keyword arguments:
            cp -- The ComputePilot to which this ComputeUnitService will connect.
        """
        self.cp.append (cp)


    def list_compute_pilots (self) :
        """ List all CPs of CUS """

        ret = []

        for cp in self.cp :
            ret.append (cp.get_id ())

        return ret


    def remove_compute_pilot (self, cp) :
        """ Remove a ComputePilot

            Note that it won't cancel the ComputePilot, it will just no longer
            receive any CUs.

            Keyword arguments:
            cp -- The ComputePilot to remove 
        """
        self.cp.remove (cp)


########################################################################
class peejay_cu (troy.interface.iComputeUnit) :

    def __init__ (self, api, adaptor) :

        self.api     = api 
        self.adaptor = adaptor
        self.peejay  = self.adaptor.module

        # we MUST interpret cu_id, if present.  In fact, we need to have an id,
        # as creation is always done in the CUS
        if not 'id' in self.api.idata_ :
            raise troy.pilot.TroyException (troy.pilot.Error.NoSuccess, 
                    "peejay needs an id to reconnect to a cu")

        self.id = self.api.idata_['id']

        print " === peejay cu init done"

        # if we got this far, we can now register adaptor level instance data in
        # the api.  
        self.adata = self.adaptor.register_adata (self.api)
        self.job   = self.adata['cu'][self.id]



    def wait (self) :
        """ Wait until CU enters a final state """
        self.job.wait ()



    def cancel (self) :
        """ Cancel the CU """
        self.job.cancel ()

    
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
class peejay_dps (troy.interface.iDataPilotService) :

    def __init__ (self, api, adaptor) :
        raise troy.pilot.TroyException (troy.pilot.Error.NotImplemented, "method not implemented!")

    def create_pilot (self, dpd) :
        """ Add a DataPilot to the DataPilotService

            Keyword arguments:
            cpd     -- DataPilot Description

            Return value:
            A DataPilot handle
        """
        raise troy.pilot.TroyException (troy.pilot.Error.NotImplemented, "method not implemented!")


########################################################################
class peejay_dp (troy.interface.iDataPilot) :

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
class peejay_dus (troy.interface.iDataUnitService) :

    def __init__ (self, api, adaptor) :
        raise troy.pilot.TroyException (troy.pilot.Error.NotImplemented, "method not implemented!")

    def add_data_pilot (self, dp) :
        """ Add a DataPilot

            Keyword arguments:
            dp -- The DataPilot to which this DataUnitService will connect.
        """
        raise troy.pilot.TroyException (troy.pilot.Error.NotImplemented, "method not implemented!")


    def list_data_pilots (self) :
        """ List all DPs of DUS """
        raise troy.pilot.TroyException (troy.pilot.Error.NotImplemented, "method not implemented!")
    

    def remove_data_pilot_service (self, dps) :
        """ Remove a DataPilotService 

            Note that it won't cancel the DataPilot, it will just no longer
            receive any DUs.
            
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
class peejay_du (troy.interface.iDataUnit) :

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
class peejay_dcus (troy.interface.iComputeDataUnitService) :

    def __init__ (self, api, adaptor) :
        raise troy.pilot.TroyException (troy.pilot.Error.NotImplemented, "method not implemented!")




########################################################################
class peejay_dcu (troy.interface.iComputeDataUnit) :

    def __init__ (self, api, adaptor) :
        raise troy.pilot.TroyException (troy.pilot.Error.NotImplemented, "method not implemented!")



# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

