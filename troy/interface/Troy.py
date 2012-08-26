

from troy.interface.base  import iBase
from troy.exception       import Exception, Error
    

########################################################################
#
# 
#
class iTroy (iBase) :
    """  L{Scheduler} interface """


    ############################################################################
    #
    def __init__ (self, obj, adaptor) :
        """ Create a Troy instance """
        raise troy.Exception (Error.NotImplemented, "interface not implemented!")


    ############################################################################
    #
    def init_ (self) :
        """ dummy method to make sure the backend can initialize the object.
            This method should *not* be implemented in the adaptor!"""
        pass


    ############################################################################
    #
    def add_scheduler (self, s) :
        """ Set a scheduler for submitted work units """
        raise troy.Exception (Error.NotImplemented, "method not implemented!")


    ############################################################################
    #
    def list_schedulers (self) :
        """ return array of registered scheduler instances """
        raise troy.Exception (Error.NotImplemented, "method not implemented!")


    ############################################################################
    #
    def remove_scheduler (self, s) :
        """ remove a previously registered scheduler instance """
        raise troy.Exception (Error.NotImplemented, "method not implemented!")


    ############################################################################
    #
    def add_pilot_framework (self, cpf) :
        """ Add a PilotFramework to this Scheduler """
        raise troy.Exception (Error.NotImplemented, "method not implemented!")


    ############################################################################
    #
    def list_pilot_frameworks (self) :
        """ List all CPFs of Scheduler """
        raise troy.Exception (Error.NotImplemented, "method not implemented!")


    ############################################################################
    #
    def remove_pilot_framework (self, cpf) :
        """ Remove a PilotFramework """
        raise troy.Exception (Error.NotImplemented, "method not implemented!")


    ############################################################################
    #
    def submit_unit (self, cud) :
        """ Submit a CU to this Scheduler """
        raise troy.Exception (Error.NotImplemented, "method not implemented!")


    ############################################################################
    #
    def list_units (self) :
        """ list managed work Unit """
        raise troy.Exception (Error.NotImplemented, "method not implemented!")


# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

