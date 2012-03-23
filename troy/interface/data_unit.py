
from troy.interface.base  import iBase
from troy.pilot.exception import Exception, Error


########################################################################
#
# iDataUnit (DU)
# 
class iDataUnit (iBase) :

    """ DataUnit. 

        This is the object that is returned by the DataUnitService when a 
        new DataUnit is created based on a DataUnitDescription.

        The DataUnit object can be used by the application to keep track 
        of DataUnits that are active.

        A DataUnit has state, can be queried and can be cancelled.
    """

    def __init__ (self):
        pass


    def wait (self, obj):
        """ Wait until DU enters a final state """
        raise Exception (Error.NotImplemented, "method not implemented!")


    def cancel (self, obj):
        """ Cancel the DU """
        raise Exception (Error.NotImplemented, "method not implemented!")


    def set_callback (self, obj, member, cb):
        """ Set a callback function for a member.

            Keyword arguments:
            member -- The member to set the callback for (state / state_detail).
            cb     -- The callback object to call.
        """
        raise Exception (Error.NotImplemented, "method not implemented!")

    
    def unset_callback (self, obj, member):
        """ Unset a callback function from a member

            Keyword arguments:
            member -- The member to unset the callback from.
        """
        raise Exception (Error.NotImplemented, "method not implemented!")


    def list_files (self, obj):
        """ list files managed by the DU """
        raise Exception (Error.NotImplemented, "method not implemented!")
    

    def data_export (self, obj, target_directory):
        """ copies content of DU to a directory on the local machine"""
        raise Exception (Error.NotImplemented, "method not implemented!")

        
    def data_import (self, obj, src_directory):
        """ copies content from a directory on the local machine to DU"""
        raise Exception (Error.NotImplemented, "method not implemented!")
        
