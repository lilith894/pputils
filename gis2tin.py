#
#+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!
#                                                                       #
#                                 gis2tin.py                            # 
#                                                                       #
#+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!
#
# Author: Pat Prodanovic, Ph.D., P.Eng.
# 
# Date: February 2, 2016
#
# Modified: Feb 20, 2016
# Made it work for python 2 and 3
#
# Purpose: Same inputs as gis2triangle.py; calls gis2triangle.py, then
# uses python's subprocess module to call triangle to create the tin, then calls 
# triangle2adcirc.py to produce an adcirc tin file.
#
# Uses: Python 2 or 3, Numpy
#
# Example:
#
# python gis2tin.py -n nodes.csv -b boundary.csv -l lines.csv -h none -o out.grd
#
# where:
#       --> -n is the file listing of all nodes (incl. embedded nodes
#                        if any). The nodes file consist of x,y,z or x,y,z,size;
#                        The size parameter is an optional input, and is used 
#                        by gmsh as an extra parameter that forces element 
#                        size around a particular node. For triangle, it has
#                        no meaning. The nodes file must be comma separated, and
#                        have no header lines. 
#
#       --> -b is the node listing of the outer boundary for the mesh.
#                        The boundary file is generated by snapping lines
#                        to the nodes from the nodes.csv file. The boundary file 
#                        consists of shapeid,x,y of all the lines in the file.
#                        Boundary has to be a closed shape, where first and last 
#                        nodes are identical. Shapeid is a integer, where the
#                        boundary is defined with a distict id (i.e., shapeid 
#                        of 0). 
#
#       --> -l is the node listing of the constraint lines for the mesh.
#                        The lines file can include open or closed polylines.
#                        The file listing has shapeid,x,y, where x,y have to 
#                        reasonable match that of the nodes.csv file. Each distinct
#                        line has to have an individual (integer) shapeid. If no 
#                        constraint lines in the mesh, enter 'none' without the
#                        quotes.
#
#       --> -h is the listing of the holes in the mesh. The holes file is
#                        generated by placing a single node marker inside a
#                        closed line constraint. The holes file must include a 
#                        x,y within the hole boundary. If no holes (islands) 
#                         in the mesh, enter 'none' without the quotes. Note 
#                        that for triangle, the format of the holes file is 
#                        different than for gmsh!!!
#
#      --> -o is the output adcirc file that is the TIN.
# 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Global Imports
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import os,sys                              # system parameters
import numpy             as np             # numpy
from collections import OrderedDict        # for removal of duplicate nodes
import struct                              # to determine sys architecture
import subprocess                          # to execute binaries
curdir = os.getcwd()
#
#
# determine which version of python the user is running
if (sys.version_info > (3, 0)):
	version = 3
	pystr = 'python3'
elif (sys.version_info > (2, 7)):
	version = 2
	pystr = 'python'
#
# I/O
if len(sys.argv) == 11 :
	dummy1 =  sys.argv[1]
	nodes_file = sys.argv[2]
	dummy2 =  sys.argv[3]
	boundary_file = sys.argv[4]
	dummy3 =  sys.argv[5]
	lines_file = sys.argv[6]
	dummy4 =  sys.argv[7]
	holes_file = sys.argv[8]
	dummy5 =  sys.argv[9]
	output_file = sys.argv[10]
else:
	print('Wrong number of Arguments, stopping now...')
	print('Usage:')
	print('python gis2tin.py -n nodes.csv -b boundary.csv -l lines.csv -h holes.csv -o out.grd')
	sys.exit()

# to determine if the system is 32 or 64 bit
archtype = struct.calcsize("P") * 8

# Tell the user what is going on
print('Constructing Triangle poly file ...')

# call gis2triangle.py
subprocess.call([pystr, 'gis2triangle_kd.py', '-n', nodes_file, 
	'-b', boundary_file, '-l', lines_file, '-h', holes_file, 
	'-o', 'tin.poly'])

if (os.name == 'posix'):
	# this assumes chmod +x has already been applied to the binaries
	if (archtype == 32):
		subprocess.call( ['./triangle/bin/triangle_32', 'tin.poly' ] )
	else:
		subprocess.call( ['./triangle/bin/triangle_64', 'tin.poly' ] )
elif (os.name == 'nt'):
	subprocess.call( ['.\\triangle\\bin\\triangle_32.exe', 'tin.poly' ] )
else:
	print('OS not supported!')
	print('Exiting!')
	sys.exit()
	
# call triangle2adcirc.py
subprocess.call([pystr, 'triangle2adcirc.py', '-n', 'tin.1.node', 
	'-e', 'tin.1.ele', '-o', output_file])

# to remove the temporary files
os.remove('tin.poly')
os.remove('tin.1.poly')
os.remove('tin.1.node')
os.remove('tin.1.ele')

print('All done!')

