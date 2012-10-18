#!/usr/bin/env ganga
#-*-python-*-

if __name__ == '__main__':

    from diane.submitters import Submitter

    prog = Submitter()
    prog.parser.description = "Submit worker agents using condor. "+prog.parser.description

    sh_download_wrapper = '''#!/bin/sh
#DOWNLOAD_URL="http://cern.ch/diane/packages"
DOWNLOAD_URL="http://www.cct.lsu.edu/~marksant/packages"
VERSION="2.4"
wget ${DOWNLOAD_URL}/diane-install
python ./diane-install --prefix=$PWD/diane --download-url ${DOWNLOAD_URL} ${VERSION}
$($PWD/diane/install/${VERSION}/bin/diane-env)
diane-worker-start $*
'''

    prog.wrapper = sh_download_wrapper
    prog.initialize()

    for i in range(prog.options.N_WORKERS):
        j = Job()
        j.backend=Condor()
        prog.submit_worker(j)
