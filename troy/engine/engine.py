
import os
import glob
import imp
import traceback

import troy.exception 


def _EngineSingleton (stype) : 

    instances = {}

    def _EngineSingleton () :

        if stype not in instances :
            instances[stype] = stype ()
        
        return instances[stype]

    _EngineSingleton.__doc__  = stype.__doc__
    _EngineSingleton.__repr__ = stype.__repr__
    
    return _EngineSingleton


@_EngineSingleton
class Engine (object) :

    """
    .. py:class:: troy.engine.Engine (object)

       The Engine singleton class has exactly two tasks in Troy: to (i) load and
       manage Troy adaptors, and to (ii) forward Troy API calls to those
       adaptors.

       The first task (adaptor loading) is performed during initialization (on
       __init__): the engine will search a predefined path, and load all found
       adaptors.  See the Troy `Adaptor Writers Guide`_ for more details on
       adaptor loading and registration.


       The second functionality (call forwarding) is provided by the engine's
       only method, :func:`troy.engine.Engine.call()`, see below.

       **TODO:** make engine search path configurable

    .. py:method:: call (self, class_name, method_name, api_class, *args, **kwargs)

       Call an adaptor methods, for the given class (*class_name*), a given
       method (*method_name*), and pass the calling object's state (derived from
       *api_class*) and method arguments (*\*args*, *\*\*kwargs*).  The Engine
       will iterate over all adaptors registered for that *class_name*, and will
       invoke the adaptor level method on each, until an invocation succeeds
       (i.e. does not raise and exception).  

    """

    ##########################################################################
    # 
    # load all adaptors
    #
    def __init__ (self) :

        # print " === init engine"
        # __init__ loads all adaptors
        
        # self.adaptors is a dict of dicts.  The inner dicts have two elements:
        # the module containing the adaptor, and an instance of the adaptor
        # class.  The adaptor class is used to inspect the adaptor (find
        # suitable classes etc).  The outer dict maps the inner dicts to
        # a unique adaptor name
        #
        # adaptors = {
        #       troy_adaptor_bigjob : 
        #            : { 'module'   : impl.source (troy_adaptor_bigjob.py),
        #                'adaptor'  : module.adaptor (),
        #                'registry' : { troy_api_class : adaptor_bigjob_class } 
        #              },
        #       troy_adaptor_diane : 
        #            : { 'module'   : impl.source (troy_adaptor_diane.py),
        #                'adaptor'  : module.adaptor (),
        #                'registry' : { troy_api_class : adaptor_diane_class } 
        #              }
        #            }
        #
        self.adaptors    = {}
        tuples           = []
        self.module_path = './troy/adaptors/'  # FIXME: pick from env or ini

        # iterate through modules and load adaptor classes
        for path in glob.glob (self.module_path + '/troy_adaptor_*.py') : 

            try :
                print "engine: init: load adaptor: " + path

                name, ext  = os.path.splitext (os.path.basename (path))
                module     = imp.load_source  (name, path)

                # we expect the module to have an 'adaptor' class implemented,
                # which has a 'name', and a 'registry' of implemented API
                # classes
                adaptor    = module.adaptor ()

                # this will throw if the adaptor is not viable
                adaptor.sanity_check ()

                a_priority = adaptor.get_priority ()
                a_name     = adaptor.get_name     ()
                a_registry = adaptor.get_registry ()

                self.adaptors[a_name] = {'module'   : module, 
                                         'adaptor'  : adaptor,
                                         'priority' : a_priority,
                                         'registry' : a_registry}

            except Exception, e :
                # this adaptor failed to load, or failed the sanity check - log
                # error and continute.
                print "engine: init: load adaptor: " + path + " failed:\n  " + str (e)
                # traceback.print_exc ()
                pass

        import pprint
        pprint.pprint (self.adaptors)
            

    ##########################################################################
    # 
    # invoke an adaptor method
    #
    def call (self, class_name, method_name, api_class, *args, **kwargs) :
        '''call an adaptor function, for the given class/method, and give as
           args the object state (extracted from api_class), and the method args
        '''

        # if the api_class is used the first time, sift through loaded adaptors (sorted list)
        if 0 == len (api_class._adaptors) :

            for a_name in self.adaptors.keys () :

                a_registry = self.adaptors[a_name]['registry']
                a_priority = self.adaptors[a_name]['priority']

                # did that adaptor register to handle the class?
                if class_name in a_registry :

                    # if so, add that one to the list of adaptors for that
                    # class.  Initially, the adaptor does not create a adaptor
                    # class instance, so we set that to 'None' -- that is only
                    # created as needed, see below
                    api_class._adaptors [a_name] = {}
                    api_class._adaptors [a_name]['a_class']  = None
                    api_class._adaptors [a_name]['success']  = 0
                    api_class._adaptors [a_name]['priority'] = a_priority


        # create a log message container for logging failed adaptors
        e_stack = "";

        # for all known adaptors, try to find one which can run the
        # requested method successfully.  We try the adaptors in inverse sorted
        # order, the order key being the number of successful method calls on
        # this api instance.
        #
        # Note that we, however, sort the tuples *twice* -- for the initial
        # attempt (where the success count is '0' for all adaptors, we use the
        # 'priority' attribute, and thus sort for that one first (non-reversed).

        ordered_adaptor_tuples = sorted (api_class._adaptors.items (), 
                                         key     = lambda x:x[1]['priority'])
        ordered_adaptor_tuples = sorted (ordered_adaptor_tuples,
                                         key     = lambda x:x[1]['success'], 
                                         reverse = True)


        print ordered_adaptor_tuples
        for a_tuple in ordered_adaptor_tuples :

            a_name = a_tuple[0]

            # each adaptor's method invocation is tried/catched, so that the
            # next adaptor can be used on failure
            try :
                adaptor    = self.adaptors[a_name]['adaptor']
                module     = self.adaptors[a_name]['module']
                a_registry = self.adaptors[a_name]['registry']

                if class_name in a_registry :
                    pass

                a_cname    = a_registry[class_name]      # name of adaptor class
                                                         # implementing the requested 
                                                         # api class
                a_class    = api_class._adaptors[a_name]['a_class'] # old adaptor class | None

              # from pudb import set_trace; set_trace()


                # this module/adaptor combo can in principle work.  Now we have
                # to check if the api class used that adaptor before - and if
                # so, we reuse the adaptor's class instance.  If not, we have to
                # create a new one before actually calling the method
                if not a_class :

                    # adaptor has not been used for this api class - create new
                    # adaptor class, init it, and keep it in the api class' list
                    api_class._adaptors[a_name]['a_class'] = getattr (module, a_cname) (api_class, adaptor)

                # adaptor class now exists, and can be used.  We try to invoke
                # the method, and to get something we can return.
                ret = getattr (api_class._adaptors[a_name]['a_class'], method_name) (*args, **kwargs)

                # so, this call was successful -- we move the adaptor to the
                # first place in the adaptor list, so that it is the first one
                # tried on the next method call on that api class instance
                api_class._adaptors[a_name]['success'] += 1

                print "engine: call  ok: " + a_name     + "." + a_cname + "." + method_name + \
                                  " (" + str (args) + str (kwargs)  + ") = " + str (ret)
                return ret

            # this adaptor failed to successfully call the method - we log the
            # error and the next adaptor is tried
            except troy.Exception as e :
                print "engine: call nok: " + a_name     + "." + a_cname + "."    + method_name + \
                                  " (" + str (args) + str (kwargs)  + ") : " + str (e)
                e_stack += "  " + a_name + " \t: " + str (e) + "\n";
              # print "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
              # traceback.print_exc ()
              # print "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"

            except Exception as e :
                print "Engine: call NOK: " + a_name     + "." + a_cname + "."    + method_name + \
                                  " (" + str (args) + str (kwargs)  + ") : '" + str (e) + "'"
                e_stack += "  " + a_name + " \t: " + str (e) + "\n";
              # print "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
              # traceback.print_exc ()
              # print "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"


        # no adaptor succeeded
        if  e_stack == "" :
            e_stack = "  Bummer, no adaptors loaded.  None at all!"

        print "ooops: %s" % e_stack
        import sys; sys.exit (0)
        raise troy.Exception (troy.Error.NoSuccess, "no valid adaptor found:\n" + e_stack)        


# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

