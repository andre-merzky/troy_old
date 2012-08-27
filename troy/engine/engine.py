
import os
import glob
import imp
import traceback

import troy.exception 

def singleton (type) :

    instances = {}
    
    def getinstance () :
        
        if type not in instances :
            instances[type] = type ()
        
        return instances[type]
    
    return getinstance


@singleton
class Engine (object) :

    ##########################################################################
    # 
    # load all adaptors
    #
    def __init__ (self) :

        print " === init engine"
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

                a_order    = adaptor.get_order    ()
                a_name     = adaptor.get_name     ()
                a_registry = adaptor.get_registry ()

                self.adaptors[a_name] = {'module'   : module, 
                                         'adaptor'  : adaptor,
                                         'order'    : a_order,
                                         'registry' : a_registry}

            except Exception, e :
                # this adaptor failed to load, or failed the sanity check - log
                # error and continute.
                print "engine: init: load adaptor: " + path + " failed:\n  " + str (e)
                pass
            

    ##########################################################################
    # 
    # invoke an adaptor method
    #
    def call (self, class_name, method_name, api_class, *args, **kwargs) :
        '''call an adaptor function, for the given class/method, and give as
           args the object state (extracted from api_class), and the method args
        '''

        # if the api_class is used the first time, sift through loaded adaptors (sorted list)
        if 0 == len (api_class.adaptors_) :

            for a_name in self.adaptors.keys () :

                a_registry = self.adaptors[a_name]['registry']
                a_order    = self.adaptors[a_name]['order']

                # did that adaptor register to handle the class?
                if class_name in a_registry :

                    # if so, add that one to the list of adaptors for that
                    # class.  Initially, the adaptor does not create a adaptor
                    # class instance, so we set that to 'None' -- that is only
                    # created as needed, see below
                    api_class.adaptors_ [a_name] = {}
                    api_class.adaptors_ [a_name]['a_class'] = None
                    api_class.adaptors_ [a_name]['success'] = 0
                    api_class.adaptors_ [a_name]['order']   = a_order


        # create a log message container for logging failed adaptors
        e_stack = "";

        # for all known adaptors, try to find one which can run the
        # requested method successfully.  We try the adaptors in inverse sorted
        # order, the order key being the number of successful method calls on
        # this api instance.
        #
        # Note that we, however, sort the tuples *twice* -- for the initial
        # attempt (where the success count is '0' for all adaptors, we use the
        # 'order' attribute, and thus sort for that one first (non-reversed).

        ordered_adaptor_tuples = sorted (api_class.adaptors_.items (), 
                                         key     = lambda x:x[1]['order'])
        ordered_adaptor_tuples = sorted (ordered_adaptor_tuples,
                                         key     = lambda x:x[1]['success'], 
                                         reverse = True)


        for a_tuple in ordered_adaptor_tuples :

            a_name = a_tuple[0]

            # each adaptor's method invocation is tried/catched, so that the
            # next adaptor can be used on failure
            try :
                adaptor    = self.adaptors[a_name]['adaptor']
                module     = self.adaptors[a_name]['module']
                a_registry = self.adaptors[a_name]['registry']
                a_cname    = a_registry[class_name]      # name of adaptor class
                                                         # implementing the requested 
                                                         # api class
                a_class    = api_class.adaptors_[a_name]['a_class'] # old adaptor class | None

                # this module/adaptor combo can in principle work.  Now we have
                # to check if the api class used that adaptor before - and if
                # so, we reuse the adaptor's class instance.  If not, we have to
                # create a new one before actually calling the method
                if not a_class :

                    # adaptor has not been used for this api class - create new
                    # adaptor class, init it, and keep it in the api class' list
                    api_class.adaptors_[a_name]['a_class'] = getattr (module, a_cname) (api_class, adaptor)

                # adaptor class now exists, and can be used.  We try to invoke
                # the method, and to get something we can return.
                ret = getattr (api_class.adaptors_[a_name]['a_class'], method_name) (*args, **kwargs)

                # so, this call was successful -- we move the adaptor to the
                # first place in the adaptor list, so that it is the first one
                # tried on the next method call on that api class instance
                api_class.adaptors_[a_name]['success'] += 1

                print "engine: call: " + a_name     + "." + a_cname + "." + method_name + \
                                  " (" + str (args) + str (kwargs)  + ") = " + str (ret)
                return ret

            # this adaptor failed to successfully call the method - we log the
            # error and the next adaptor is tried
            except troy.Exception as e :
                print "engine: call: " + a_name     + "." + a_cname + "."    + method_name + \
                                  " (" + str (args) + str (kwargs)  + ") : " + str (e)
                e_stack += "  " + a_name + " \t: " + str (e) + "\n";
                print "  --- ~~~ --->"
                traceback.print_exc ()
                print " <--- ~~~ ---"


        # no adaptor succeeded
        if e_stack == "" :
            e_stack = "  Bummer, no adaptors loaded.  None at all!"

        raise troy.Exception (troy.Error.NoSuccess, "no valid adaptor found:\n" + e_stack)        


# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

