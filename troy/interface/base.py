
from troy.pilot.exception        import TroyException, Error


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
        print "iBase: dummy init method called"
        pass



########################################################################
#
# the base of all adaptor classes.
#
# FIXME: move to adaptors
#
class aBase:

    ############################################################################
    #
    def __init__ (self) :
        pass



    ############################################################################
    #
    def get_name (self) :
        raise TroyException (Error.NoSuccess, "adaptor disabled as it does not" \
                                              "implement get_name!")


    ############################################################################
    #
    def get_registry (self) :
        raise TroyException (Error.NoSuccess, "adaptor disabled as it does not" \
                                              "implement get_registry!")
        return self.registry



    ############################################################################
    #
    def get_order (self) :
        return 1000  # low adaptor priority by default



    ############################################################################
    #
    def sanity_check (self) :
        raise TroyException (Error.NoSuccess, "adaptor disabled as it does not" \
                                              "implement sanity check!")
        pass


# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

