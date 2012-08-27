
from troy.interface.base  import iBase
from troy.exception       import Exception, Error
    

########################################################################
#
#  
#
class iPilotFramework (iBase) :
    """ L{PilotFramework} interface """


    ############################################################################
    #
    def __init__ (self, obj, adaptor) :
        """ Create a PilotFramework """
        raise troy.Exception (Error.NotImplemented, "interface not implemented!")


    ############################################################################
    #
    def init_ (self) :
        """ dummy method to make sure the backend can initialize the object.
            This method should *not* be implemented in the adaptor!"""
        pass


    ############################################################################
    #
    def submit_pilot (self, pd) :
        """ Create a Pilot. """
        raise troy.Exception (Error.NotImplemented, "method not implemented!")


    ############################################################################
    #
    def list_pilots (self) :
        """ list managed Pilot. """
        raise troy.Exception (Error.NotImplemented, "method not implemented!")


    ############################################################################
    #
    def submit_unit (self, ud) :
        """ Submit a work unit to this PilotFramework """
        raise troy.Exception (Error.NotImplemented, "method not implemented!")


    ############################################################################
    #
    def list_units (self) :
        """ list managed work unit """
        raise troy.Exception (Error.NotImplemented, "method not implemented!")


    ############################################################################
    #
    def cancel (self) :
        """ cancel pilot framework, and all its pilots """
        raise troy.Exception (Error.NotImplemented, "method not implemented!")


# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

