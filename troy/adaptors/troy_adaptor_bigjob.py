
import imp
import urlparse

import troy
import troy.interface
from   troy.pilot.exception import TroyException, Error


########################################################################
#
# main adaptor class, registers the implementation with troy upon loading
#
class adaptor (troy.interface.aBase) :
    
    def __init__ (self) :
        
        # we do not simply import bigjob, but rather load the bigjob module
        # 'manually' -- that seems (to me) the easiest way to avoid pilot API
        # name space clashes / confusions...

        print "adaptor bigjob: init: load bigjob's pilot module"
        ## try :
        ##     file, path, desc = imp.find_module ('pilot')
        ##     self.bj_module   = imp.load_module ('pilot', file, path, desc)
        ##     print str(self.bj_module)
        ##     print "loading bigjob's pilot module ok, version (" + str (self.bj_module.application_id) + ")"

        ## except Exception as e :
        ##     print "loading bigjob failed: " + str (e)
        ##     raise troy.pilot.TroyException (troy.pilot.Error.NoSuccess, 
        ##                                     "Could not load bigjob!")

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
        return 1

    def sanity_check (self) :
        raise TroyException (Error.NoSuccess, "adaptor disabled")

        # # not sure when the BJ pilot API was introduced, but everything beyond
        # # 0.4 should be fine
        # v = self.bj_module.version
        # v1, v2, v3 = v.split ('.')
        # if int (v1) < 1 and int (v2) < 4 :
        #     raise TroyException (Error.NoSuccess, 
        #           "Cannot use BigJob version older than 0.4 (found " + v + ")")

        # the pilot API module does not have a version, so we just check its
        # application_id
        app_id = self.bj_module.application_id

        if app_id != 'bigjob' :
            raise TroyException (Error.NoSuccess, 
                  "Cannot use non-BigJob version of pilot api (found %s)"  %  app_id)


    # for each api object, we register our adaptor data.  That way, the adata
    # will be available in all adaptor level calls (each belonging to exactly
    # one api class instance).
    def register_adata (self) :

        self.api.idata_[self.get_name ()] = self.adata
        return self.adata



#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# Compute API
#

########################################################################
class bigjob_cps (troy.interface.iComputePilotService) :

    def __init__ (self, api, adaptor) :

        print "bj cps ctor"
        self.api     = api 
        self.adaptor = adaptor

        # FIXME: check if we need to reconnect to an ID

        if 'rm' in self.api.idata_ :
            self.rm = self.api.idata_['rm']
        else :
            self.rm = ''

        elems = urlparse.urlparse (self.rm)
        if elems.scheme != 'bigjob' :
            raise troy.pilot.TroyException (troy.pilot.Error.BadParameter, 
                  "can only handle bigjob:// URLs, not " + elems.scheme + "://")

        # all ok now, we can create and register the cps in the adaptor
        self.cps = self.adaptor.bj_module.PilotComputeService (1)
        self.id  = self.cps.id
        self.adaptor.adata['cps'][self.id] = self.cps


    def create_pilot (self, cpd) :
        """ Create a ComputePilot

            Keyword arguments:
            cpd     -- ComputePilot Description

            Return value:
            A ComputePilot handle
        """
        if not 'number_of_processes' in cpd.keys () : cpd['number_of_processes'] = 1
        if not 'queue'               in cpd.keys () : cpd['queue'              ] = ''
        if not 'project'             in cpd.keys () : cpd['project'            ] = ''
        if not 'workingdirectory'    in cpd.keys () : cpd['workingdirectory'   ] = '/tmp'
        if not 'userproxy'           in cpd.keys () : cpd['userproxy'          ] = ''
        if not 'walltime'            in cpd.keys () : cpd['walltime'           ] = ''
        if not 'processes_per_node'  in cpd.keys () : cpd['processes_per_node' ] = 1

        print str (cpd)

        cpd_copy = cpd
        cpd_copy['resource_url'] = cpd_copy['rm']

        pilot     = self.cps.create_pilot (cpd['rm'], cpd)
        pilot_id  = pilot.id
        self.adaptor.adata['cp'][pilot_id] = pilot

        return troy.pilot.ComputePilot (pilot_id)


