# Example on how to display a binary output with matplotlib. Be free to
# adapt it.
# Execution line: python reader.py. After the execution,
# change the arguments.

from pylab import *

filename = "gasdens2.dat"
nx = 384; ny=128

data = fromfile(filename).reshape(ny,nx)
imshow(data,origin='lower')
show()
