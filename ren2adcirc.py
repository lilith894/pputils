#
#+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!
#                                                                       #
#                                 ren2adcirc2.py                        # 
#                                                                       #
#+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!
#
# Author: Pat Prodanovic, Ph.D., P.Eng.
# 
# Date: June 29, 2015
#
# Purpose: Script takes in a renumbered mesh, and generates the adcirc
# file back. To prevent modification of the John Burkardt's fortran code
# a shift of the cordinates has to take place (as he didn't include enough
# decimal places in the output of x and y). As the files are written from
# adcirc via adcirc2ren.py, the coordinate shift is written there. These same 
# coordinates must be used as input here to get the correct adcirc file.
#
# Uses: Python2.7.9, Matplotlib v1.4.2, Numpy v1.8.2
#
# Example:
#
# python adcirc2ren.py -i out_nodes.txt out_elements.txt -o out_ren.grd -s xref yref
# where:
# -i input adcirc mesh file
# -o output files needed for rcm renumbering
# -s shift x and y coordinates by this amount
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Global Imports
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import os,sys                              # system parameters
import numpy             as np             # numpy
# 
# this is the function that returns True if the elements is oriented CCW
def isCCW((x1,y1),(x2,y2),(x3,y3)):
   return (y3-y1)*(x2-x1) > (y2-y1)*(x3-x1)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# MAIN
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~	
curdir = os.getcwd()
#
# I/O
if len(sys.argv) != 9 :
	print 'Wrong number of Arguments, stopping now...'
	print 'Usage:'
	print 'python adcirc2ren.py -i out_nodes.txt out_elements.txt -o out_ren.grd -s xref yref'
	sys.exit()
dummy1 =  sys.argv[1]
nodes_file = sys.argv[2]
elements_file = sys.argv[3]
dummy2 = sys.argv[4]
adcirc_file = sys.argv[5]
dummy3 = sys.argv[6]
xref = float(sys.argv[7])
yref = float(sys.argv[8])

# to create the output files
nodes_data = np.genfromtxt(nodes_file,unpack=True)
elements_data = np.genfromtxt(elements_file,unpack=True)

# print nodes_data.shape
# print elements_data.shape

fout = open(adcirc_file,"w")

# nodes 
node_id = np.arange(1,len(nodes_data[1,:])+1)
x = nodes_data[0,:] + xref
y = nodes_data[1,:] + yref
z = nodes_data[2,:]

# elements
e1 = elements_data[0,:]
e1 = e1.astype(np.int32)
e2 = elements_data[1,:]
e2 = e2.astype(np.int32)
e3 = elements_data[2,:]
e3 = e3.astype(np.int32)

# construct the ikle numpy array
ikle = np.column_stack((e1,e2,e3))

# go through each element, and make sure it is oriented in CCW fashion
for i in range(len(ikle)):
	
	# if the element is not CCW then must change its orientation
	if not isCCW( (x[ikle[i,0]], y[ikle[i,0]]), (x[ikle[i,1]], y[ikle[i,1]]), 
			(x[ikle[i,2]], y[ikle[i,2]])  ):
		
		t0 = ikle[i,0]
		t1 = ikle[i,1]
		t2 = ikle[i,2]
		
		# switch orientation
		ikle[i,0] = t2
		ikle[i,2] = t0
		
		# print('re-orienting element ' + str(i+1))

# now to write the adcirc mesh file
fout.write("ADCIRC" + "\n")
# writes the number of elements and number of nodes in the header file
fout.write(str(len(e1)) + " " + str(len(node_id)) + "\n")

# writes the nodes
for i in range(0,len(node_id)):
	fout.write(str(node_id[i]) + " " + str("{:.3f}".format(x[i])) + " " + 
		str("{:.3f}".format(y[i])) + " " + str("{:.3f}".format(z[i])) + "\n")

# writes the elements
for i in range(0,len(e1)):
	fout.write(str(i+1) + " 3 " + str(ikle[i,0]) + " " + str(ikle[i,1]) + " " + 
		str(ikle[i,2]) + "\n")	

