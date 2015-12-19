#
#+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!
#                                                                       #
#                                 triangle2adcirc.py                    # 
#                                                                       #
#+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!
#
# Author: Pat Prodanovic, Ph.D., P.Eng.
# 
# Date: June 26, 2015
#
# Purpose: Script takes files generated by triangle mesh generator, and 
# converts them to an ADCIRC mesh format
#
# Uses: Python2.7.9, Matplotlib v1.4.2, Numpy v1.8.2
#
# Example:
#
# python triangle2adcirc.py -n out.1.node -e out.1.ele -o out.14
# where:
# -n nodes file generated by triangle
# -e elements file generated by triangle
# -o output adcirc mesh file
# 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Global Imports
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import os,sys                              # system parameters
#import matplotlib.tri    as mtri           # matplotlib triangulations
import numpy             as np             # numpy
import math                                # for the ceil function
curdir = os.getcwd()
#
#
# I/O
if len(sys.argv) != 7 :
	print 'Wrong number of Arguments, stopping now...'
	print 'Usage:'
	print 'python triangle2adcirc.py -n out.1.node -e out.1.ele -o out.14'
	sys.exit()
dummy1 =  sys.argv[1]
nodes_file = sys.argv[2]
dummy2 =  sys.argv[3]
elements_file = sys.argv[4]
dummy3 =  sys.argv[5]
output_file = sys.argv[6]

# to create the output file
fout = open(output_file,"w")

# use numpy to read the file
# each column in the file is a row in data read by no.loadtxt method
nodes_data = np.genfromtxt(nodes_file,skip_header=1,comments="#",unpack=True)
elements_data = np.genfromtxt(elements_file,skip_header=1,comments="#",unpack=True)

# nodes in the input file
node_id = nodes_data[0,:]
node_id = node_id.astype(np.int32)
x = nodes_data[1,:]
y = nodes_data[2,:]
z = nodes_data[3,:]

# elements in the input file
element_id = elements_data[0,:]
element_id = element_id.astype(np.int32)
e1 = elements_data[1,:]
e1 = e1.astype(np.int32)
e2 = elements_data[2,:]
e2 = e2.astype(np.int32)
e3 = elements_data[3,:]
e3 = e3.astype(np.int32)

# now to write the adcirc mesh file
fout.write("ADCIRC" + "\n")
# writes the number of elements and number of nodes in the header file
fout.write(str(len(element_id)) + " " + str(len(node_id)) + "\n")

# writes the nodes
for i in range(0,len(node_id)):
	fout.write(str(node_id[i]) + " " + str("{:.3f}".format(x[i])) + " " + 
		str("{:.3f}".format(y[i])) + " " + str("{:.3f}".format(z[i])) + "\n")

# writes the elements
for i in range(0,len(element_id)):
	fout.write(str(element_id[i]) + " 3 " + str(e1[i]) + " " + str(e2[i]) + " " + 
		str(e3[i]) + "\n")	
	

