
from troy.pilot.exception        import TroyException, Error


########################################################################
#
# the base of all interface classes.  Not yet used, really
#
class iBase:

    def __init__ (self) :
        pass


########################################################################
#
# the base of all adaptor classes.
#
class aBase:

    def __init__ (self) :
        pass

    def sanity_check (self) :
        raise TroyException (Error.NoSuccess, "adaptor disabled as it does not" \
                                          "implement sanity check!")

