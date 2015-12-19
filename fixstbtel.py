#
#+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!
#                                                                       #
#                                 fixstbtel.py                          # 
#                                                                       #
#+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!
#
# Author: Pat Prodanovic, Ph.D., P.Eng.
# 
# Date: July 27, 2015
#
# Purpose: Script takes the file generated by TELEMAC's STBTEL mesh
# mesh conversion utility, and deletes the duplicate time record so 
# that the file can be used in parallel TELEMAC simulations. 
#
# Uses: Python2.7.9, Matplotlib v1.4.2, Numpy v1.8.2
#
# Example:
#
# python fixstbtel.py -i out.slf -o out_fixed.slf
# where:
# -i input *.slf file generated by STBTEL utility
# -o output *.slf fixed
# 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Global Imports
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import os,sys                              # system parameters
import matplotlib.tri    as mtri           # matplotlib triangulations
import numpy             as np             # numpy
from ppmodules.selafin_io import *
#
# I/O
if len(sys.argv) != 5 :
	print 'Wrong number of Arguments, stopping now...'
	print 'Usage:'
	print 'python fixstbtel.py -i out.slf -o out_fixed.slf'
	sys.exit()
dummy1 =  sys.argv[1]
input_file = sys.argv[2]
dummy2 =  sys.argv[3]
output_file = sys.argv[4]

# reads the input SELAFIN file
inp = SELAFIN(input_file)

# this is the output file
# now to write the SELAFIN mesh file
out = SELAFIN('')

#print '     +> Set SELAFIN variables'
out.TITLE = 'Fixed from STBTEL'
out.NBV1 = 1 
out.NVAR = 1
out.VARINDEX = range(out.NVAR)
out.VARNAMES.append('BOTTOM          ')
out.VARUNITS.append('M               ')

#print '     +> Set SELAFIN sizes'
out.NPLAN = 1
out.NDP2 = 3
out.NDP3 = 3
out.NPOIN2 = inp.NPOIN2
out.NPOIN3 = inp.NPOIN3
out.NELEM2 = inp.NELEM2
out.NELEM3 = inp.NELEM2
out.IPARAM = [1, 0, 0, 0, 0, 0, 0, 0, 0, 0]

#print '     +> Set SELAFIN mesh'
out.MESHX = inp.MESHX
out.MESHY = inp.MESHY

#print '     +> Set SELAFIN IPOBO'
out.IPOB2 = inp.IPOB2
out.IPOB3 = inp.IPOB3

#print '     +> Set SELAFIN IKLE'
out.IKLE2 = inp.IKLE2
out.IKLE3 = inp.IKLE3

#print '     +> Set SELAFIN times and cores'
# these two lists are empty after constructor is instantiated
out.tags['cores'].append(0)
out.tags['times'].append(0)

#out.tags = { 'times':[0] } # time (sec)
#out.DATETIME = sel.DATETIME
out.DATETIME = [2015, 1, 1, 1, 1, 1]
#out.tags = { 'cores':[long(0)] } # time frame 

#print '     +> Write SELAFIN headers'
out.fole.update({ 'hook': open(output_file,'w') })
out.fole.update({ 'name': 'Fixed from STBTEL' })
out.fole.update({ 'endian': ">" })     # big endian
out.fole.update({ 'float': ('f',4) })  # single precision

out.appendHeaderSLF()
out.appendCoreTimeSLF(0) 

# gets the values at time index zero for all variables
# but, in the file generated by stbtel, there will be only one variable
values = inp.getVALUES(0)

z = np.zeros(inp.NPOIN2)
z = values[0,:]

out.appendCoreVarsSLF([z])


