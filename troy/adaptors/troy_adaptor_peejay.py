
import imp
import urlparse
import traceback

import troy
import troy.interface
from   troy.adaptors.base import aBase
from   troy.exception     import Exception, Error


########################################################################
# 
# This TROY adaptor interfaces to peejay, a minimal P* aligned PJ (doh!) 
# implementation -- see https://github.com/andre-merzky/peejay
#


########################################################################
#
# main adaptor class, registers the implementation with troy upon loading
#
class adaptor (aBase) :
    
    def __init__ (self) :
        
        # duh!
        self.name     = 'troy_adaptor_peejay'

        # The registry maps api interface classes to the adaptor classes 
        # implementing them:
        self.registry = {'PilotFramework'            : 'peejay_pf'  ,

                         'ComputePilot'              : 'peejay_cp'  ,
                         'ComputeUnit'               : 'peejay_cu'  , 

                         'DataPilot'                 : 'peejay_dp'  ,
                         'DataUnit'                  : 'peejay_du'  }
        
        # The adaptor_data keeps links between all id's and backend instances.
        # It is also use to maintain any other adaptor level state.
        self.adata = { 'pf'  : {},
                       'cp'  : {}, 
                       'cu'  : {} }


    def get_name (self) :
        return self.name

    def get_registry (self) :
        return self.registry

    def get_order (self) :
        return 2

    def sanity_check (self) :
        # raise troy.Exception (Error.NoSuccess, "adaptor disabled")
        
        # try lo load peejay
        try :
            (f, p, d)   = imp.find_module ('peejay', ['/home/merzky/saga/peejay/'])
            self.module = imp.load_module ('peejay', f, p, d)
        except Exception as e :
            print ' ======== could not load peejay adaptor: ' + str (e)
            raise troy.Exception (Error.NoSuccess, 'Could not load the peejay module')

        # Hey, we can use peejay objects now!  Like this:
        # self.module.state.New

        # FIXME: disable module for now, so that we can test bigjob :P
        # raise troy.Exception (Error.NoSuccess, 'disabling peejay adaptor')
    

    # for each api object, we register our adaptor data.  That way, the adata
    # will be available in all adaptor level calls (each belonging to exactly
    # one api class instance).
    def register_adata (self, api) :

        if not 'idata_' in api :
            api.idata_ = {}

        api.idata_[self.get_name ()] = self.adata
        return self.adata


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# Compute API
#

########################################################################
class peejay_pf (troy.interface.iPilotFramework) :

    def __init__ (self, api, adaptor) :

        self.api     = api 
        self.adaptor = adaptor
        self.peejay  = self.adaptor.module

        # we accept two types of id URLs: complete and incomplete ones.
        # Complete ones (peejay:///path) are interpreted as ID, and are used to
        # reconnect to a master.  Incomplete ones (peejay://) are interpreted as
        # request to create a new master.

        id = 'peejay://'  # default on empty id

        if 'id' in self.api :
            id = self.api.id

        elems = urlparse.urlparse (id)
        if elems.scheme != '' and   \
           elems.scheme != 'peejay' :
            raise troy.Exception (troy.Error.BadParameter, 
                  "can only handle peejay:// URLs, not " + elems.scheme + "://")

        if elems.path != '' :
            # we MUST interpret pf_id, if present
            if not id in self.adaptor.adata['pf'] :
                raise troy.Exception (troy.Error.BadParameter, 
                      "cannot reconnect to PF - invalid id")
            self.master = self.adaptor.adata['pf'][id]

        else :
            # Otherwise, we go ahead and create a new master

            self.master = self.peejay.master ()
            self.api.id = 'peejay:///' + self.master.get_id ()
            self.adaptor.adata['pf'][self.api.id] = self.master

        # if we got this far, we can now register adaptor level instance data in
        # the api.  
        self.adata = self.adaptor.register_adata (self.api)


    def submit_pilot (self, cpd) :
        """ Add a ComputePilot to the ComputePilotFramework

            Keyword arguments:
            cpd     -- ComputePilot Description

            Return value:
            A ComputePilot handle
        """

        # FIXME: add param checks
        pilot     = self.master.run_pilot ()
        pilot_id  = 'peejay:///' + str (pilot.get_id ())

        # register pilot for later use
        self.adata['cp'][pilot_id] = pilot

        return troy.ComputePilot (pilot_id)

    def list_pilots (self) :
        ids = self.adata['cp'].keys ()
        return self.adata['cp'].keys ()



