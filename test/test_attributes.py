
import troy.pilot as pilot

################################################################################
#
#
#
class Transliterator ( pilot.Attributes ) :
    
    def __init__ (self, *args, **kwargs) :
      # setting attribs to non-extensible will cause the cal to init below to
      # complain if attributes are specified.  Default is extensible.
      # self.attributes_extensible_ (False)

        # pass args to base class init (implies extensible)
        super (Transliterator, self).__init__ (*args, **kwargs)

        # setup class attribs
        self.attributes_register_   ('apple', 'Appel', self.Url,    self.Scalar, self.Writeable)
        self.attributes_register_   ('plum',  'Pruim', self.String, self.Scalar, self.ReadOnly)

      # setting attribs to non-extensible at *this* point will have allowed
      # custom user attribs on __init__ time (via args), but will then forbid
      # any additional custom attributes
      # self.attributes_extensible_ (False)


################################################################################
#
#
#
if __name__ == "__main__":

    def cb (key, val, obj) :
        print "called: %s - %s - %s"  %  (key, val, type (obj))
        return True

    trans = Transliterator (cherry='Kersche')

    # trans.attributes_dump_ ()

    print " -- apple"
    print trans.apple 
    print trans['apple']
    trans.apple = 'Abbel'
    print trans.apple 

    trans.add_callback ('apple', cb)
    trans.apple = ['Abbel', 'Appel']

    trans.attributes_set_final_ ('apple', 'Appel')
    trans.apple = 'Abbel'  # this will be ignored, attrib is 'final'
    print trans.apple 


    print "\n -- plum"
    print trans.plum 
  # trans.plum = 'Pflaume'  # raises exception
    print trans.plum

    print "\n -- cherry"
    print trans.cherry

    print "\n -- peach"
    trans['peach'] = 'Berne'
    print trans.peach
    trans.peach = 'Birne'
    print trans.peach

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

