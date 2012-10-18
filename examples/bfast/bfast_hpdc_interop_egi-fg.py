#!/usr/bin/env python
#
import time

from troy import PilotJobService, PilotJobDescription
from troy import WorkUnitService, WorkUnitDescription
from troy import State

egi_substitutes = { 
    'bfast_exe_dir' : './',
    'bfast_tmp_dir' : './',
    'bfast_ref_dir' : './',
    'bfast_reads_dir' : './',
    'bfast_matches_dir' : './'
    }

india_substitutes = dict ( 
    bfast_exe_dir = '/N/u/marksant/proj/bfast/bfast-0.7.0a/bfast',
    bfast_tmp_dir = '/N/u/marksant/data/bfast-small/matchtmp/',
    bfast_ref_dir = '/N/u/marksant/data/bfast-small/hg18chr21_10',
    bfast_reads_dir = '/N/u/marksant/data/bfast-small/reads',
    bfast_matches_dir = '/N/u/marksant/data/bfast-small/matches'
    )

# Local data and program sources
local_bfast_exe_dir = '/home/marksant/proj/bfast/bfast-0.7.0a/bfast'
local_bfast_ref_dir = '/home/marksant/data/bfast-small/hg18chr21_10'
local_bfast_reads_dir = '/home/marksant/data/bfast-small/reads'

# program
bfast_exe = 'bfast'
reffa = 'alt_HuRef_chr21.fa'
NR_INDEXES=10
NR_READS=128
bifs = [ 'alt_HuRef_chr21.fa.cs.%s.1.bif' % x for x in range(1, NR_INDEXES + 1) ]
bfast_reads = [ 'reads.%s.fastq' % x for x in range(1, NR_READS + 1) ]
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
            elif y == 'Uploading' and 'Running' in run_stats[w]:
                print str(run_stats[w]['Running']) + ',',
            elif y == 'Downloading' and 'Done' in run_stats[w]:
                print str(run_stats[w]['Done']) + ',',
            else:
                print '0' + ',',
        print

#
# T = ZERO
#
starttime = time.time()

# Initiate the PilotJobService
pjs = PilotJobService()

# Create a PilotJob on EGI using DIANE
pj1_desc = PilotJobDescription()
pj1_desc.number_of_processes = 64 # number of single-core pilots
#pj1_desc.total_core_count = 2
#pj1_desc.processes_per_host = 8
pj1_desc.working_directory = '.'
pj1_desc.substitutes = egi_substitutes
pj1 = pjs.create_pilotjob('ganga://localhost', pj1_desc, 'diane')

# Create a PilotJob on Future Grid using BigJob
pj2_desc = PilotJobDescription()
pj2_desc.number_of_processes = 8
pj2_desc.total_core_count = 64
pj2_desc.processes_per_host = 8 # on india
pj2_desc.working_directory = '/N/u/marksant/bigjob/'
pj2_desc.substitutes = india_substitutes
pj2 = pjs.create_pilotjob('pbs-ssh://marksant@india.futuregrid.org', 
                            pj2_desc, 'bigjob')

# Instantiate a WorkUnitService, 
wus = WorkUnitService()

# Link the PilotJobService we created before
wus.add(pjs)

# Create bfast WorkUnits and submit them to the WorkUnitService
wu_repo = []
for r in bfast_reads:
    wu_desc = WorkUnitDescription()

    wu_desc.executable = '${bfast_exe_dir}/%s' % bfast_exe

    # output (bfast match file)
    bmf = '{0}.bmf'.format(r)

    wu_desc.number_of_processes = 1

    wu_desc.output = "bfast-stdout.txt"
    wu_desc.error = "bfast-stderr.txt"
    wu_desc.arguments = [
                    'match',
                    '-f', '${bfast_ref_dir}/%s' % reffa,
                    '-A', '1',
                    '-r', '${bfast_reads_dir}/%s' % r,
                    '-n', '1',
                    '-T', '${bfast_tmp_dir}',
                    '-t',
                    '-i', '1-%s' % NR_INDEXES,
                    '>', '${bfast_matches_dir}/%s' % bmf
                    ]

    wu_desc.working_directory = '.' # XXX Does the WU need a working directory
                                    # (conceptually)?
    wu_desc.file_transfer = []
    # the binary
    wu_desc.file_transfer.append('{0}/{1} > {1}'.format(local_bfast_exe_dir, bfast_exe))
    # input referece indexes
    for b in bifs:
        wu_desc.file_transfer.append('{0}/{1} > {1}'.format(local_bfast_ref_dir, b))
    # input brg file
    wu_desc.file_transfer.append('{0}/{1} > {1}'.format(local_bfast_ref_dir, brgs))
    # input read file
    wu_desc.file_transfer.append('{0}/{1} > {1}'.format(local_bfast_reads_dir, r))
    # output file
    wu_desc.file_transfer.append('{0} < {0}'.format(bmf))

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

                if d == 'None' and s == State.Running and \
                        'Running' not in run_stats[w]:
                    run_stats[w]['Running'] = time.time() - starttime

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
