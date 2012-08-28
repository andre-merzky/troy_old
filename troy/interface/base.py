
import troy.exception


########################################################################
#
# the base of all interface classes.  Not yet used, really
#
class iBase:


    ############################################################################
    #
    def __init__ (self) :
        # each API class instance manages its own instance data, which is used
        # by the adaptors to keep class state consistent between function calls,
        # and across different adaptors (late binding)
        pass


    ############################################################################
    #
    def init_ (self) :
        """ dummy method to make sure the backend can initialize the object.
            This method should *not* be implemented in the adaptor!"""
        pass


# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

