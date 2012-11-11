
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
# This is a skeleton adaptor for pilot framework backends.
# 
########################################################################


########################################################################
#
# main adaptor class, registers the implementation with troy upon loading
#
class adaptor (aBase) :
    
    ########################################################################
    # we want a thread per adaptor instance which watches (== polls) for pilot 
    # and job state changes.  Backends with asynchronous notification won't have
    # to do that.
    #
    # We add poller calls for all stateful troy objects.  init needs to make
    # sure that the respective lists are in place.
    #
    def skeleton_watcher_ (self) :

        while True :

            for pilot_id in self.watch['cp'] :
                pilot = self.watch['cp'][pilot_id]
                state = pilot.sync_backend_state () 

            for job_id in self.watch['cu'] :
                pilot = self.watch['cu'][job_id]
                state = pilot.sync_backend_state () 

            for pilot_id in self.watch['dp'] :
                pilot = self.watch['dp'][pilot_id]
                state = pilot.sync_backend_state () 

            for job_id in self.watch['du'] :
                pilot = self.watch['du'][job_id]
                state = pilot.sync_backend_state () 

            sleep (1)


    ########################################################################
    # we want a thread per adaptor instance which watches (== polls) for pilot 
    # and job state changes
    #
    def __init__ (self) :
        
        # duh!
        self.name     = 'troy_adaptor_skeleton'

        # The registry maps api interface classes to the adaptor classes 
        # implementing them.  Note that we need to add Base, as the registration
        # will no automatically register the base classes (yet).
        self.registry = {'PilotFramework' : 'skeleton_pf' ,

                         'ComputePilot'   : 'skeleton_cp' ,
                         'ComputeUnit'    : 'skeleton_cu' ,

                         'DataPilot'      : 'skeleton_dp' ,
                         'DataUnit'       : 'skeleton_du' ,

                         'Base'           : 'skeleton_pf' ,
                         'Base'           : 'skeleton_cp' ,
                         'Base'           : 'skeleton_cu' , 
                         'Base'           : 'skeleton_dp' ,
                         'Base'           : 'skeleton_du' }
        
        # We assume that this adaptor does not keep state, as all skeleton
        # entities are easily and cheaply reconnectable.  So, no need to keep
        # any adaptor_data around.  Some object state will be cached on API
        # object level however.
        #
        # self.adata = {}

        # We keep, however, a list of objects to be watched in the the watcher
        # thread
        self.watch = { 'cp' : {} ,
                       'cu' : {} ,
                       'dp' : {} ,
                       'du' : {} }

        # create the watcher thread.  This could in principle be delayed until
        # the first object gets created.
        self.watcher = threading.Thread (target = self.skeleton_watcher_)
        self.watcher.setDaemon (True)
        self.watcher.start ()



    ############################################################################
    #
    def sanity_check (self) :
        # raise troy.Exception (Error.NoSuccess, "adaptor disabled")
        
        # try lo load your backend python module, check for the version, and
        # moon phase, check if pi is still normal, or whatever.  If it looks
        # like the universe disagrees with you, and this adaptor will not be
        # able to run, raise a 'UniverseMismatch' exception.  Or
        # 'Error.NoSuccess' if you are shy.
        #
        # If you load a module here, you may want to keep it around for usage.
        # Do *not* import the module -- that will screw up not only this adaptor
        # on failure, but in fact all of Troy.
        #
        # To disable this adaptor, obviously throw with a sensible error.
        #
        # For the purpose of this skeleton adaptor, we load a dummy backend
        # module.
        try :
            (f, p, d)    = imp.find_module ('peejay', ['/home/merzky/saga/peejay/'])
            self.backend = imp.load_module ('backend', f, p, d)

        except Exception as e :
            print ' could not load skeleton adaptor: ' + str (e)
            raise troy.Exception (Error.NoSuccess, '1 > 2 : not good.')



    ############################################################################
    #
    # for each api object, we can register adaptor state information.  That way,
    # the adata will be available in all adaptor level calls (each belonging to
    # exactly one api class instance).  An example would be to cache
    # a connection object for an ssh job instance
    #
    def register_adata (self, api) :
    
        api._idata[self.get_name ()] = self.adata
        return self.adata


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# Pilot Framework
#
########################################################################
class skeleton_pf (troy.interface.iPilotFramework) :


    ############################################################################
    #
    def __init__ (self, api, adaptor) :

        self.api     = api 
        self.adaptor = adaptor
        self.backend = self.adaptor.backend

        # we accept two types of id URLs: complete and incomplete ones.
        # Complete ones (skeleton:///path) are interpreted as ID, and are used
        # to reconnect to a pf instance.  Incomplete ones (skeleton://) are
        # interpreted as request to create a new instance.  IDs which are not
        # handled by this adaptor should cause a 'BadParameter' exception.

        # default, so that we can handle calls with empty IDs.  If this adaptor
        # should not handle those, raise a BadParameter on empty IDs.
        id = 'skeleton://'  

        if 'id' in self.api :
            id = self.api.id

        elems = urlparse.urlparse (id)
        if elems.scheme != '' and   \
           elems.scheme != 'skeleton' :
            raise troy.Exception (troy.Error.BadParameter, 
                  "can only handle skeleton:// URLs, not " + elems.scheme + "://")

        pf_id = elems.path.lstrip ('/')

        if pf_id != '' :
            # we MUST interpret pf_id, if present
            # FIXME: try/except
            self.pf = self.backend.pilot_framework (pf_id)

            # we need to make sure that this CU instance has all required
            # attributes.  See :class:`troy.PilotFramework` for details.
            self.api['pilots'] = self.pf.list_pilots ()
            self.api['units']  = self.pf.list_jobs ()

        else :
            # Otherwise, we go ahead and create a new pf

            self.pf     = self.backend.backend_framework ()
            self.api.id = 'skeleton:///' + self.pf.get_id ()

            # we need to make sure that this CU instance has all required
            # attributes.  See :class:`troy.PilotFramework` for details.
            self.api['pilots'] = []
            self.api['units']  = []



    ############################################################################
    #
    # synchronize troy level state changes with the backend
    #
    def push_state (self, obj, key) :
        # nothing to do here
        pass


    ############################################################################
    #
    # synchronize backend level state changes with troy (on state queries)
    #
    def pull_state (self, obj, key) :
        # this really should be implemented by the adaptor
        self.sync_backend_state ()


    ############################################################################
    #
    def sync_backend_state (self) :
        # well, nothing to do in this skeleton adaptor...
        pass

    
    ############################################################################
    #
    # below are the adaptor implementations for the pilot framework methods.  
    #
    def submit_pilot (self, pd) :
        """ Add a ComputePilot to the ComputePilotFramework

            Keyword arguments:
            cpd     -- ComputePilot Description

            Return value:
            A ComputePilot handle
        """

        # TODO: do some parameter check here.  Like, check if the pd is
        # a ComputeUnitDescription or DataUnitDescription, to create the right
        # kind of pilot.
        
        # create a backend pilot instance
        pilot     = self.adaptor.backend.run_pilot ()

        # determine the ID of the pilot
        pilot_id  = 'skeleton:///' + str (pilot.get_id ())

        # create an troy level pilot object
        obj =  troy.ComputePilot (pilot_id)

        # register that id (and thus the instance) in the PF instance data.
        # That way, any other PF adaptor can get a list of pilots managed by
        # this PF instance.
        # See :class:`troy.PilotFramework` for details on the available instance
        # data
        self.api['pilots'].append (pilot_id)

        # return the API object to the application
        return obj


    ############################################################################
    #
    # def submit_unit (self, ud) :
    #     This skeleton adaptor does not allow to submit units to the pf
    #     directly, but only to the pilots.


    ############################################################################
    #
    def list_pilots (self) :
        return self.api['pilots']


    ############################################################################
    #
    def list_units (self) :
        # NOTE: even if this adaptor does not submit units to the pf directly, 
        # the units list will in general be filled by the pilots.
        return self.api['units']


    ############################################################################
    #
    def cancel (self) :

        # the cancel semantics requires us to also cancel all jobs, and all
        # pilots.
        #
        # FIXME: the code below needs to also handle data units and data pilots
        #
        # NOTE: even if this adaptor does not submit units to the pf directly, 
        # the units list will in general be filled by the pilots.
        for job_id in  self.api['units'] :
            job = troy.ComputeUnit (job_id)
            job.cancel ()

        for pilot_id in  self.api['pilots'] :
            print " ---> " + pilot_id
            pilot = troy.ComputePilot (pilot_id)
            pilot.cancel ()

        # cancel the backend framework as requested
        self.pf.cancel ()



