#!/usr/bin/python

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

import troy
import time
import pdb

def test_compute ():
    # try:
        print " 1 -------------------------------------------- "
        t   = troy.Troy ()
        pf  = troy.PilotFramework ('peejay://')

        print " 2 -------------------------------------------- "
        t.add_pilot_framework (pf)
        
        print " 3 -------------------------------------------- "
        s   = troy.Scheduler ('Random')
        t.add_scheduler (s)

        print " 4 -------------------------------------------- "
        cpd  = troy.ComputePilotDescription ()

        print " 5 -------------------------------------------- "
        cp1  = pf.submit_pilot (cpd)

        print " 6 -------------------------------------------- "
        cp2  = pf.submit_pilot (cpd)
 
        print " 7 -------------------------------------------- "

        for id in t.list_pilot_frameworks () :
            print "pf: " + str(id) + " : " + str (troy.PilotFramework(id).list_pilots())
 
        print " 8 -------------------------------------------- "
        cud  = troy.ComputeUnitDescription ()
 
        cud['executable'] = '/bin/sh'
        cud['arguments']  = ['-c', 'touch /tmp/hello_troy_pj && sleep 10']
 
        print " 9 -------------------------------------------- "
        cu  = t.submit_unit (cud)

        print " 10 -------------------------------------------- "
        print str(cu)
        cu._attributes_dump ()

        s_  = cu.state

        while s_ != troy.State.Done and \
              s_ != troy.State.Failed   :

            print "cu : %s"  %  (str(s_))
            time.sleep (1)
            s_ = cu.state

        print "cu : %s"  %  (str(s_))
 
        print " 11 -------------------------------------------- "
        cp1.cancel ()
        cp2.cancel ()
        print " 12 ------------------------------------------- "
        pf.cancel ()
 
    # except Exception, e:
        # print str (e)


 
def main():
    test_compute ()

if __name__ == '__main__':
    main()

