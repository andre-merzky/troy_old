
from troy  import engine
from state import State

########################################################################
#
#
#
class Base (object):

    """ 

    All Troy API classes inherit  from this base class, which provides support
    for adaptor management and the management of class instance data.  

    In particular, this base class provides the following class members to all
    API classes:

      - engine_   : a reference to the engine singleton, which manages adaptors 
                    and call forwarding
      - adaptors_ : a sorted list of used adaptors, which can be used by the
                    engine to optimize adaptor invocation (previously successful
                    adaptors are most likely to succeed again)
      - idata_    : a dict of dicts, for class instance state data management.  
                    The dict under idata_['api'] holds the actual class instance
                    data (documented for each class), all other keys hold adaptor
                    level instance data, for example to cache connections.  The
                    keys for those adaptor instance data SHOULD be the adaptor
                    name.
      - contexts  : a list of context dicts which are specified by the
                    application, and used by the adaptors, as pointer to
                    security tokens to be used for backend operations.

    The first three members marked as private, as they are not part of the API
    -- they are intended to be used by the API implementation only.  The context
    list is public, and applications are explicitly able and encouraged to
    access it.

    """
    

    def __init__ (self) :
        self.engine_   = engine.Engine ()  # engine singleton to handle adaptors
        self.adaptors_ = {}                # sorted list of used adaptors
        self.idata_    = {}                # adaptor specific instance data
        self.contexts  = []                # list of security context dicts

        
    def get_idata_ (self, id = 'api') :
        """ 
        Get instance data dict entry.
        
        By default, this returns the class instance data, otherwise the instance
        data of the specified adaptor.
        """
        return self.idata_[id]


    def set_idata_ (self, data, id='api') :
        """ 
        Set instance data dict entry.
        
        By default, this sets the class instance data, otherwise the instance
        data of the specified adaptor.
        """
        self.idata_[id] = data


    def dump_ (self) :
        """
        Dump dumps.  Doh!

        But really, what did you expect a dump() method would do? ;-)
        """
        print "dumping " + str(self)
        for key in self.idata_ :
            print "  " + key + "\t : " + str (self.idata_[key])



# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

