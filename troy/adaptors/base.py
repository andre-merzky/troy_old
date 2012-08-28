
from troy.exception import Exception, Error


########################################################################
#
# the base of all adaptor classes.
#
class aBase:

    ############################################################################
    #
    def __init__ (self) :
        pass



    ############################################################################
    #
    def get_name (self) :
        raise troy.Exception (Error.NoSuccess, "adaptor disabled as it does not" \
                                               "implement get_name!")


    ############################################################################
    #
    def get_registry (self) :
        raise troy.Exception (Error.NoSuccess, "adaptor disabled as it does not" \
                                               "implement get_registry!")
        return self.registry


    ############################################################################
    #
    def get_order (self) :
        return 1000  # low adaptor priority by default


    ############################################################################
    #
    def sanity_check (self) :
        raise troy.Exception (Error.NoSuccess, "adaptor disabled as it does not" \
                                               "implement sanity check!")
        pass



# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

