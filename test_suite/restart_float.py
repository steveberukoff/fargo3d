import sys
import os
here = os.path.realpath("."); path = sys.path.insert(0,here+"/scripts")
try:
    import test as T
except ImportError:
    print "\nError!!! test module can not be imported. Be sure that you're executing the test from the main directory, using make for that.\n"

description1 = """Testing a restart with the mrif setup (unstratified MRI in single precision)
Initial run is on 6 processors.\n"""
description2 = """Restarting the simulation with 4 processors.\n"""
RestartTest = T.GenericTest(testname = "RESTART_TEST_MRI_FLOAT4",
                            flags1 = "SETUP=mrif  UNITS=0 PARALLEL=1 FARGO_DISPLAY=NONE GPU=0",
                            launch1 = "mpirun -np 6 ./fargo3d -m",
                            description1 = description1,
                            flags2 = "SETUP=mrif PARALLEL=1 FARGO_DISPLAY=NONE GPU=0",
                            launch2 = "mpirun -quiet -np 4 ./fargo3d -S 1 -m",
                            description2 = description2,
                            parfile = "setups/mrif/mrif.par",
                            verbose = True,
                            plot=False,
                            field = "gasdens",
                            compact = True,
                            parameters = {'dt':0.4, 'ninterm':2 ,'ntot':5,
                                          'nx':50, 'ny':25, 'nz':10},
                            clean = False,
                            restore = False,
                            n = 2)

RestartTest.set_commands(command1 = "mkdir RESTART_TEST_MRI_FLOAT4/test2; cp RESTART_TEST_MRI_FLOAT4/test1/* RESTART_TEST_MRI_FLOAT4/test2/",
                         command2 = None)
RestartTest.run()
