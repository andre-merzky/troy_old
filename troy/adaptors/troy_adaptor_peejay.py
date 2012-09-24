
import imp
import urlparse
import traceback
import threading
from   time import sleep

import troy
import troy.interface
from   troy.adaptors.base import aBase
from   troy.exception     import Exception, Error


########################################################################
# 
# FIXME: try/except on all backend interactions
# 


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
    
    ########################################################################
    # we need a thread per adaptor instance which watches (== polls) for pilot 
    # and job state changes
    #
    def peejay_watcher_ (self) :

        while True :
            for pilot_id in self.watch['cp'] :
                pilot = self.watch['cp'][pilot_id]
                state = pilot._sync_backend_state () 
            for job_id in self.watch['cu'] :
                pilot = self.watch['cu'][job_id]
                state = pilot._sync_backend_state () 
            sleep (1)


    def __init__ (self) :
        
        # duh!
        self.name     = 'troy_adaptor_peejay'

        # The registry maps api interface classes to the adaptor classes 
        # implementing them:
        self.registry = {'PilotFramework' : 'peejay_pf' ,
                         'ComputePilot'   : 'peejay_cp' ,
                         'ComputeUnit'    : 'peejay_cu' ,
                         'Base'           : 'peejay_pf' ,
                         'Base'           : 'peejay_cp' ,
                         'Base'           : 'peejay_cu' }
        
        # This adaptor does not keep state, as all peejay entities are easily
        # and cheaply reconnectable.  
        #
        # self.adata = {}

        # We keep, however, a list of peejay CUs and
        # CPs watch in the watcher thread
        self.watch = { 'cp' : {},
                       'cu' : {} }

        self.watcher = threading.Thread (target = self.peejay_watcher_)
        self.watcher.setDaemon (True)
        self.watcher.start ()



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
    

    # # for each api object, we register our adaptor data.  That way, the adata
    # # will be available in all adaptor level calls (each belonging to exactly
    # # one api class instance).
    # def register_adata (self, api) :
    #
    #     api._idata[self.get_name ()] = self.adata
    #     return self.adata


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

        master_id = elems.path.lstrip ('/')

        if master_id != '' :
            # we MUST interpret pf_id, if present
            # FIXME: try/except
            self.master = self.peejay.master (master_id)

            # we need to make sure that this CU instance has all required attributes
            self.api['pilots'] = self.master.list_pilots ()
            self.api['units']  = self.master.list_jobs ()

        else :
            # Otherwise, we go ahead and create a new master

            self.master = self.peejay.master ()
            self.api.id = 'peejay:///' + self.master.get_id ()


    def _push_state (self, obj, key) :
        pass

    def _pull_state (self, obj, key) :
        self._sync_backend_state ()

    def _sync_backend_state (self) :
        pass

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

        # create pilot, and register with framework
        ret =  troy.ComputePilot (pilot_id)
        self.api['pilots'].append (pilot_id)

        return ret


    def list_pilots (self) :
        return self.api['pilots']


    def cancel (self) :

        for job_id in  self.api['units'] :
            print " ---> " + job_id
            job = troy.ComputeUnit (job_id)
            job.cancel ()

        for pilot_id in  self.api['pilots'] :
            print " ---> " + pilot_id
            pilot = troy.ComputePilot (pilot_id)
            pilot.cancel ()



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

        elems = urlparse.urlparse (self.api.id)
        if elems.scheme != '' and   \
           elems.scheme != 'peejay' :
            raise troy.Exception (troy.Error.BadParameter, 
                  "can only handle peejay:// URLs, not " + elems.scheme + "://")

        pilot_id = elems.path.lstrip ('/')

        if pilot_id == '' :
            # we MUST have an ID to connect to
            raise troy.Exception (troy.Error.BadParameter, 
                "cannot reconnect to CP - invalid (empty) id")

        self.pilot   = self.peejay.pilot (pilot_id)
        self.running = 1

        # we need to make sure that this CU instance has all required attributes
        self._sync_backend_state ()
        # sets self.api.state
        # sets self.api.state_detail
        
        self.api.framework   = self.pilot.get_master_id   ()
        self.api.description = self.pilot.get_description ()
        self.api.units       = self.pilot.list_jobs       ()


        # make sure that this CP instance is watched by the adaptor's watcher
        # thread
        if not self.api.id in self.adaptor.watch['cp'] :
            self.adaptor.watch['cp'][self.api.id] = self


    def _push_state (self, obj, key) :
        pass

    def _pull_state (self, obj, key) :
        self._sync_backend_state ()


    def _sync_backend_state (self) :
        """ sync api level state with backend state """
        s = self.pilot.get_state ()

        if   s == self.peejay.state.Unknown  : ret = troy.State.Unknown 
        elif s == self.peejay.state.New      : ret = troy.State.New     
        elif s == self.peejay.state.Pending  : ret = troy.State.Pending 
        elif s == self.peejay.state.Running  : ret = troy.State.Running 
        elif s == self.peejay.state.Done     : ret = troy.State.Done    
        elif s == self.peejay.state.Canceled : ret = troy.State.Canceled
        elif s == self.peejay.state.Failed   : ret = troy.State.Failed  
        else                                 : ret = troy.State.Unknown 

        self.api.state        = ret
        self.api.state_detail = s

        return ret

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

        # store description for the cu instance
        job.description = cud
        job.pilot       = self.api.id
        job.framework   = self.api.framework

        # register cu for later state checks etc.
        self.api.attributes_dump_ ()
        self.api['units'].append (job_id)

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

        self.api.attributes_dump_ ()
        self.job = self.peejay.job (self.api.id)

        # we need to make sure that this CU instance has all required attributes
        self._sync_backend_state ()
        # sets self.api.state
        # sets self.api.state_detail

        self.api.pilot       = self.job.get_pilot_id ()
        self.api.framework   = self.job.get_master_id ()
        self.api.description = self.job.get_description ()

        # make sure that this CU instance is watched by the adaptor's watcher
        # thread
        if not self.api.id in self.adaptor.watch['cu'] :
            self.adaptor.watch['cu'][self.api.id] = self


    def _push_state (self, obj, key) :
        pass

    def _pull_state (self, obj, key) :
        self._sync_backend_state ()


    def _sync_backend_state (self) :
        """ sync api level state with backend state """
        s = self.job.get_state ()

        if   s == self.peejay.state.Unknown  : ret = troy.State.Unknown 
        elif s == self.peejay.state.New      : ret = troy.State.New     
        elif s == self.peejay.state.Pending  : ret = troy.State.Pending 
        elif s == self.peejay.state.Running  : ret = troy.State.Running 
        elif s == self.peejay.state.Done     : ret = troy.State.Done    
        elif s == self.peejay.state.Canceled : ret = troy.State.Canceled
        elif s == self.peejay.state.Failed   : ret = troy.State.Failed  
        else                                 : ret = troy.State.Unknown 

        self.api.state        = ret
        self.api.state_detail = s

        return ret


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

