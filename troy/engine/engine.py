
import os
import glob
import imp

from troy.pilot.exception import Exception                         
from troy.pilot.exception import Error                         

class Engine:

    # make engine a singleton
    def __new__ (type):
        
        # if instance does not exist (first usage)
        if not '_the_instance' in type.__dict__:
            # then create instance and store in _the_instance
            type._the_instance = object.__new__ (type)
        
        # return the (new or existing) instance on new()
        return type._the_instance


    def __init__(self):

        # __init__ loads all adaptors
        
        # self.adaptors is a dict of dicts.  The inner dicts have two elements:
        # the module containing the adaptor, and an instance of the adaptor
        # class.  The adaptor class is used to inspect the adaptor (find
        # suitable classes etc).  The outer dict maps the inner dicts to
        # a unique adaptor name
        #
        # adaptor = {
        #      troy_adaptor_bigjob : { 'module'  : impl.source (troy_adaptor_bigjob.py)
        #                              'adaptor' : module.adaptor () },
        #      troy_adaptor_diane  : { 'module'  : impl.source (troy_adaptor_diane.py)
        #                              'adaptor' : module.adaptor () },
        #     }
        #
        self.adaptors    = {}
        self.module_path = './troy/adaptors/'  # FIXME: pick from env or ini

        # iterate through modules and load adaptor classes
        for path in glob.glob (self.module_path + '/*/troy_adaptor_*.py'): 

            try:
                print "engine: init: load adaptor: " + path

                name, ext  = os.path.splitext (os.path.basename (path))
                module     = imp.load_source  (name, path)

                # we expect the module to have an 'adaptor' class implemented,
                # which has a 'name', and a 'registry' of implemented API
                # classes
                adaptor    = module.adaptor ()

                if not adaptor.sanity_check () :
                    raise Exception (Error.NoSuccess, "failed sanity check")

                a_name     = adaptor.get_name ()
                a_registry = adaptor.get_registry ()

                self.adaptors[a_name] = {'module'   : module, 
                                         'adaptor'  : adaptor,
                                         'registry' : a_registry}

                print "engine: init: load adaptor: " + path + " done"

            except Exception, e:
                print "engine: init: load adaptor: " + path + " failed:\n  " + str (e)
            



    def call (self, class_name, method_name, api_class, *args, **kwargs):
        '''call an adaptor function, for the given class/method, and give as
           args the object state (extracted from api_class), and the method args
        '''

        # for all known adaptors, find those who implement the requested class
        valid_adaptors = []

        for a_name in self.adaptors.keys () :

            adaptor    = self.adaptors[a_name]['adaptor']
            a_registry = self.adaptors[a_name]['registry']

            if class_name in a_registry:

                valid_adaptors.append (a_name)



        # for all those valid adaptor classes, try to find one which can run 
        # the requested # method successfully.
        #
        # FIXME: a necessary optimization (i.e. not premature optimization) is
        # to *first* try to re-use previously successful adaptors.  For that
        # purpose, the list of adaptor class instances managed by the api_class
        # should be sorted, and 'good' adaptors should be on top.  New adaptor
        # class instances should only be created once that list cycled through
        # w/o success. 
        # 
        # FIXME: further, before attempting to create a adaptor class instance,
        # the adaptor instance should be called to check if it is applicable.
        # For example, a URL scheme match could be performed for some classes,
        # if applicable.  That check should operate on the api class instance
        # data.
        # 
        e_stack = "";

        for a_name in valid_adaptors :

            try:
              adaptor    = self.adaptors[a_name]['adaptor']
              module     = self.adaptors[a_name]['module']
              a_registry = self.adaptors[a_name]['registry']
              a_class    = a_registry[class_name]  # name of adaptor class
                                                   # implementing the requested 
                                                   # api class

              # this module/adaptor combo should work.  Now we have to check if
              # the api class used that one before - and if so, we reuse the
              # adaptor class instance.  If not, we have to create a new one
              # before actually calling the method
              if not a_name in api_class.adaptors_ :

                  # adaptor has not been used for this api class - create new
                  # adaptor class, and keep it in the api class' list
                  api_class.adaptors_[a_name] = getattr (module, a_class)()

              # adaptor class now exists, and can be used
              print "engine: call: " + a_name + "." + a_class + "." \
                    + method_name + " (" + str (args) + str (kwargs) + ")"

              ret = getattr (api_class.adaptors_[a_name], method_name) (api_class, *args, **kwargs)

              print "engine: call: " + a_name + "." + a_class + "." \
                    + method_name + " (" + str (args) + str (kwargs) + ") : " + str (ret)

              return ret


            except Exception, e:
              print "engine: call: " + a_name + "." + a_class + "." \
                    + method_name + " (" + str (args) + str (kwargs) + ") failed : " \
                    + e.msg
              e_stack = "  " + a_name + " \t: " + str (e) + "\n";

        # no adaptor succeeded
        # FIXME: should re-throw one of the above exceptions
        if e_stack == "" :
          e_stack = "  Bummer, no adaptors loaded.  None at all!"
        # raise Exception (Error.NoSuccess, "no valid adaptor found:\n" + e_stack)        
        print "no valid adaptor found:\n" + e_stack        
        pass

