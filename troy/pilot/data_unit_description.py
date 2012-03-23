

########################################################################
#
# DataUnitDescription
# 
class DataUnitDescription (dict) :

    """ DataUnitDescription.

        'file_urls': [file1, file2, file3]        
        
        Currently, no directories supported
    """

    # Class members
    __slots__ = (
        # FIXME: what goes here?
        )


    def __init__ (self):
        pass


    def __setattr__ (self, attr, value):
        self[attr]=value
    

    def __getattr__ (self, attr):
        return self[attr]
    
