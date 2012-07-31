
import troy.pilot as pilot

################################################################################
#
#
#
class Transliterator ( pilot.Attributes ) :
    
    def __init__ (self) :
        self.attribute_register_   ('apple', 'Appel', self.String, self.Scalar, self.Writeable)
        self.attribute_register_   ('plum',  'Pruim', self.String, self.Scalar, self.ReadOnly)
        self.attribute_extensible_ (True)


################################################################################
#
#
#
if __name__ == "__main__":

    def cb (key, val, obj) :
        print "called: %s - %s - %s"  %  (key, val, type (obj))

    trans = Transliterator ()

    print " -- apple"
    print trans.apple 
    trans.apple = 'Apfel'
    print trans.apple 

    trans.attribute_register_cb ('apple', cb)
    trans.apple = ['Boskop', 'Jonas']
    trans.apple = 'Apfel'

    trans.attribute_set_final_ ('apple')
    trans.apple = 'Abbel'
    print trans.apple 


    print "\n -- plum"
    print trans.plum 
  # trans.plum = 'Pflaume'  # raises exception
    print trans.plum

    print "\n -- peach"
  # print trans.peach       # raises exception
    trans.peach = 'Birne'
    print trans.peach

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

