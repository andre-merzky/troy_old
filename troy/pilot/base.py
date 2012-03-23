
from ..    import engine
from state import State

########################################################################
#
#
#
class Base:

    def __init__ (self) :
        print "base: init"
        self.engine_   = engine.Engine ()  # engine singleton to handle adaptors
        self.adaptors_ = {}                # sorted list of used adaptors
        self.idata_    = {}                # adaptor specific instance data

    def get_engine_ (self) :
        return self.engine_
        
    def get_adaptors_ (self) :
        return self.adaptors_
        
    def get_idata_ (self, id) :
        return self.idata_[id]

    def set_idata_ (self, id, data) :
        self.idata_[id] = data


