#!/bin/bash 
# The script below is intended to run every night all the tests
# of the test suite, on the latest commit of branch 'develop'.
# As such, it is meant to be placed in the $HOME directory of
# our 'tesla' machine, and launched periodically via cron.
# It is copied into this script subdirectory as a backup. 
# It should be straightforwardly adaptable to another platform.
# Note that it needs the cudpp library to be installed, as some
# tests (those related to irradiation) need this library.
if [ -f ~/.bashrc ]; then . ~/.bashrc; fi
/bin/rm -fr fargo3d
export TERM=linux
export PATH=/opt/openmpi-1.7.2/bin:/usr/local/cuda/bin:$PATH
export LD_LIBRARY_PATH=/opt/openmpi-1.7.2/lib:/usr/local/cuda/lib64:$LD_LIBRARY_PATH
export FARGO_ARCH=TESLAOPENMPI
git clone git@kepler:fargo3d.git
cd fargo3d
git checkout develop
echo "Nightly build test suite" > tests.log
echo "started at `date`" >> tests.log
git log --pretty=format:'FARGO3D Commit: %h' -n 1 >> tests.log
echo -e "\n=======================" >> tests.log
echo " " >> tests.log
python scripts/nightlybuilds.py >& detail.log
echo "Execution finished at `date`" >> tests.log
python scripts/nb_backwards.py >& detail_back.log
echo "Execution finished at `date`" >> backward.log
