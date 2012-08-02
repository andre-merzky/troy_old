
from troy.interface.base  import iBase
from troy.pilot.exception import TroyException, Error


########################################################################
#
# iDataUnit (DU)
# 
class iDataUnit (iBase) :
    """ L{DataUnit} interface """

    ############################################################################
    #
    def __init__ (self, obj, adaptor) :
        raise TroyException (Error.NotImplemented, "method not implemented!")
        pass



    ############################################################################
    #
    def init_ (self) :
        """ dummy method to make sure the backend can initialize the object.
            This method should *not* be implemented in the adaptor!"""
        pass



    ############################################################################
    #
    def wait (self):
        """ Wait until DU enters a final state """
        raise TroyException (Error.NotImplemented, "method not implemented!")



    ############################################################################
    #
    def cancel (self):
        """ Cancel the DU """
        raise TroyException (Error.NotImplemented, "method not implemented!")


# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
