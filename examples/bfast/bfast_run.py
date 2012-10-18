# tell DIANE that we are just running executables
# the ExecutableApplication module is a standard DIANE test application

import ExecutableApplication as application

bfast_exe_dir = '../../bfast/bfast-0.7.0a/bfast/'
bfast_exe = 'bfast'
refdir = '/home/marksant/data/bfast-small/hg18chr21_10/'
reffa = 'alt_HuRef_chr21.fa'
bifs = [ 
    'alt_HuRef_chr21.fa.cs.1.1.bif',
    'alt_HuRef_chr21.fa.cs.2.1.bif', 
    'alt_HuRef_chr21.fa.cs.3.1.bif',
    'alt_HuRef_chr21.fa.cs.4.1.bif',
    'alt_HuRef_chr21.fa.cs.5.1.bif',
    'alt_HuRef_chr21.fa.cs.6.1.bif',
    'alt_HuRef_chr21.fa.cs.7.1.bif',
    'alt_HuRef_chr21.fa.cs.8.1.bif',
    'alt_HuRef_chr21.fa.cs.9.1.bif',
    'alt_HuRef_chr21.fa.cs.10.1.bif'
    ]
brgs = [ 
    'alt_HuRef_chr21.fa.cs.brg',  # Color Space
    # 'alt_HuRef_chr21.fa.nt.brg' # Nucleotide
    ]
readdir = '/home/marksant/data/bfast-small/reads/'
#bmf = 'bfast.matches.file.hg21.1.bmf'
bfast_reads = [ 
    'reads.1.fastq',
    'reads.2.fastq',
    'reads.3.fastq',
    'reads.4.fastq',
    'reads.5.fastq',
    'reads.6.fastq',
    'reads.7.fastq',
    'reads.8.fastq',
    'reads.9.fastq',
    'reads.10.fastq',
    'reads.11.fastq',
    'reads.12.fastq',
    'reads.13.fastq',
    'reads.14.fastq',
    'reads.15.fastq',
    'reads.16.fastq',
#    'reads.17.fastq',
#    'reads.18.fastq',
#    'reads.19.fastq',
#    'reads.20.fastq',
#    'reads.21.fastq',
#    'reads.22.fastq',
#    'reads.23.fastq',
#    'reads.24.fastq',
#    'reads.25.fastq',
#    'reads.26.fastq',
#    'reads.27.fastq',
#    'reads.28.fastq',
#    'reads.29.fastq',
#    'reads.30.fastq',
#    'reads.31.fastq',
#    'reads.32.fastq'
]
bfast_tmp_dir = './'

# the run function is called when the master is started
# input.data stands for run parameters
def run(input,config):

	d = input.data.task_defaults # this is just a convenience shortcut

	# all tasks will share the default parameters (unless set otherwise in individual task)
	d.input_files = []
	d.input_files.append(bfast_exe_dir + bfast_exe)
        for b in bifs:
            d.input_files.append(refdir + b)
        for b in brgs:
            d.input_files.append(refdir + b)
        for r in bfast_reads:
            d.input_files.append(readdir + r)

	d.output_files = ['message.out']
	d.executable = bfast_exe

	# here are tasks differing by arguments to the executable
	for r in bfast_reads:
		t = input.data.newTask()
                t.args = [ 
                    'match',
                    '-f', reffa,
                    '-A', '1',
                    '-r', r,
                    '-n', '1',
                    '-T', bfast_tmp_dir,
                    '-t'
                    ]