########################################################################
class bigjob_cp (troy.interface.iComputePilot) :

    def __init__ (self, api, adaptor) :
        print "bj cp ctor"
        self.api     = api 
        self.adaptor = adaptor

        if 'id' in self.api.idata_ :
            self.id = self.iapi.data_['id']
        else :
            raise troy.pilot.TroyException (troy.pilot.Error.BadParameter,
                    "cannot create ComputePilot w/o ID")

        if not self.id in self.adaptor.adata['cp'].keys () :
            raise troy.pilot.TroyException (troy.pilot.Error.BadParameter,
                    "cannot reconnect to ComputePilot with ID " + self.id)

        # all seems fine: id is valid and known to the adaptor.


    def submit_compute_unit (self, cud) :
        """ Submit a CU to this ComputePilot.

            Keyword argument:
            cud -- The ComputeUnitDescription from the application

            Return:
            ComputeUnit object
        """
        raise troy.pilot.TroyException (troy.pilot.Error.NotImplemented, "method not implemented!")


    def wait (self) :
        """ Wait until CP enters a final state """
        raise troy.pilot.TroyException (troy.pilot.Error.NotImplemented, "method not implemented!")


    def cancel (self) :
        """ Remove the ComputePilot from the ComputePilot Service.
        """
        raise troy.pilot.TroyException (troy.pilot.Error.NotImplemented, "method not implemented!")


    def get_id (self) :
        """ get instance id """
        return self.id


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
class bigjob_cus (troy.interface.iComputeUnitService) :

    # Note that Bigjob, surprisingly, does not have a ComputeUnitService
    # implementation -- so we use its ComputeDataService
    
    def __init__ (self, api, adaptor) :

        self.api     = api 
        self.adaptor = adaptor

        id = self.api.idata_['id']

        # we will only handle this api class if its ID is 'None', or was issued
        # by this adaptor -- otherwise a different adaptor already manages it.
        if not id == None :

            if not id in self.adaptor.adata['cus'] :

                # try to reconnect to that CUS
                try :
                    self.cus = self.adaptor.bj_module.ComputeDataService (id)
                except :
                    # did not work, so we cannot handle the given id
                    raise troy.pilot.TroyException (troy.pilot.Error.NoSuccess, 
                        "API class handled by a different adaptor")

            else : 
                # we found the id and the instance, and reconnect to the class 
                self.cus = self.adaptor.adata['cus'][id]

        # id is none - init new instance
        else :
            # create the cus, and assign id
            self.cus              = self.adaptor.bj_module.ComputeDataService ()
            cus_id                = self.cus.get_id ()
            self.api.idata_['id'] = cus_id
            self.adaptor.adata['cus'][cus_id] = self.cus


    def add_compute_pilot (self, cp) :
        """ Add a ComputePilot to this CUS.

            Keyword arguments:
            cps -- The ComputePilot to which this ComputeUnitService will connect.
        """
        # we leave this to the default adaptor
        raise troy.pilot.TroyException (troy.pilot.Error.NotImplemented, "method not implemented!")


    def list_compute_pilots (self) :
        """ List all CPs of CUS """
        # we leave this to the default adaptor
        raise troy.pilot.TroyException (troy.pilot.Error.NotImplemented, "method not implemented!")


    def remove_compute_pilot (self, cp) :
        """ Remove a ComputePilot

            Note that it won't cancel the ComputePilot, it will just not receive
            any CUs anynmore.

            Keyword arguments:
            cp -- The ComputePilot to remove 
        """
        # we leave this to the default adaptor
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
class bigjob_cu (troy.interface.iComputeUnit) :

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

            Keyword arguments :
            member -- The member to set the callback for (state / state_detail).
            cb     -- The callback object to call.
        """
        raise troy.pilot.TroyException (troy.pilot.Error.NotImplemented, "method not implemented!")

    
    def unset_callback (self, member) :
        """ Unset a callback function from a member

            Keyword arguments :
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

    def create_pilot (self, dpd) :
        """ Create a DataPilot.

            Keyword arguments:
            cpd     -- DataPilot Description

            Return value:
            A DataPilot handle
        """
        raise troy.pilot.TroyException (troy.pilot.Error.NotImplemented, "method not implemented!")


########################################################################
class bigjob_dp (troy.interface.iDataPilot) :

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
class bigjob_dus (troy.interface.iDataUnitService) :

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
    

    def remove_data_pilot (self, dp) :
        """ Remove a DataPilot 

            Note that it won't cancel the DataPilot, it will just not receive
            any DUs anymore.
            
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
class bigjob_du (troy.interface.iDataUnit) :

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
class bigjob_dcus (troy.interface.iComputeDataUnitService) :

    def __init__ (self, api, adaptor) :
        raise troy.pilot.TroyException (troy.pilot.Error.NotImplemented, "method not implemented!")




########################################################################
class bigjob_dcu (troy.interface.iComputeDataUnit) :

    def __init__ (self, api, adaptor) :
        raise troy.pilot.TroyException (troy.pilot.Error.NotImplemented, "method not implemented!")



# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

