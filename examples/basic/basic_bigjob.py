#!/usr/bin/python

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

import troy

COORDINATION_URL = "advert://localhost/?dbtype=sqlite3"

def test_compute ():
    # try:
        cpd = troy.pilot.ComputePilotDescription ()
        cpd['rm'] = 'fork://localhost'

        cpf = troy.pilot.ComputePilotFramework ('bigjob://localhost/')
        cp1 = cpf.submit_pilot (cpd)
        cp2 = cpf.submit_pilot (cpd)

        print "--------------------"
        cpf.dump_()
        print "--------------------"

        cus = troy.pilot.ComputeUnitService ()

        print "--------------------"
        cus.dump_()
        print "--------------------"


        cus.add_compute_pilot (cp1)
        cus.add_compute_pilot (cp2)

        print "--------------------"
        cus.dump_()
        print "--------------------"

        print str(cus.list_compute_pilots ())

        cud = troy.pilot.ComputeUnitDescription ()

        cud['executable'] = '/bin/sh'
        cud['arguments']  = ['-c', 'touch /tmp/hello_troy_bj && sleep 10']

        cu  = cus.submit_compute_unit (cud)

        cu.wait ()

        cp1.cancel ()
        cp2.cancel ()
 
    # except Exception, e:
        # print str (e)


def test_data ():
    # try:
        dpd = troy.pilot.DataPilotDescription ()
        dpf = troy.pilot.DataPilotFramework ('file://localhost')
        dp  = dpf.submit_pilot (dpd)

        dus = troy.pilot.DataUnitService ()
        dus.add_data_pilot (dp)

        dud = troy.pilot.DataUnitDescription ()
        du  = dus.submit_data_unit (dud)
 
    # except Exception, e:
    #     print str (e)


def test_pilot ():
    # try:
        cpd = troy.pilot.ComputePilotDescription ()
        cpf = troy.pilot.ComputePilotFramework ('fork://localhost')
        cp  = cpf.submit_pilot (cpd)

        cus = troy.pilot.ComputeUnitService ()
        cus.add_compute_pilot (cp)

        cud = troy.pilot.ComputeUnitDescription ()
        cu  = cus.submit_compute_unit (cud)
 
    # except Exception, e:
    #     print str (e)

 
def main():
    test_compute ()
    # test_data    ()
    # test_pilot   ()

if __name__ == '__main__':
    main()

