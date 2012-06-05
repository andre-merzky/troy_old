
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

    def __init__ (self) :
        Base.__init__ (self)
        pass 


    def wait (self) :
        """ Wait until DU enters a final state """
        return self.engine_.call ('DataUnit', 'wait', self)


    def cancel (self) :
        """ Cancel the DU """
        return self.engine_.call ('DataUnit', 'cancel', self)


    def set_callback (self, member, cb) :
        """ Set a callback function for a member.

            Keyword arguments:
            member -- The member to set the callback for (state / state_detail).
            cb     -- The callback object to call.
        """
        return self.engine_.call ('DataUnit', 'set_callback', 
                                        self, member, cb)

    
    def unset_callback (self, member) :
        """ Unset a callback function from a member

            Keyword arguments:
            member -- The member to unset the callback from.
        """
        return self.engine_.call ('DataUnit', 'unset_callback', 
                                        self, member)


    def list_files (self) :
        """ list files managed by the DU """
        return self.engine_.call ('DataUnit', 'list_files', 
                                        self)
    

    def data_export (self, tgt) :
        """ copies content of DU to a directory on the local machine"""
        return self.engine_.call ('DataUnit', 'data_export', 
                                        self, tgt)

        
    def data_import (self, src_directory) :
        """ copies content from a directory on the local machine to DU"""
        return self.engine_.call ('DataUnit', 'data_import', 
                                        self, src)
        
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

