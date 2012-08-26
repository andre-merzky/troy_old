
from troy.interface.base  import iBase
from troy.exception       import Exception, Error


########################################################################
#
# iDataUnit (DU)
# 
class iDataUnit (iBase) :
    """ L{DataUnit} interface """


    ############################################################################
    #
    def __init__ (self, obj, adaptor) :
        raise troy.Exception (Error.NotImplemented, "method not implemented!")


    ############################################################################
    #
    def init_ (self) :
        """ dummy method to make sure the backend can initialize the object.
            This method should *not* be implemented in the adaptor!"""
        pass


    ############################################################################
    #
    def wait (self) :
        """ Wait until DU enters a final state """
        raise troy.Exception (Error.NotImplemented, "method not implemented!")


    ############################################################################
    #
    def cancel (self) :
        """ Cancel the DU """
        raise troy.Exception (Error.NotImplemented, "method not implemented!")


# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

