
import troy.pilot as pilot

###########################################
class Attributator ( pilot.Attributes ) :
    
    def __init__ (self, *args, **kwargs) :
        # setting attribs to non-extensible will cause the cal to init below to
        # complain if attributes are specified.  Default is extensible.
        # self.attributes_extensible_ (False)

        # pass args to base class init (implies extensible)
        super (Attributator, self).__init__ (*args, **kwargs)

        # setup class attribs
        self.attributes_register_   ('apple', 'Appel', self.Url,    self.Scalar, self.Writable)
        self.attributes_register_   ('plum',  'Pruim', self.String, self.Scalar, self.ReadOnly)

        self.attributes_register_deprecated_ ('Plum',  'plum')

        # setting attribs to non-extensible at *this* point would have allowed
        # custom user attribs on __init__ time (via args), but would then forbid
        # any additional custom attributes 
        # self.attributes_extensible_ (False)

        # register a getter poll for 'plum', so that we can change values on the fly.  The
        # use case would be to, at this point, ask some backend for value updates.
        #################################
        def poller (key, val, obj) :
            # the poller gets information about what attribute was changed
            # on what object:
            print "polled: %s - %s - %s"  %  (key, str(val), type (obj))

            if isinstance (val, basestring) :
                obj.set_attribute (key, val + ' pie')

            # recursion check
            # obj.get_attribute (key)
  
            # returning True will keep the poller registered for further
            return True
        #################################
        self.attributes_poll_add_ ('apple', poller, self.Get)


###########################################
if __name__ == "__main__":
    # define a callback method.  This callback can get registered for
    # attribute changes later.

    #################################
    def cb (key, val, obj) :
        # the callback gets information about what attribute was changed
        # on what object:
        print "called: %s - %s - %s"  %  (key, str(val), type (obj))

        # returning True will keep the callback registered for further
        return True
    #################################

    # create a class instance and add a 'cherry' attribute/value on
    # creation.  
    attr = Attributator (cherry='Kersche')

    # use the property and the dict interface to mess with the pre-defined
    # 'apple' attribute
    print "\n -- apple"
    print attr.apple 
    print attr['apple']
    attr.apple = 'Abbel'
    print attr.apple 

    # add our callback to the apple attribute, and trigger some changes.
    # Note that the callback is also triggered when the attribute's
    # value changes w/o user control, e.g. by some internal state
    # changes.
    attr.add_callback ('apple', cb)
    attr.apple = ['Abbel', 'Appel']
    attr.apple = 'Apfel'

    # Setting an attribute final is actually an internal method, used by
    # the implementation to signal that no further changes on that
    # attribute are expected.  We use that here for demonstrating the
    # concept though.  Callback is invoked on set_final_.
    attr.attributes_set_final_ ('apple')
    attr.apple = 'Abbel'
    print attr.apple 

    # mess around with the 'plum' attribute, which was marked as
    # ReadOnly on registration time.
    print "\n -- plum"
    print attr.plum
  # attr.plum    = 'Pflaume'  # raises readonly exception
  # attr['plum'] = 'Pflaume'  # raises readonly exception
    print attr.plum

    # lets see what happens if we use the deprecated name
    print attr.Plum

    # check if the 'cherry' attribute exists, which got created on
    # instantiation time.
    print "\n -- cherry"
    print attr.cherry

    # as we have 'extensible' set, we can add a attribute on the fly,
    # via either the property or the dict interface, or via the GFD.90
    # API of course.
    print "\n -- peach"
    attr['peach'] = 'Berne'
    print attr.peach
    attr.peach = 'Birne'
    print attr.peach

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

