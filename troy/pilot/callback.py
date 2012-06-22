
########################################################################
# 
# Callback (Abstract) Class
#
class Callback ():
    """ 
    Callback base class.

    All stateful objects of the pilot API allow to register a callback for
    'state' (and 'state_detail') attribute changes.  That callback is a class
    instance which inherits this callback base class, and implements (overloads)
    the cb() method.  The cb() method is then invoked whenever the TROY
    implementation is notified of a state change of the monitored object.

    The cb instance receives three parameters upon invokation:

      - obj:    the watched object instance
      - member: the watched attribute ('state' or 'state_detail')
      - value:  the new value of the watched attribute

    If cb() returns True, the callback will remain registered after invocation,
    to monitor the object for the next subsequent state change.  On False, the
    callback will not be called again.

    Only one callback can be registered for any given object instance at any
    given time.  If 'set_callback()' is called twice, the earlier callback is
    unregistered.

    To register a callback on a object instance, use::

        class MyCallback (troy.pilot.Callback) :
           
            def __init__ (self, msg) :
                self.msg_ = msg

            def cb (self, obj, member, value) :

                print " %s\n %s (%s) : %s"  %  self.msg_, obj, member, value


        def main () :
          
            cpd = troy.pilot.compute_pilot_description ()
            cps = troy.pilot.compute_pilot_service ()
            cp  = cps.create_pilot (cpd)

            mcb = MyCallback ("Hello Pilot, how is your state?")

            cp.set_callback ('state', mcb)

    """

    def __init__ (self) :
        """ The callback constructor simply raises an IncorrectState exception,
            to signal that the application needs to inherit the callback class
            in a custom class in order to use notifications.
        """
        raise TroyException (Error.IncorrectState, 
                             "Callback class must be inherited before use!")


    def cb (self, wu, member, value) :
        """ This is the method that needs to be implemented by the application
        
            Keyword arguments:
            obj:    the watched object instance
            member: the watched attribute ('state' or 'state_detail')
            value:  the new value of the watched attribute

            Return:
            Keep   -- bool, Keep or remove the callback

            Callback invocation may (and in general will) happen in a separate
            thread -- so the application need to make sure that the callback
            code is thread-safe.

            The boolean return value is used to signal Troy if the callback
            should continue to listen for events (return True) , or if it rather
            should get unregistered after this invocation (return False).
        """
        pass


# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

