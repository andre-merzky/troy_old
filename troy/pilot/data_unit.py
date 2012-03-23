
from base import Base


########################################################################
#
# DataUnit (DU)
# 
class DataUnit (Base) :

    """ DataUnit. 

        This is the object that is returned by the DataUnitService when a 
        new DataUnit is created based on a DataUnitDescription.

        The DataUnit object can be used by the application to keep track 
        of DataUnits that are active.

        A DataUnit has state, can be queried and can be cancelled.
    """

    # Class members
    __slots__ = (
        'id',           # Reference 
        'state',        # State
        'state_detail', # Backend specific state of the DataUnit

        'description',  # Description
    )


    def wait (self):
        """ Wait until DU enters a final state """
        pass


    def cancel (self):
        """ Cancel the DU """
        pass


    def set_callback (self, member, cb):
        """ Set a callback function for a member.

            Keyword arguments:
            member -- The member to set the callback for (state / state_detail).
            cb     -- The callback object to call.
        """
        pass

    
    def unset_callback (self, member):
        """ Unset a callback function from a member

            Keyword arguments:
            member -- The member to unset the callback from.
        """
        pass


    def list_files (self):
        """ list files managed by the DU """
        pass
    

    def data_export (self, target_directory):
        """ copies content of DU to a directory on the local machine"""
        pass    

        
    def data_import (self, src_directory):
        """ copies content from a directory on the local machine to DU"""
        pass    
        
