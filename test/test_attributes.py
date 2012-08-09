
import troy.pilot as pilot

###########################################
class Transliterator ( pilot.Attributes ) :
    
    def __init__ (self, *args, **kwargs) :
      # setting attribs to non-extensible will cause the cal to init below to
      # complain if attributes are specified.  Default is extensible.
      # self.attributes_extensible_ (False)

        # pass args to base class init (implies extensible)
        super (Transliterator, self).__init__ (*args, **kwargs)

        # setup class attribs
        self.attributes_register_   ('apple', 'Appel', self.Url,    self.Scalar, self.Writable)
        self.attributes_register_   ('plum',  'Pruim', self.String, self.Scalar, self.ReadOnly)

      # setting attribs to non-extensible at *this* point will have allowed
      # custom user attribs on __init__ time (via args), but will then forbid
      # any additional custom attributes
      # self.attributes_extensible_ (False)


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
    trans = Transliterator (cherry='Kersche')

    # use the property and the dict interface to mess with the pre-defined
    # 'apple' attribute
    print "\n -- apple"
    print trans.apple 
    print trans['apple']
    trans.apple = 'Abbel'
    print trans.apple 

    # add our callback to the apple attribute, and trigger some changes.
    # Note that the callback is also triggered when the attribute's
    # value changes w/o user control, e.g. by some internal state
    # changes.
    trans.add_callback ('apple', cb)
    trans.apple = ['Abbel', 'Appel']
    trans.apple = 'Apfel'

    # Setting an attribute final is actually an internal method, used by
    # the implementation to signal that no further changes on that
    # attribute are expected.  We use that here for demonstrating the
    # concept though.  Callback is invoked on set_final_.
    trans.attributes_set_final_ ('apple')
    trans.apple = 'Abbel'
    print trans.apple 

    # mess around with the 'plum' attribute, which was marked as
    # ReadOnly on registration time.
    print "\n -- plum"
    print trans.plum
  # trans.plum    = 'Pflaume'  # raises readonly exception
  # trans['plum'] = 'Pflaume'  # raises readonly exception
    print trans.plum

    # check if the 'cherry' attribute exists, which got created on
    # instantiation time.
    print "\n -- cherry"
    print trans.cherry

    # as we have 'extensible' set, we can add a attribute on the fly,
    # via either the property or the dict interface, or via the GFD.90
    # API of course.
    print "\n -- peach"
    trans['peach'] = 'Berne'
    print trans.peach
    trans.peach = 'Birne'
    print trans.peach

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

