
########################################################################
# 
# Callback (Abstract) Class
#
class Callback ():
    """ Callback class.

        Specifies the structure for callback classes.

        Callbacks can be set for WorkUnits on the state or state_detail members.
    """

    def cb (self, wu, member, value):
        """ This is the method that needs to be implemented by the application
        
            Keyword arguments:
            wu     -- The WU that is calling back.
            member -- The member that triggered the callback.
            value  -- The new (detailed) state.

            Return:
            Keep   -- bool, Keep (true) or remove (false) the callback
        """
        pass


