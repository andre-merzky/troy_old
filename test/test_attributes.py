#!/usr/bin/python

import datetime
import troy

###########################################
class Attributator ( troy.Attributes ) :
    
    def __init__ (self, *args, **kwargs) :
        # setting attribs to non-extensible will cause the cal to init below to
        # complain if attributes are specified.  Default is extensible.
        # self._attributes_extensible (False)

        # pass args to base class init (implies extensible)
        super (Attributator, self).__init__ (*args, **kwargs)

        # setup class attribs
        self._attributes_register   ('apple', 'Appel', self.Url,    self.Scalar, self.Writable)
        self._attributes_register   ('plum',  'Pruim', self.String, self.Scalar, self.ReadOnly)

        self._attributes_register_deprecated ('Plum',  'plum')

        # setting attribs to non-extensible at *this* point would have allowed
        # custom user attribs on __init__ time (via args), but would then forbid
        # any additional custom attributes 
        # self._attributes_extensible (False)

        # register a getter poll for 'plum', so that we can change values on the fly.  The
        # use case would be to, at this point, ask some backend for value updates.
        #################################
        def poller_all (obj, key) :
            # the poller gets information about what attribute was changed
            # on what object:
            val = obj[key]
            print "POLLED: %s - %s - %s"  %  (key, str(val), type (obj))

            if isinstance (val, basestring) :
                obj.set_attribute (key, val + ' pie')

            # recursion check
            # obj.get_attribute (key)
  
            # returning True will keep the poller registered for further
            return True
        #################################
        def poller (obj, key) :
            # the poller gets information about what attribute was changed
            # on what object:
            val = obj[key]
            print "polled: %s - %s - %s"  %  (key, str(val), type (obj))

            if isinstance (val, basestring) :
                obj.set_attribute (key, val + ' pie')

            # recursion check
            # obj.get_attribute (key)
  
            # returning True will keep the poller registered for further
            return True
        #################################
        self._attributes_set_getter (None,    poller_all)
        self._attributes_set_getter ('apple', poller)


###########################################
if __name__ == "__main__":
    # define a callback method.  This callback can get registered for
    # attribute changes later.

    #################################
    def cb (obj, key, val) :
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
    attr._attributes_set_final ('apple')
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

    # start = datetime.datetime.now ()
    # for i in range (20000) :
    #     t = attr.peach
    # end = datetime.datetime.now ()
    # diff = end - start
    # print str(diff)




# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

