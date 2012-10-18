#!/bin/sh

#BASE=/home/cctsg/software/troy_trunk/troy/adaptors/diane/troy_diane_backend
BASE=$(dirname $0)
echo $BASE
#export PYTHONPATH=$PYTHONPATH:$BASE/troy_diane_backend
export PYTHONPATH=$PYTHONPATH:$BASE
#env ORBendPoint=giop:tcp:130.39.12.221:22000 diane-run $BASE/troy_diane_backend/troy_diane_backend.run&
diane-run $BASE/troy_diane_backend/troy_diane_backend.run
