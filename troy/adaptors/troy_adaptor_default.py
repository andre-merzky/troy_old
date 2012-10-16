
import troy
from   troy.adaptors.base import aBase


########################################################################
#
# This default adaptor only implements the Troy class.  
#
# A major motivation for Troy is to provide application level scheduling, 
# which is provided by scheduler plugins.  This default Troy adaptor 
# manages these plugins, and invokes them as needed.
# 
class adaptor (aBase) :
    
    # 'generator' for serial id's
    serial_ = 0

    def __init__ (self) :
        
        self.name     = 'troy_adaptor_default'
        self.registry = {'Troy' : 'default_troy'}
        self.adata_   = { 'default_troy' : {} }


    def sanity_check (self) :
      # raise troy.Exception (Error.NoSuccess, "adaptor disabled")
        pass


    def get_serial_ (self) :
        adaptor.serial_ += 1
        return adaptor.serial_


########################################################################
class default_troy (troy.interface.iTroy) :

    def __init__ (self, api, adaptor) :

        self.api     = api 
        self.adaptor = adaptor

        self.id = None
        if 'id' in self.api :
            self.id = self.api.id

        # we will only handle this api class if its ID is 'None', or was issued
        # by this adaptor -- otherwise a different adaptor already manages it.
        if self.id == None :

            # id is none - init new instance, assign an id
            self.id = "default_troy_%d"  %  self.adaptor.get_serial_ ()
            self.api.attributes_i_set_ ('id', self.id)

            # register this instance in the adaptor for state persistency
            self.adaptor.adata_['default_troy'][self.id] = self

        else :

            if self.id in self.adaptor.adata_['default_troy'] :
                # we found the id, and reconnect to the class instance, i.e.
                # re-create the class state.
                print "default_troy : will re-use existing instance " + id
                old = self.adaptor.adata_['default_troy'][self.id]
            
                # sync all instance data from that registered version
                self.api.attributes_i_set_ ('id', self.id)
                self.api.attributes_i_set_ ('pilot_frameworks', old.api['pilot_frameworks'])
                self.api.attributes_i_set_ ('schedulers',       old.api['schedulers'])

            else : 
                # The CUS instance was created by another adaptor.
                raise troy.Exception (troy.Error.BadParameter, 
                      "Cannot handle id")


    ############################################################################
    def _push_state (self, obj, key) :
        pass

    def _pull_state (self, obj, key) :
        pass


    ############################################################################
    def add_scheduler (self, bs) :
        """ 
        Add a Backend Scheduler to this Troy instance.

        Keyword arguments:
        bs -- Backend Scheduler to be used by this Troy instance.

        FIXME: bs can be id or instance
        """
        if isinstance (bs, basestring) :
            try :
                instance = troy.BackendScheduler (bs)
                self.api['schedulers'].append (instance)
            except :
                raise troy.Exception (troy.Error.BadParameter, 
                      "Cannot handle bs id")
        elif isinstance (bs, troy.Scheduler) :
            self.api['schedulers'].append (bs)
        else :
            raise troy.Exception (troy.Error.BadParameter, 
                "Cannot handle bs (expected string ID or troy.Scheduler type")


    ############################################################################
    def list_schedulers (self) :
        """ List all Backend Scheduler IDs of this Troy instance """
        ret = []

        for bs in self.api['schedulers'] :
            ret.append (bs.id)

        return ret


    ############################################################################
    def remove_scheduler (self, bs) :
        """ 
        Remove a Scheduler

        Note that it won't cancel the Scheduler nor its pilots -- it will
        just no longer receive any work units from this Troy instance

        Keyword arguments:
        bs -- The Scheduler to remove 
        """
        if isinstance (bs, basestring) :
            try :
                instance = troy.scheduler (bs)
                self.api['schedulers'].remove (instance)
            except :
                raise troy.Exception (troy.Error.BadParameter, 
                      "Cannot handle bs id")
        elif isinstance (bs, troy.Scheduler) :
            self.api['schedulers'].remove (bs)
        else :
            raise troy.Exception (troy.Error.BadParameter, 
                "Cannot handle scheduler (expected string ID or troy.Scheduler type")



    ############################################################################
    def add_pilot_framework (self, pf) :
        """ Add a PilotFramework to this Troy instance.

            Keyword arguments:
            pf -- PilotFramework to be used by this Troy instance.

            FIXME: pf can be id or instance
        """
        if isinstance (pf, basestring) :
            try :
                instance = troy.pilot_framework (pf)
                self.api['pilot_frameworks'].append (instance)
            except :
                raise troy.Exception (troy.Error.BadParameter, 
                      "Cannot handle pf id")
        elif isinstance (pf, troy.PilotFramework) :
            self.api['pilot_frameworks'].append (pf)
        else :
            raise troy.Exception (troy.Error.BadParameter, 
                "Cannot handle pf (expected string ID or troy.PilotFramework type")


    ############################################################################
    def list_pilot_frameworks (self) :
        """ List all PF IDs of this Troy instance """
        ret = []

        for pf in self.api['pilot_frameworks'] :
            ret.append (pf.id)

        return ret


    ############################################################################
    def remove_pilot_framework (self, pf) :
        """ 
        Remove a PilotFramework

        Note that it won't cancel the PilotFramework nor its pilots -- it will
        just no longer receive any work units from this Troy instance

        Keyword arguments:
        pf -- The PilotFramework to remove 
        """
        if isinstance (pf, basestring) :
            try :
                instance = troy.pilot_framework (pf)
                self.api['pilot_frameworks'].remove (instance)
            except :
                raise troy.Exception (troy.Error.BadParameter, 
                      "Cannot handle pf id")
        elif isinstance (pf, troy.PilotFramework) :
            self.api['pilot_frameworks'].remove (pf)
        else :
            raise troy.Exception (troy.Error.BadParameter, 
                "Cannot handle pf (expected string ID or troy.PilotFramework type")



    ############################################################################
    def submit_unit (self, ud) :
        """ 
        Schedule a work unit.

        Now, this adaptor tries one registered scheduler after the other, until
        one is successfully able to submit the unit.  Schedulers MUST throw on
        submission or scheduling failure

        """

        error = ""
        for scheduler in self.api['schedulers'] :
            try :
                return scheduler.schedule (self.api, ud)
            except troy.Exception as e :
                error += "e.msg\n";

        raise troy.Exception (troy.Error.BadParameter, 
            "No scheduler algorithm managed to assign the unit to any of the " + \
            "registered pilot frameworks : " + error)
 
                
    ############################################################################
    def list_units (self) :
        """ list IDs of managed work units.  """
        ret = []

        for pf in self.api['pilot_frameworks'] :
            ret += pf.list_units ()

        return ret
                
    ############################################################################

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

