#!/usr/bin/env python
#
# This example demonstrates:
# N WorkUnits, to 1 PilotJob, using 1 PilotJobService
#
import time

from troy import Callback
from troy import PilotJobService, PilotJobDescription
from troy import WorkUnitService, WorkUnitDescription
from troy import State

# Initiate the PilotJobService
pjs = PilotJobService()

# Create a PilotJob on Ranger, let the "system" decide which type
pj1_desc = PilotJobDescription()
pj1_desc.number_of_processes = 5
#pj1_desc.total_core_count = 1
#pj1_desc.processes_per_host = 1
#pj1_desc.working_directory = '/home/marksant/agent'
#pj1_desc.working_directory = 'gsiftp://oliver1.loni.org/work/marksant/diane'
#pj1_desc.working_directory = '$PWD'
pj1_desc.working_directory = '.'
#pj1 = pjs.create_pilotjob('fork://localhost', pj1_desc, 'bigjob')
egi_substitutes = {}
#pj1_desc.substitutes = egi_substitutes
print 'pj1_desc:', dir(pj1_desc)
pj1 = pjs.create_pilotjob('ganga://localhost', pj1_desc, 'diane')


# Instantiate a WorkUnitService, 
wus = WorkUnitService()

# Link the PilotJobService we created before
wus.add(pjs)

# Some input
#all_input_files = [ '/data/file1', '/data/file2' ]
all_input_files = [ '0', '1', '2', '3', '4', '5', '6', '7', '8', '9' ]

wu_repo = []

# Create bfast WorkUnits and submit them to the WorkUnitService
for inp in all_input_files:
    wu_desc = WorkUnitDescription()
    #wu_desc.executable = "/bin/bfast"
    #wu_desc.arguments = ["match", "-t4", inp]
    #wu_desc.executable = "/bin/echo"
    #wu_desc.arguments = ["match", "-t4", inp]
    #wu_desc.executable = "/usr/bin/touch"
    #wu_desc.arguments = ["/tmp/bla"]
    wu_desc.executable = "/bin/echo"
    wu_desc.arguments = [inp]
    wu_desc.total_core_count = 1
    wu_desc.file_transfer = []

#    wu_desc.number_of_processes = 1
    #wu_desc.working_directory = '$PWD/'
    wu_desc.working_directory = '.'
    wu_desc.output= 'stdout-%s.txt' % (inp)
    wu_desc.error = 'stderr-%s.txt' % (inp)
    wu = wus.submit(wu_desc)
    wu_repo.append(wu)

while wu_repo:
    for w in wu_repo:
        print 'Workunit: %s (state: %s)' % (w.wu_id, w.get_state())
        
        if w.get_state() == State.Done:
            print 'Workunit is done, removing from list'
            wu_repo.remove(w)
            
    print 'Application going to sleep'
    time.sleep(5)
        
#
# Some work, sleep, etc.
#
