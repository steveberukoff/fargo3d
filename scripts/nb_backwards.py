import subprocess
import time
import os
import numpy as np

#The purpose of this script is to compare the outputs of runs
#performed with the last version on branch 'develop', and the output
#of the same runs with the most recent version aged at least 24
#hours. For this purpose we use some selected test files in
#test_suites. These test files usually produce two directories, test1
#and test2. Here, we only use the output in test1, which we compare in
#the new and old version (we simply compare gasdens1.dat in these two
#directories).

#It is very simple to select a test file for this backward
#compatibility check: just insert a comment in the python test file
#that contains the string 'backward' and it will be used during the
#backward nightly build.

#This functionality should help spot problems if one introduces
#erroneous changes which would not be spotted by the traditional test
#suites (the changes introduced can be dimensionally homogeneous,
#yield same results on CPU and GPU, etc., and they could still be
#wrong !)

#If no changes have been introduced in the last 24 hours, the old and
#new version coincide.

#First we check out the lastest version
os.system ('git checkout develop')
#We seek the files in the test_suite that will be used for the backward compatibility test
out=subprocess.check_output('ls -1 test_suite/*.py | xargs grep -i -l backward', shell=True).split()
TestList = []
#We open the log file,
f=open('backward.log','w')
#then we start the loop on the file names
for i in out:
    command = i.replace('test_suite/','test').replace('.py','')
    name = i.replace('test_suite/','').replace('.py','')
    f.write ('Backward testing on '+name+':')
    f.write (os.popen("git log --pretty=format:' (new:%h) vs' -n 1").read())
    TestList.append (command)
#We initialize the build process
    os.system ("make mrproper")
#We alter the initial python test file: we rename the test as
#'BACKWARD' (this will be the subdirectory used), we set the flag
#'clean' to False (since we want to keep track of the output !) and we
#set 'log' to False, so that these tests do not write in tests.log,
#which has already been written by the traditional nightly built
#suite. The new file thus constructed is called 'test_suite/back.py'
    com_line = "sed -e 's/testname.*,/testname = \"BACKWARD\",/' "+i+"  | sed -e 's/clean.*,/clean=False,log=False,/' > test_suite/back.py"
    os.system (com_line)
# We run the corresponding test
    os.system ("make testback")
# We move the output
    os.system ("mv BACKWARD BACKWARD_NEW")
# We now check out the 'develop' branch as it was 24 hours ago
    os.system ("git checkout `git rev-list -n 1 --before='24 hours ago' develop`")
    f.write (os.popen("git log --pretty=format:' (old:%h)' -n 1").read())
# We rebuild
    os.system ("make mrproper")
# and retest (note: test_suite/back.py is not part of the git distribution so it is not overwritten)
    os.system ("make testback")
    success = False
    file1 = "BACKWARD/test1/gasdens1.dat"
    file2 = "BACKWARD_NEW/test1/gasdens1.dat"
    command = 'diff '+file1+' '+file2
    var = os.popen(command).read()
    if len(var) > 1:
	d0 = np.fromfile(file1)
        d1 = np.fromfile(file2)
	res = np.fabs(d0-d1)/(.5*(d1+d0))
	r=res.max()
	if (r < 1e-13):
		success=True
		f.write (" (max relative diff: "+str(r)+") ")
	else:
		f.write ("\nMax relative difference: "+str(r)+"...FAILED\n")
    else:
	success = True
    if success:
	f.write (" SUCCESS\n")
# We clean everything before using the next file
    os.system ("rm -fr BACKWARD")
    os.system ("rm -fr BACKWARD_NEW")
    os.system ("rm -fr test_suite/back.py")
    os.system ('git checkout develop')
f.close()
