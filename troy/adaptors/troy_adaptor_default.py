
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
      # raise troy.Exception (troy.Error.NoSuccess, "adaptor disabled")
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
            self.api._attributes_i_set ('id', self.id)

            # register this instance in the adaptor for state persistency
            self.adaptor.adata_['default_troy'][self.id] = self

        else :

            if self.id in self.adaptor.adata_['default_troy'] :
                # we found the id, and reconnect to the class instance, i.e.
                # re-create the class state.
                print "default_troy : will re-use existing instance " + id
                old = self.adaptor.adata_['default_troy'][self.id]

                # sync all instance data from that registered version
                self.api._attributes_i_set ('id', self.id)
                self.api._attributes_i_set ('pilot_frameworks', old.api['pilot_frameworks'])
                self.api._attributes_i_set ('schedulers',       old.api['schedulers'])

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
    def add_scheduler (self, s) :
        """ 
        Add a Backend Scheduler to this Troy instance.

        Keyword arguments:
        s -- Backend Scheduler to be used by this Troy instance.

        """
        if  not   isinstance (s, troy.Scheduler) :
            raise troy.Exception (troy.Error.BadParameter, 
                  "not a troy.Scheduler")

        self.api['schedulers'].append(s)
        

    ############################################################################
    def list_schedulers (self) :
        """ List all Backend Scheduler IDs of this Troy instance """
        ret = []

        for s in self.api['schedulers'] :
            ret.append (s.id)

        return ret


    ############################################################################
    def remove_scheduler (self, s) :
        """ 
        Remove a Scheduler

        Note that it won't cancel the Scheduler nor its pilots -- it will
        just no longer receive any work units from this Troy instance

        Keyword arguments:
        s -- The Scheduler to remove 
        """

        if  not   isinstance (s, troy.Scheduler) :
            raise troy.Exception (troy.Error.BadParameter, 
                  "not a troy.Scheduler")

        self.api['schedulers'].remove (s)


    ############################################################################
    def add_pilot_framework (self, pf) :
        """ Add a PilotFramework to this Troy instance.

            Keyword arguments:
            pf -- PilotFramework to be used by this Troy instance.

            PF can be id or instance
        """
        pf_instance = None

        if isinstance (pf, basestring) :
            try :
                pf_instance = troy.pilot_framework (pf)
            except :
                raise troy.Exception (troy.Error.BadParameter, "Cannot handle pf id")

        elif isinstance (pf, troy.PilotFramework) :
            pf_instance = pf

        else :
            raise troy.Exception (troy.Error.BadParameter, 
                "Cannot handle pf (expected string ID or troy.PilotFramework type")

        self.api['pilot_frameworks'].append (pf_instance)


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
        print "SCHEDULERS:"
        for scheduler in self.api['schedulers'] :
            try :
                return scheduler.schedule (self.api, ud)
            except troy.Exception as e :
                error += str(e) + "\n"

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

