#
# This example demonstrates:
# N WorkUnits, to M PilotJob, using 1 PilotJobService
#

#from troy import Callback
from troy import PilotJobService, PilotJobDescription
from troy import WorkUnitService, WorkUnitDescription
from troy import State
import time

# Create our callback class and method
#class MyCallback(Callback):
#    def cb(self, wu, member, value):
#        print 'Called by', wu, 'because ', member, \
#                ' changed, and its new value is:', value
#        
#        return True # Stay registered


# Initiate the PilotJobService
pjs = PilotJobService()

# Create a PilotJob on Ranger, let the "system" decide which type
pj1_desc = PilotJobDescription()
pj1_desc.total_cpu_count = 16
pj1 = pjs.create_pilotjob('gram://ranger', pj1_desc, 'bigjob')
print 'Created PilotJob with ID:', pj1.pj_id

# Create a PilotJob on Kraken, specify that we want a DIANE backend
pj2_desc = PilotJobDescription()
pj2_desc.total_core_count = 16
pj2 = pjs.create_pilotjob('gram://kraken', pj2_desc, 'diane')
print 'Created PilotJob with ID:', pj2.pj_id

# Instantiate a WorkUnitService, 
wus = WorkUnitService()

# Link the PilotJobService we created before
wus.add(pjs)

# Some input
#all_input_files = { '/data/file1', '/data/file2' }

wu_repo = []

# Create bfast WorkUnits and submit them to the WorkUnitService
#for inp in all_input_files:
for inp in range(10):
    wu_desc = WorkUnitDescription()
#    wu_desc.executable = "/bin/bfast"
#    wu_desc.arguments = ["match", "-t4", inp]
    wu_desc.executable = "/bin/echo"
    wu_desc.arguments = [str(inp)]

    wu_desc.total_core_count = 4
    wu = wus.submit(wu_desc)
    wu_repo.append(wu)

#    cb = MyCallback()
#    wu.add_callback('state', cb)


#
# Some work, sleep, etc.
#
while wu_repo:
    for w in wu_repo:
        print 'Workunit: %s (state: %s)' % (w.wu_id, w.get_state())
        
        if w.get_state() == State.Done:
            print 'Workunit is done, removing from list'
            wu_repo.remove(w)
            
    print 'Application going to sleep'
    time.sleep(5)
    
        