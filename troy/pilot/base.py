
from ..    import engine
from state import State

########################################################################
#
#
#
class Base:

    """ 
    All Troy API classes inherit  from this base class, which provides
    interfaces to adaptor management and to the management of class instance
    data.

    In particular, this base class provides the following class members to all
    API classes:

      - engine_   : a reference to the engine singleton, which manages adaptors 
                    and call forwarding
      - adaptors_ : a sorted list of used adaptors, which *can* be used by the
                    engine to optimize adaptor invocation (previously successful
                    adaptors are most likely to succeed again)
      - idata_    : a dict of dicts, for class instance state data management.  
                    The dict under idata_['api'] holds the actual class instance
                    data (documented for each class), all other keys hold adaptor
                    level instance data, for example to cache connections.  The
                    keys for those adaptor instance data SHOULD be the adaptor
                    name.  idata_ SHOULD not be accessed directly, but via
                    get_idata() and set_idata(),

    The accessor methods are marked as private, as they are not part of the API.
    They are intended to be used by the engine and the adaptors.
    """
    

    def __init__ (self) :
        print "base: init"
        self.engine_   = engine.Engine ()  # engine singleton to handle adaptors
        self.adaptors_ = {}                # sorted list of used adaptors
        self.idata_    = {}                # adaptor specific instance data

    def get_engine_ (self) :
        """ 
        Get the engine singleton.  

        That method is only used by the API instance itself, to invoke the
        engine's call() forwarding mechanism.
        """
        return self.engine_

        
    def get_adaptors_ (self) :
        """ 
        Get list of all previously successful adaptors.

        That list is maintained by the engine (only).
        """
        return self.adaptors_

        
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


# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