#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# Compute API
#

########################################################################
class skeleton_cp (troy.interface.iComputePilot) :

    ############################################################################
    #
    def __init__ (self, api, adaptor) :

        self.api      = api 
        self.adaptor  = adaptor
        self.backend  = self.adaptor.backend

        # we MUST interpret cp_id, if present.  In fact, we need to have an id,
        # as creation is always done in the CPF
        if not 'id' in self.api or not self.api.id :
            raise troy.Exception (troy.Error.NoSuccess, 
                    "skeleton needs an id to reconnect to a pilot")

        elems = urlparse.urlparse (self.api.id)

        if elems.scheme != '' and   \
           elems.scheme != 'skeleton' :
            raise troy.Exception (troy.Error.BadParameter, 
                  "can only handle skeleton:// URLs, not " + elems.scheme + "://")

        pilot_id = elems.path.lstrip ('/')

        # we MUST have an ID to connect to -- an empty ID would trigger the
        # creation of pilots, but that is taken care of in skeleton_pf.
        if pilot_id == '' :
            raise troy.Exception (troy.Error.BadParameter, 
                "cannot reconnect to CP - invalid (empty) id")

        self.pilot = self.backend.pilot (pilot_id)

        # we need to make sure that this CU instance has all required
        # attributes, so pull state from backend once.
        self.sync_backend_state ()
        
        self.api.framework   = self.pilot.get_master_id   ()
        self.api.description = self.pilot.get_description ()
        self.api.units       = self.pilot.list_jobs       ()


        # make sure that this CP instance is watched by the adaptor's watcher
        # thread
        if not self.api.id in self.adaptor.watch['cp'] :
            self.adaptor.watch['cp'][self.api.id] = self


    ############################################################################
    #
    def push_state (self, obj, key) :
        pass


    ############################################################################
    #
    def pull_state (self, obj, key) :
        self.sync_backend_state ()


    ############################################################################
    #
    def sync_backend_state (self) :
        """ 
        sync api level state with backend state.

        This method can potentially be called very often, so it is advisable to
        cache the state for some amount of time.
        """
        s = self.pilot.get_state ()

        if   s == self.backend.state.Unknown  : ret = troy.State.Unknown 
        elif s == self.backend.state.New      : ret = troy.State.New     
        elif s == self.backend.state.Pending  : ret = troy.State.Pending 
        elif s == self.backend.state.Running  : ret = troy.State.Running 
        elif s == self.backend.state.Done     : ret = troy.State.Done    
        elif s == self.backend.state.Canceled : ret = troy.State.Canceled
        elif s == self.backend.state.Failed   : ret = troy.State.Failed  
        else                                  : ret = troy.State.Unknown 

        self.api.state        = ret
        self.api.state_detail = s

        return ret


    ############################################################################
    #
    def is_final (self) :
        """ 
        Check if the job reached a final state.  
        We consider Unknown states to be final. 
        """

        sync_backend_state ()

        if   self.api.state == troy.State.Unknown  : return False
        elif self.api.state == troy.State.New      : return False
        elif self.api.state == troy.State.Pending  : return False
        elif self.api.state == troy.State.Running  : return False
        elif self.api.state == troy.State.Done     : return True
        elif self.api.state == troy.State.Canceled : return True
        elif self.api.state == troy.State.Failed   : return True
        else                                       : return True


    ############################################################################
    #
    def submit_unit (self, cud) :
        """
        Create a compute unit
        
        Just as a pf uses a pilot description to create a pilot, this pilot
        uses a compute unit description to create a compute unit -- the code
        looks very similar.
        """

        if not 'executable' in cud :
            raise troy.Exception (troy.Error.NoSuccess, 
                    "executable missing in compute unit description!")

        job      = self.pilot.compute (cmd)
        job_id   = str (job.get_id ())

        # store description for the cu instance
        job.description = cud
        job.pilot       = self.api.id
        job.framework   = self.api.framework

        # register cu for later state checks etc.
        self.api._attributes_dump ()
        self.api['units'].append (job_id)

        return troy.ComputeUnit (job_id)


    ############################################################################
    #
    def wait (self) :
        """ Wait until CP enters a final state """
        if self.is_final () :
            # job is final, so there is no point in waiting
            return

        self.pilot.wait ()


    ############################################################################
    #
    def cancel (self) :
        """ 
        Cancel the pilot, and unregister it from the pilot framework
        """

        if not self.is_final () :
            self.pilot.kill ()

        # make sure it is dead
        self.pilot.wait ()


    ############################################################################
    #
    def reinitialize (self, cpd) :
        """ 
        This method is not implemented.  It is actually not necessary to add the
        code for the method and to raise an exception -- if the method is not
        available at all, the interface will raise an exception.
        """

        raise troy.Exception (troy.Error.NotImplemented, "method not implemented!")


