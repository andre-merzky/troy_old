
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

        if not self.name :
            raise troy.Exception (Error.NoSuccess, "adaptor disabled as it does not" \
                                                   "define a name!")
        return self.name


    ############################################################################
    #
    def get_registry (self) :

        if not self.registry :
            raise troy.Exception (Error.NoSuccess, "adaptor disabled as it does not" \
                                                   "expose a registry!")
        return self.registry


    ############################################################################
    #
    def get_priority (self) :

        if not self.priority :
            self.priority = 0  # low adaptor priority by default

        return 0  


    ############################################################################
    #
    def sanity_check (self) :
        raise troy.Exception (Error.NoSuccess, "adaptor disabled as it does not" \
                                               "implement sanity check!")


# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

