#!/usr/bin/python

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

import troy

def test_compute ():
    # try:
        cpd = troy.pilot.ComputePilotDescription ()
        cpd['queue'] = 'large'
        cpd['key']   = 'val'

        cps = troy.pilot.ComputePilotService ()
        print "cps : " + str (cps)
        print cps.list_pilots ()

        cp1 = cps.create_pilot ("peejay://localhost", cpd)
        cp2 = cps.create_pilot ("peejay://localhost", cpd)

        print str(cps.list_pilots ())

        cus = troy.pilot.ComputeUnitService ()
        cus.add_compute_pilot_service (cps)

        print str(cus.list_compute_pilot_services ())

        cud = troy.pilot.ComputeUnitDescription ()

        cud['executable'] = 'touch'
        cud['arguments']  = ['/tmp/hello_troy', '&&', 'sleep', '10']

        cu  = cus.submit_compute_unit (cud)

        cu.wait ()

        cp1.cancel ()
        cp2.cancel ()
 
    # except Exception, e:
        # print str (e)


def test_data ():
    # try:
        dpd = troy.pilot.DataPilotDescription ()
        dps = troy.pilot.DataPilotService ()
        dp  = dps.create_pilot ("file://localhost", dpd)

        dus = troy.pilot.DataUnitService ()
        dus.add_data_pilot_service (dps)

        dud = troy.pilot.DataUnitDescription ()
        du  = dus.submit_data_unit (dud)
 
    # except Exception, e:
    #     print str (e)


def test_pilot ():
    # try:
        cpd = troy.pilot.ComputePilotDescription ()
        cps = troy.pilot.ComputePilotService ()
        cp  = cps.create_pilot ("fork://localhost", cpd)

        cus = troy.pilot.ComputeUnitService ()
        cus.add_compute_pilot_service (cps)

        cud = troy.pilot.ComputeUnitDescription ()
        cu  = cus.submit_compute_unit (cud)
 
    # except Exception, e:
    #     print str (e)

 
def main():
    test_compute ()
    # test_data    ()
    # test_pilot   ()

if __name__ == "__main__":
    main()

