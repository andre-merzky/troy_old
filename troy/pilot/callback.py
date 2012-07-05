
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
          print " %s\\n %s (%s) : %s"  %  self.msg_, obj, member, value

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


class monitorable () :
    """ 
    Interface to attach callback to watch class attributes.

    This interface is used throughout Troy's Pilot API to support the monitoring
    of stateful class instances, such as L{ComputePilot}s and L{ComputeUnit}s.
    It provides two methods, to register and unregister callbacks for a specific
    class attribute::

        class MyCallback (troy.pilot.Callback) :
            def cb (self, obj, member, value) :
                print " %s (%s) : %s"  %  obj, member, value

        def main () :
            cb = MyCallback()
            cu = troy.pilot.ComputeUnit (id)
            cu.add_callback ('state', cb)

            cu.wait ()  
            # callback will get triggered when the cu reaches a final state.
    """

    def set_callback (self, member, cb) :
        """ Set a callback function for a member.

            Keyword arguments:
            member -- The member to set the callback for (state / state_detail / wall_time_left).
            cb     -- The callback object to call.

            Setting the callback does not guarantee that all changes of the
            watched member cause a callback invocation.  For example,
            wall_time_left will be a continuously changing member, but the
            callback may be invoked at regular or non-regular intervals.  The
            implementation will, however, invoke the callback on a best-effort
            basis.

            It is not an error to call this method if a callback is already
            registered -- the call will then replace the callback, and behave
            like::

                def set_callback (self, member, cb) :
                  
                  if self.has_callback () :
                      unset_callback  (member)

                  self.set_callback (member, cb)

        """
        return self.engine_.call ('Monitorable', 'set_callback', self, member, cb)

    def unset_callback (self, member) :
        """ Unset a callback function from a member

            Keyword arguments:
            member -- The member to unset the callback for (state / state_detail / wall_tim_left).

            A callback may still be invoked during the unset_call, but it is
            guaranteed that no invocation will happen after the call finishes.

            It is not an error to call this method if no callback is registered
            -- the call will simply return immediately.
        """
        return self.engine_.call ('Monitorable', 'unset_callback', self, member)
    

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