########################################################################
class peejay_cp (troy.interface.iComputePilot) :

    def __init__ (self, api, adaptor) :

        self.api     = api 
        self.adaptor = adaptor
        self.peejay  = self.adaptor.module

        # we MUST interpret cp_id, if present.  In fact, we need to have an id,
        # as creation is always done in the CPF
        if not 'id' in self.api or not self.api.id :
            raise troy.Exception (troy.Error.NoSuccess, 
                    "peejay needs an id to reconnect to a pilot")

        self.id = self.api.id

        elems = urlparse.urlparse (self.api.id)
        if elems.scheme != '' and   \
           elems.scheme != 'peejay' :
            raise troy.Exception (troy.Error.BadParameter, 
                  "can only handle peejay:// URLs, not " + elems.scheme + "://")

        if elems.path == '' :
            # we MUST have an ID to connect to
            raise troy.Exception (troy.Error.BadParameter, 
                "cannot reconnect to CP - invalid id")

        self.pilot   = self.peejay.pilot (elems.path)
        self.running = 1

        # if we got this far, we can now register adaptor level instance data in
        # the api.  
        self.adata = self.adaptor.register_adata (self.api)


    def submit_unit (self, cud) :
        """ Submit a CU to this Pilot.

            Keyword argument:
            cud -- The ComputeUnitDescription from the application

            Return:
            ComputeUnit object
        """
        # build command from cud
        cmd = ""

        if not 'executable' in cud :
            raise troy.Exception (troy.Error.NoSuccess, 
                    "executable missing in compute unit description!")


        if 'environment' in cud :
            cmd += '/bin/env'
            for env in cud['environment'] :
                cmd += ' ' + env
            cmd += ' '

        cmd += cud['executable']

        if 'arguments' in cud :
            for arg in cud['arguments'] :
                cmd += ' "' + arg + '"'

        job      = self.pilot.job_submit (cmd)
        job_id   = str (job.get_id ())

        # register cu for later state checks etc.
        self.adata['cu'][job_id] = job

        return troy.ComputeUnit (job_id)


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
        raise troy.Exception (troy.Error.NotImplemented, "method not implemented!")


    def set_callback (self, member, cb) :
        """ Set a callback function for a member.

            Keyword arguments:
            member -- The member to set the callback for (state / state_detail / wall_time_left).
            cb     -- The callback object to call.
        """
        if not self.running :
            raise troy.Exception (troy.Error.IncorrectState, 
                    "cannot attach callback to dead pilot!")

        raise troy.Exception (troy.Error.NotImplemented, "method not implemented!")


    def unset_callback (self, member) :
        """ Unset a callback function from a member

            Keyword arguments:
            member -- The member to unset the callback for (state / state_detail / wall_tim_left).
        """
        if not self.running :
            raise troy.Exception (troy.Error.IncorrectState, 
                    "cannot remove callback from dead pilot!")

        raise troy.Exception (troy.Error.NotImplemented, "method not implemented!")
    



# ########################################################################
# class peejay_cus (troy.interface.iComputeUnitService) :
# 
#     cus_index = 0
# 
#     def __init__ (self, api, adaptor) :
# 
#         self.api     = api 
#         self.adaptor = adaptor
#         self.peejay  = self.adaptor.module
#         self.cpf     = []  # list of associated compute pilot services
# 
# 
#         peejay_cus.cus_index += 1
#         self.id      = str (peejay_cus.cus_index)
# 
#         # we MUST interpret cus_id, if present.  But in fact, peejay does not
#         # have a CUS, so we cannot, ever, reconnect to a CUS.  So, we have to
#         # throw if an id is present
#         # as creation is always done in the CPF
#         if 'id' in self.api and self.api.id :
#             raise troy.Exception (troy.Error.NoSuccess, 
#                                             "peejay cannot reconnect to CUS!")
# 
#         # we need a scheduler.  There is no way for the API to re-init or
#         # re-assign a scheduler after the CUS has been created -- the scheduler
#         # is fully internal -- so we can just create it here.  For now, we use
#         # the 'Random' scheduler
#         self.scheduler = troy.ComputeScheduler ('Random')
# 
#         # if we got this far, we can now register adaptor level instance data in
#         # the api.  
#         self.adata = self.adaptor.register_adata (self.api)
# 
#         # register the pilot after creation
#         self.adata ['cus'][self.id] = self
# 
# 
# 
#     def get_id (self) :
#         return self.id
# 
#     # def submit_unit (self, cud) :
#     #     self.scheduler.schedule (self.api, cud)
# 
# 
#     def add_pilot_framework (self, cpf) :
#         """ Add a ComputePilotFramework to this CUS.
# 
#             Keyword arguments:
#             cpf -- The ComputePilotFramework to which this ComputeUnitService will connect.
#         """
#         self.cpf.append (cpf)
# 
# 
#     def list_pilot_frameworks (self) :
#         """ List all CPFs of CUS """
# 
#         ret = []
# 
#         for cpf in self.cpf :
#             ret.append (cpf.id)
# 
#         return ret
# 
# 
#     def remove_pilot_framework (self, cpf) :
#         """ Remove a ComputePilotFramework
# 
#             Note that it won't cancel the ComputePilotFramework, it will just no longer
#             receive any CUs.
# 
#             Keyword arguments:
#             cpf -- The ComputePilotFramework to remove 
#         """
#         self.cp.remove (cp)


########################################################################
class peejay_cu (troy.interface.iComputeUnit) :

    def __init__ (self, api, adaptor) :

        self.api     = api 
        self.adaptor = adaptor
        self.peejay  = self.adaptor.module

        # we MUST interpret cu_id, if present.  In fact, we need to have an id,
        # as creation is always done in the CUS
        if not 'id' in self.api or not self.api.id :
            raise troy.Exception (troy.Error.NoSuccess, 
                    "peejay needs an id to reconnect to a cu")

        self.id = self.api.id

        # if we got this far, we can now register adaptor level instance data in
        # the api.  
        self.adata = self.adaptor.register_adata (self.api)
        self.job   = self.adata['cu'][self.id]



    def get_state (self) :
        """ return the current state """
        s = self.job.get_state ()

        if   s == self.peejay.state.Unknown  : return troy.State.Unknown 
        elif s == self.peejay.state.New      : return troy.State.New     
        elif s == self.peejay.state.Pending  : return troy.State.Pending 
        elif s == self.peejay.state.Running  : return troy.State.Running 
        elif s == self.peejay.state.Done     : return troy.State.Done    
        elif s == self.peejay.state.Canceled : return troy.State.Canceled
        elif s == self.peejay.state.Failed   : return troy.State.Failed  
        else                                 : return troy.State.Unknown 


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
        raise troy.Exception (troy.Error.NotImplemented, "method not implemented!")

    
    def unset_callback (self, member) :
        """ Unset a callback function from a member

            Keyword arguments:
            member -- The member to unset the callback from.
        """
        raise troy.Exception (troy.Error.NotImplemented, "method not implemented!")


# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

