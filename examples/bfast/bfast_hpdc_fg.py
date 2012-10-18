#!/usr/bin/env python
#
import time

from troy import PilotJobService, PilotJobDescription
from troy import WorkUnitService, WorkUnitDescription
from troy import State

# Program
bfast_exe_dir = '/N/u/marksant/proj/bfast/bfast-0.7.0a/bfast'
bfast_exe = 'bfast'
bfast_tmp_dir = '/N/u/marksant/data/bfast-small/matchtmp/'
bfast_matches_dir = '/N/u/marksant/data/bfast-small/matches'

# Dataset
refdir = '/N/u/marksant/data/bfast-small/hg18chr21_10'
readsdir = '/N/u/marksant/data/bfast-small/reads'
reffa = 'alt_HuRef_chr21.fa'
#bifs = [ 'alt_HuRef_chr21.fa.cs.%s.1.bif' % x for x in range(1, 11) ]
bfast_reads = [ 'reads.%s.fastq' % x for x in range(1, 17) ]
brgs = 'alt_HuRef_chr21.fa.cs.brg'

#
# Helper function for human readable statenames
# Need nices solution
#
def state2str(state):
    if state == State.New:
        return 'New'
    elif state == State.Running:
        return 'Running'
    elif state == State.Done:
        return 'Done'
    elif state == State.Canceled:
        return 'Canceled'
    elif state == State.Failed:
        return 'Failed'
    else:
        return 'Unknown'

def stats():
    print 'Statistics:'

    for y in [ 'ID', 'Unknown', 'New', 'Uploading', 'Running', 'Downloading',
           'Done', 'Cancelled', 'Failed' ]:
        print y + ',',
    print
    for w in run_stats:
        print w.wu_id + ',',
        for y in [ 'Unknown', 'New', 'Uploading', 'Running', 'Downloading',
                    'Done', 'Cancelled', 'Failed' ]:
            if y in run_stats[w]:
                print str(run_stats[w][y]) + ',',
            else:
                print '0' + ',',
        print

#
# T = ZERO
#
starttime = time.time()

# Initiate the PilotJobService
pjs = PilotJobService()

# Create a PilotJob on Future Grid using BigJob
pj1_desc = PilotJobDescription()
pj1_desc.number_of_processes = 1
pj1_desc.total_core_count = len(bfast_reads)
pj1_desc.processes_per_host = 8 # on india
pj1_desc.working_directory = '/N/u/marksant/bigjob/'
#pj1 = pjs.create_pilotjob('ganga://localhost', pj1_desc, 'diane')
pj1 = pjs.create_pilotjob('pbs-ssh://marksant@india.futuregrid.org', 
                            pj1_desc, 'bigjob')

# Instantiate a WorkUnitService, 
wus = WorkUnitService()

# Link the PilotJobService we created before
wus.add(pjs)

# Create bfast WorkUnits and submit them to the WorkUnitService
wu_repo = []
for r in bfast_reads:
    wu_desc = WorkUnitDescription()

    wu_desc.executable = '{0}/{1}'.format(bfast_exe_dir, bfast_exe)

    # output (bfast match file)
    bmf = '{0}.bmf'.format(r)

    wu_desc.number_of_processes = 1

    wu_desc.output = "bfast-stdout.txt"
    wu_desc.error = "bfast-stderr.txt"
    wu_desc.arguments = [
                    'match',
                    '-f', '{0}/{1}'.format(refdir, reffa),
                    '-A', '1',
                    '-r', '{0}/{1}'.format(readsdir, r),
                    '-n', '1',
                    '-T', bfast_tmp_dir,
                    '-t',
                    '-i', '1',
                    '>', '{0}/{1}'.format(bfast_matches_dir, bmf)
                    ]

    wu_desc.working_directory = '.' # XXX Does the WU need a working directory
                                    # (conceptually)?
    #wu_desc.file_transfer = []
    # the binary
    #wu_desc.file_transfer.append('{0}/{1} > {1}'.format(bfast_exe_dir, bfast_exe))
    # input referece indexes
    #for b in bifs:
    #    wu_desc.file_transfer.append('{0}/{1} > {1}'.format(refdir, b))
    # input brg file
    #wu_desc.file_transfer.append('{0}/{1} > {1}'.format(refdir, brgs))
    # input read file
    #wu_desc.file_transfer.append('{0}/{1} > {1}'.format(readsdir, r))
    # output file
    #wu_desc.file_transfer.append('{0} < {0}'.format(bmf))

    wu = wus.submit(wu_desc)
    wu_repo.append(wu)

#
# Main loop for checking progress
#
prev_state = {}
prev_state_detail = {}
run_stats = {}
while wu_repo:
    for w in wu_repo:
        s = w.get_state()

        if w not in run_stats:
            run_stats[w] = {}
        for y in [ 'Done', 'New', 'Cancelled', 'Failed', 'Unknown' ]:
            if state2str(s) == y and y not in run_stats[w]:
                run_stats[w][y] = time.time() - starttime

        if w in prev_state:
            if prev_state[w] != s:
                print 'Workunit %s changed state: %s' % (w.wu_id, state2str(s))
            if s == State.New or s == State.Running:
                d = w.get_state_detail()
                if w in prev_state_detail:
                    if prev_state_detail[w] != d:
                        print 'Workunit %s changed state_detail: %s' % (w.wu_id, d)
                else:
                    print 'Workunit %s entered state_detail: %s' % (w.wu_id, d)

                for y in [ 'Running', 'Downloading', 'Uploading' ]:
                    if d == y and y not in run_stats[w]:
                        run_stats[w][y] = time.time() - starttime

                prev_state_detail[w] = d

            elif s == State.Done:
                print 'Workunit is done, removing from list'
                wu_repo.remove(w)

            elif s == State.Failed:
                print 'Workunit is failed, removing from list'
                wu_repo.remove(w)

        else:
            print 'Workunit %s entered state: %s' % (w.wu_id, state2str(s))

        prev_state[w] = s

    # Sleep at end of loop
    time.sleep(1)
        
# cancel the pilotjobservice (and all its pilots)
pjs.cancel()

stats()


# EOF