########################################################################
class skeleton_cu (troy.interface.iComputeUnit) :

    ############################################################################
    #
    def __init__ (self, api, adaptor) :

        self.api     = api 
        self.adaptor = adaptor
        self.backend  = self.adaptor.backend

        # we MUST interpret cu_id, if present.  In fact, we need to have an id,
        # as creation is always done in the CUS
        if not 'id' in self.api or not self.api.id :
            raise troy.Exception (troy.Error.NoSuccess, 
                    "skeleton needs an id to reconnect to a cu")

        self.api._attributes_dump ()
        self.job = self.backend.job (self.api.id)

        # we need to make sure that this CU instance has all required attributes
        self.sync_backend_state ()
        # sets self.api.state / self.api.state_detail

        self.api.pilot       = self.job.get_pilot_id    ()
        self.api.framework   = self.job.get_master_id   ()
        self.api.description = self.job.get_description ()

        # make sure that this CU instance is watched by the adaptor's watcher
        # thread
        if not self.api.id in self.adaptor.watch['cu'] :
            self.adaptor.watch['cu'][self.api.id] = self


    ############################################################################
    #
    def push_state (self, obj, key) :
        pass

    ############################################################################
    #
    def pull_state (self, obj, key) :
        self.sync_backend_state ()


    ############################################################################
    #
    def sync_backend_state (self) :
        """ sync api level state with backend state """
        s = self.job.get_state ()

        if   s == self.backend.state.Unknown  : ret = troy.State.Unknown 
        elif s == self.backend.state.New      : ret = troy.State.New     
        elif s == self.backend.state.Pending  : ret = troy.State.Pending 
        elif s == self.backend.state.Running  : ret = troy.State.Running 
        elif s == self.backend.state.Done     : ret = troy.State.Done    
        elif s == self.backend.state.Canceled : ret = troy.State.Canceled
        elif s == self.backend.state.Failed   : ret = troy.State.Failed  
        else                                  : ret = troy.State.Unknown 

        self.api.state        = ret
        self.api.state_detail = s

        return ret


    ############################################################################
    #
    def wait (self) :
        """ Wait until CU enters a final state """
        self.job.wait ()


    ############################################################################
    #
    def cancel (self) :
        """ Cancel the CU """
        self.job.cancel ()

    
    ############################################################################
    #
    def set_callback (self, member, cb) :
        """ Set a callback function for a member.

            Keyword arguments:
            member -- The member to set the callback for (state / state_detail).
            cb     -- The callback object to call.
        """
        raise troy.Exception (troy.Error.NotImplemented, "method not implemented!")

    
    ############################################################################
    #
    def unset_callback (self, member) :
        """ Unset a callback function from a member

            Keyword arguments:
            member -- The member to unset the callback from.
        """
        raise troy.Exception (troy.Error.NotImplemented, "method not implemented!")


# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

