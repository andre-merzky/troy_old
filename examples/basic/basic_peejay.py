#!/usr/bin/python

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

import troy
import time
import pdb

def test_compute ():
    # try:
        t   = troy.Troy ()
        pf  = troy.PilotFramework ('peejay://')

        t.add_pilot_framework (pf)

        
        s   = troy.Scheduler ('Random')
        t.add_scheduler (s)


        cpd  = troy.ComputePilotDescription ()
        cp1  = pf.submit_pilot (cpd)
        cp2  = pf.submit_pilot (cpd)
 
        print str(t.list_pilot_frameworks ())
 
        cud  = troy.ComputeUnitDescription ()
 
        cud['executable'] = '/bin/sh'
        cud['arguments']  = ['-c', 'touch /tmp/hello_troy_pj && sleep 10']
 
        cu  = t.submit_unit (cud)
        s_  = cu.state

        while s_ != troy.State.Done and \
              s_ != troy.State.Failed   :

            print "u : %s"  %  (str(s))
            time.sleep (1)
            s_ = cu.state

        print "cu : %s"  %  (str(s))
 
        cp1.cancel ()
        cp2.cancel ()
        pf.cancel ()
 
    # except Exception, e:
        # print str (e)


 
def main():
    test_compute ()

if __name__ == '__main__':
    main()

