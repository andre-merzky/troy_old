
from troy            import engine
from troy.state      import State
from troy.attributes import Attributes

########################################################################
#
#
#
class Base (Attributes, object):

    """
    All Troy API classes inherit  from this base class, which provides support
    for adaptor management and the management of class instance data.

    In particular, this base class provides the following class members to all
    API classes:



      - _engine   : a reference to the engine singleton, which manages adaptors
                    and call forwarding


      - _adaptors : a sorted list of used adaptors, which can be used by the
                    engine to optimize adaptor invocation (previously successful
                    adaptors are most likely to succeed again)


      - _idata    : a dict of dicts, for class instance state data management.
                    The dict under _idata['api'] holds the actual class instance
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

        # _engine   : engine singleton to handle adaptors 
        # _adaptors : sorted list of used adaptors        
        # _idata    : adaptor specific instance data      
        # _contexts : list of security context dicts      

        self._attributes_register  ('_engine',   engine.Engine(), self.Any, self.Scalar, self.ReadOnly)
        self._attributes_register  ('_adaptors', {},              self.Any, self.Scalar, self.ReadOnly)
        self._attributes_register  ('_idata',    {},              self.Any, self.Scalar, self.ReadOnly)
        self._attributes_register  ('_contexts', [],              self.Any, self.Scalar, self.ReadOnly)


    def dump_ (self) :
        """
        Dump dumps.  Doh!

        But really, what did you expect a dump() method would do? ;-)
        """
        print "dumping " + str(self)
        for key in self._idata :
            print "  " + key + "\t : " + str (self._idata[key])



# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

