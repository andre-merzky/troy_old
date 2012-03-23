
import traceback
import StringIO

class Error:

    NoSuccess      = 'NoSuccess'
    NotImplemented = 'NotImplemented'


class Exception (Exception):
    

    def __init__ (self, error, msg) :

        tmp = StringIO.StringIO ()
        traceback.print_stack (file = tmp)

        self.trace = tmp.getvalue ()
        self.error = error
        self.msg   = msg


    def __str__ (self) :
        return str (self.error) + ": " + self.msg
 
