
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

    To register a callback on a object instance, use::

      def MyCallback (troy.pilot.Callback) :

          def cb (self, obj, member, value) :

              print " %s (%s) : %s" %  obj, member, value


      def main () :
        
          cpd = troy.pilot.compute_pilot_description ()
          cps = troy.pilot.compute_pilot_service ()
          cp  = cps.create_pilot (cpd)

          mcb = MyCallback ()

          cp.register_callback ('state', mcb)

    """

    def cb (self, wu, member, value) :
        """ This is the method that needs to be implemented by the application
        
            Keyword arguments:
            obj:    the watched object instance
            member: the watched attribute ('state' or 'state_detail')
            value:  the new value of the watched attribute

            Return:
            Keep   -- bool, Keep (true) or remove (false) the callback
        """
        pass


# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

