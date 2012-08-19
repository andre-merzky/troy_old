
import troy
import troy.interface
from   troy.pilot.exception import TroyException, Error


########################################################################
#
# This default adaptor only implements the XxxUnitServices.  Those 'Services'
# can trivially be implemented as a container of XxxPilots, where CUs are being
# submitted to any one of the pilots.
#
# A major motivation for Troy is to provide application level scheduling on
# XxxUnitService level, which is provided by the scheduler adaptors.  This
# default XxxUnitService adaptor makes sure that the scheduler can actually be
# invoked when no backend provides an XxxUnitService implementation (which is in
# fact the expected case).
# 
class adaptor (troy.interface.aBase) :
    
    def __init__ (self) :
        
        self.name     = 'troy_adaptor_default'

        # this adaptor only implements the XxxUnitService classes
        self.registry = {'ComputeUnitService'        : 'default_cus' ,
                         'DataUnitService'           : 'default_dus' ,
                         'ComputeDataUnitService'    : 'default_cdus'}

        # 'generator' for serial id's
        self.serial_ = 0

        self.adata = { 
                       'cus'  : {},
                       'dus'  : {},
                       'cdus' : {} 
                     }

    def get_name (self) :
        return self.name

    def get_registry (self) :
        return self.registry

    def get_order (self) :
        return 1000  # low adaptor priority

    def sanity_check (self) :
      # raise TroyException (Error.NoSuccess, "adaptor disabled")
        pass

    def get_serial_ (self) :
        self.serial_ += 1
        return self.serial_


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# Compute API
#
########################################################################
class default_cus (troy.interface.iComputeUnitService) :

    def __init__ (self, api, adaptor) :

        self.api     = api 
        self.adaptor = adaptor

        self.id = None
        if 'id' in self.api :
            self.id = self.api.id

        # we will only handle this api class if its ID is 'None', or was issued
        # by this adaptor -- otherwise a different adaptor already manages it.
        if self.id == None :

            # id is none - init new instance.  assign an id
            self.id = "troy_adaptor_default_cus_%d"  %  self.adaptor.get_serial_ ()
            self.api['id'] = self.id

            # get a scheduler instance, as requested via idata.  We always get that
            # scheduler instance, even if taking over a CUS created by a foreign
            # adaptor...
            self.scheduler = troy.pilot.compute_scheduler.ComputeScheduler (self.api.idata_['scheduler'])

            # register this class instance with the adaptor, to get some
            # persistent state.
            self.adaptor.adata['cus'][self.id]['scheduler'] = self.scheduler

        else :

            if self.id in self.adaptor.adata['cus'] :
                # we found the id, and reconnect to the class instance, i.e.
                # re-create the class state.
                print "troy_adaptor_default_cus : will re-use existing instance " + id
                self.scheduler = self.adaptor.adata['cus'][self.id]['scheduler']

            else : 
                # The CUS instance was created by another adaptor.
                raise troy.pilot.TroyException (troy.pilot.Error.BadParameter, 
                      "Cannot handle id")




    def add_compute_pilot (self, cp) :
        """ Add a ComputePilot to this CUS.

            Keyword arguments:
            cp -- The ComputePilot to which this ComputeUnitService will connect.
        """
        self.api.idata_['pilots'].append (cp)


    def list_compute_pilots (self) :

        ret = []
        for cp in self.api.idata_['pilots'] :
            ret.append (cp.id)

        return ret


    def remove_compute_pilot (self, cp) :
        """ Remove a ComputePilot

            Note that it won't cancel the ComputePilot, it will just no longer
            receive any CUs

            Keyword arguments:
            cp -- The ComputePilot to remove 
        """
        self.api.idata_['pilots'].remove (cp)



    def submit_compute_unit (self, cud) :
        """ Submit a CU to this ComputeUnitService.

            Keyword argument:
            cud -- The ComputeUnitDescription from the application

            Return:
            ComputeUnit object

            This method is not implemented
        """
        self.api.dump_ ()
        return self.scheduler.schedule (self.api, cud)


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# Data API
#

########################################################################
class default_dus (troy.interface.iDataUnitService) :

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


    def wait (self) :
        """ Wait until DUS enters a final state """
        raise troy.pilot.TroyException (troy.pilot.Error.NotImplemented, "method not implemented!")

    
    def cancel (self) :
        """ Cancel the DUS.
            
            Cancelling the DUS also cancels all the DUs submitted to it.
        """
        raise troy.pilot.TroyException (troy.pilot.Error.NotImplemented, "method not implemented!")


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# Compute-Data API
#

########################################################################
class default_dcus (troy.interface.iComputeDataUnitService) :

    def __init__ (self, api, adaptor) :
        raise troy.pilot.TroyException (troy.pilot.Error.NotImplemented, "method not implemented!")

