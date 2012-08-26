
import traceback
import StringIO

class Error:

    """
    TROY's exception class instances have two attributes: an error code, and an
    error message.  This 'Error' enum is the error code.  This list will be
    expanded once the API's semantics is smoothening out.
    """

    NoSuccess      = 'NoSuccess'      # """ operation failed on backend. """
    BadParameter   = 'BadParameter'   # """ operation cannot handle parameter type or value. """
    IncorrectState = 'IncorrectState' # """ operation not allowed in current object state. """
    NotImplemented = 'NotImplemented' # """ operation is not implemented. """
    DoesNotExist   = 'DoesNotExist'   # """ operation target is missing. """
    AlreadyExists  = 'DoesNotExist'   # """ operation target is already present. """



class Exception (Exception) :

    """
    The TROY exception class is (obviously) used to signal error conditions to
    the user of TROY's API.
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

