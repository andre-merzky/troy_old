#!/usr/bin/env python

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

import troy
import time
import pudb

PF_URL = "bigjob+redis://ILikeBigJob_wITH-REdIS@gw68.quarry.iu.teragrid.org:6379"
PF_URL = "bigjob+redis://localhost:6379"

pudb.set_interrupt_handler ()

def test_compute ():
    # try:
        print " 1 -------------------------------------------- "
        t   = troy.Troy ()
        print " 2 -------------------------------------------- "
        pf  = troy.PilotFramework (PF_URL)

        print " 3 -------------------------------------------- "
        t.add_pilot_framework (pf)

        print " 4 -------------------------------------------- "
      # pudb.set_trace()
        s   = troy.Scheduler ('RandomOrNot')
        print "RANDOM"
        print str(s)
        t.add_scheduler (s)

        print " 5 -------------------------------------------- "
        cpd  = troy.ComputePilotDescription ()

        cpd.service_url         = 'fork://localhost'
        cpd.working_directory   = '/home/merzky/.bigjob/agent'
        cpd.number_of_processes = 1


        print " 6 -------------------------------------------- "
        cp1  = pf.submit_pilot (cpd)

        print " 7 -------------------------------------------- "
        cp2  = pf.submit_pilot (cpd)

        print " 8 -------------------------------------------- "

        for id in t.list_pilot_frameworks () :
            print "pf: " + str (id) + " : "
            print "    " + str (troy.PilotFramework(id).list_pilots())

        print " 9 -------------------------------------------- "
        cud  = troy.ComputeUnitDescription ()

        cud['executable'] = '/usr/bin/touch'
        cud['arguments']  = ['/tmp/hello_troy_pj']

        print " 10 ------------------------------------------- "
        cu  = t.submit_unit (cud)

        print " 11 ------------------------------------------- "
        s_  = cu.state

        while s_ != troy.State.Done and \
              s_ != troy.State.Failed   :

            print "cu : %s"  %  (str(s_))
            time.sleep (1)
          # pudb.set_trace()
            s_ = cu.state

        print "cu : %s"  %  (str(s_))

        print " 11 -------------------------------------------- "
        cp1.cancel ()
        cp2.cancel ()
        print " 12 ------------------------------------------- "
        pf.cancel ()
 
    # except Exception, e:
    #     print str (e)


 
def main():
    test_compute ()

if __name__ == '__main__':
    main()

