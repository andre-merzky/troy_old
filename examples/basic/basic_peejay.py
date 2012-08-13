#!/usr/bin/python

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

import troy

def test_compute ():
    try:
        cpd = troy.pilot.ComputePilotDescription ()

        cps = troy.pilot.ComputePilotService ('peejay://')
        cp1 = cps.submit_pilot (cpd)
        cp2 = cps.submit_pilot (cpd)
 
        cus = troy.pilot.ComputeUnitService ()
        cus.add_pilot_service (cps)
 
        print str(cus.list_pilot_services ())
 
        cud = troy.pilot.ComputeUnitDescription ()
 
        cud['executable'] = '/bin/sh'
        cud['arguments']  = ['-c', 'touch /tmp/hello_troy_pj && sleep 10']
 
        cu  = cus.submit_unit (cud)
 
        cu.wait ()
 
        cp1.cancel ()
        cp2.cancel ()
 
    except Exception, e:
        print str (e)


def test_data ():
    # try:
        dpd = troy.pilot.DataPilotDescription ()
        dps = troy.pilot.DataPilotService ('file://localhost')
        dp  = dps.submit_pilot (dpd)

        dus = troy.pilot.DataUnitService ()
        dus.add_pilot (dp)

        dud = troy.pilot.DataUnitDescription ()
        du  = dus.submit_unit (dud)
 
    # except Exception, e:
    #     print str (e)


def test_pilot ():
    # try:
        cpd = troy.pilot.ComputePilotDescription ()
        cps = troy.pilot.ComputePilotService ('fork://localhost')
        cp  = cps.submit_pilot (cpd)

        cus = troy.pilot.ComputeUnitService ()
        cus.add_pilot_service (cps)

        cud = troy.pilot.ComputeUnitDescription ()
        cu  = cus.submit_unit (cud)
 
    # except Exception, e:
    #     print str (e)

 
def main():
    test_compute ()
    # test_data    ()
    # test_pilot   ()

if __name__ == '__main__':
    main()

