
from troy.interface.base  import iBase
from troy.exception       import Exception, Error


########################################################################
# 
#
#
class iDataPilot (iBase) :
    """ L{DataPilot} interface """


    ############################################################################
    #
    def __init__ (self, obj, adaptor) :
        """ Create a DataPilot """
        raise troy.Exception (Error.NotImplemented, "interface not implemented!")


    ############################################################################
    #
    def init_ (self) :
        """ dummy method to make sure the backend can initialize the object.
            This method should *not* be implemented in the adaptor!"""
        pass


    ############################################################################
    #
    def reinitialize (self, dpd) :
        """ Re-Initialize the DataPilot to the (new) DataPilotDescription. """
        raise troy.Exception (Error.NotImplemented, "method not implemented!")


    ############################################################################
    #
    def submit_unit (self, dud) :
        """ Submit a DU to this DataPilot """
        raise troy.Exception (Error.NotImplemented, "method not implemented!")


    ############################################################################
    #
    def list_units (self) :
        """ list managed L{DataUnit}s """
        raise troy.Exception (Error.NotImplemented, "method not implemented!")


    ############################################################################
    #
    def wait (self) :
        """ Wait until DP enters a final state """
        raise troy.Exception (Error.NotImplemented, "method not implemented!")


    ############################################################################
    #
    def cancel (self) :
        """ Cancel DP """
        raise troy.Exception (Error.NotImplemented, "method not implemented!")


# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

