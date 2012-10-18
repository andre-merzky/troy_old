#!/bin/sh

JOBSERVICE_URL=$1
FILESYSTEM_URL=$2
NUMBER_NODES=$3
WORKERS_PER_NODE=$4

if [ -z "${JOBSERVICE_URL}" -o -z "${FILESYSTEM_URL}" -o -z \
    "${NUMBER_NODES}" -o -z "${WORKERS_PER_NODE}" ]; then
    echo "usage: submit_worker.sh <jobservice_url> <filesystem_url> \
<number_nodes> <workers_per_node>"
    exit 1
fi

#diane-submitter Local

#diane-submitter SAGA \
#--jobservice-url=${JOBSERVICE_URL} \
#--filesystem-url=${FILESYSTEM_URL} \
#--diane-number-nodes=${NUMBER_NODES} \
#--diane-workers-per-node=${WORKERS_PER_NODE}

#diane-submitter SAGA \
#--jobservice-url=${JOBSERVICE_URL} \
#--filesystem-url=${FILESYSTEM_URL} \
#--diane-worker-number=${NUMBER_NODES}
#--diane-workers-per-node=${WORKERS_PER_NODE}

#
# Local submitter
#
#diane-submitter Local \
#--diane-worker-number=${NUMBER_NODES}

#
# Plain EGI submitter
#
diane-submitter LCG \
--diane-worker-number=${NUMBER_NODES}

#
# EGI Submitter that uses a "CEs" file that lists the CEs to use.
#
#diane-submitter LCG \
#--diane-worker-number=${NUMBER_NODES} \
#--CE-list=/home/marksant/proj/troy/troy/adaptors/diane/CEs
