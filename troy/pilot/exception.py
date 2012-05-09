
import traceback
import StringIO

class Error:

    """
    TROY's exception class instances have two attributes: an error code, and an
    error message.  This 'Error' enum is the error code.  This list will be
    expanded once the API's semantics is smoothening out.
    """

    NoSuccess      = 'NoSuccess'         """ operation failed on backend.  """
    NotImplemented = 'NotImplemented'    """ operation is not implemented. """



class TroyException (Exception):

    """
    The TROY exception class is (obviously) used to signal error conditions to
    the user of TROY's pilot API.

    In principle, the name 'Exception' would suffice, but that can, on
    occasions, collide  with the native python Exception type (on careless
    'import as' directives (as I learned the hard way...).  That is why the
    class is named TroyException for now -- that may change in the future.
    """
    

    def __init__ (self, error, msg) :

        tmp = StringIO.StringIO ()
        traceback.print_stack (file = tmp)

        self.trace = tmp.getvalue ()
        self.error = error
        self.msg   = msg


    def __str__ (self) :
        return str (self.error) + ": " + self.msg


    def get_trace (self) :
        return self.trace

 
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

