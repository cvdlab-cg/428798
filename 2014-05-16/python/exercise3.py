# EXERCISE 3


from pyplasm import *
from collections import *
import sys

""" import modules from lar-cc/lib/py/ """
sys.path.insert(0, '/home/leonardo/lar-cc/lib/py/')
import architectural
from architectural import *

import sysml
from sysml import *


''' Shortcut for the visualization of a LAR model diagram '''
DRAW = COMP([VIEW,STRUCT,MKPOLS])


''' Takes a lar diagram model as input and returns its 
	corresponding HPC (re-)numbered 1-skeleton. '''
def DIAGRAM2NUMBERED_SKELETON(diagram, numScale=1, color=CYAN):
	V,CV = diagram
	hpc_skel = SKEL_1(STRUCT(MKPOLS(diagram)))
	hpc_skel = cellNumbering(diagram, hpc_skel)(range(len(CV)), color, numScale)
	return hpc_skel


''' Views the 1_SKEL of a LAR diagram. '''
VIEW_1_SKEL= COMP([VIEW,DIAGRAM2NUMBERED_SKELETON])


'''	Removes the cells in 'toRemove' from the given diagram 
	and returns the resulting diagram. '''
def REMOVE_CELLS((V,CV), toRemove):
	return V,[cell for k,cell in enumerate(CV) if not (k in toRemove)]


'''	Executes the merge of a list of diagrams against 
	a master's cells list in one time. '''
def MERGE_CELLS(master,diagrams,toMerge):
	V,CV = master
	for i in range(len(CV))[::-1]:
		if i in toMerge:
			k = toMerge.index(i)
			master = diagram2cell(diagrams[k],master,toMerge[k])
	return master


''' Automatizes the loop "merging-numbering-elimination" of blocks, 
	shown in lar-cc/test/py/sysml/text04.py, providing a software 
	interface where a single 3-array of blocks is mapped at the same 
	time against a number of master's blocks. '''
def MNR_CELLS(master, diagrams, toMerge, toRemove):
	# if on between toMerge and toRemove is empty there is no conflict
	if(toMerge and toRemove):
		# elems in diagrams and in toMerge are mapped 1-to-1 thus they must be equally numerous
		if (len(diagrams) == len(toMerge)):
			# foreach cell number in toMerge: decrease it by 1 foreach lower value in toRemove
			for i in range(len(toMerge)):
				c = 0
				for r in toRemove:
					if (toMerge[i] > r):
						c += 1
				toMerge[i] -= c
	# once the fallout of removals has been prevented (re-numbering of cells to merge)
	# the "REMOVE" and "MERGE" operations can be chained safely
	master = REMOVE_CELLS(master, toRemove)
	master = MERGE_CELLS(master, diagrams, toMerge)
	return master



'''	------------ TESTING (lar-cc/test/py/sysml/test04.py) ------------- '''

# INITIAL ASSEMBLY
master = assemblyDiagramInit([5,5,2])([[.3,3.2,.1,5,.3],[.3,4,.1,2.9,.3],[.3,2.7]])
VIEW_1_SKEL(master)
# DIAGRAM REPRESENTING A WALL WITH A DOOR HOLE
diagram1 = assemblyDiagramInit([3,1,2])([[2,1,2],[.3],[2.2,.5]])
VIEW_1_SKEL(diagram1)
# DIAGRAM REPRESENTING A WALL WITH TWO WINDOW HOLES
diagram2 = assemblyDiagramInit([5,1,3])([[1.5,0.9,.2,.9,1.5],[.3],[1,1.4,.3]])
VIEW_1_SKEL(diagram2)

''' MERGE-NUMBERING-REMOVE IS AUTOMATIZED IN ONE SINGLE OPERATION: '''
diagrams = [diagram1, diagram2]
toMerge = [31, 39]
toRemove = [13,33,17,37]
master = MNR_CELLS(master, diagrams, toMerge, toRemove)
VIEW_1_SKEL(master)
DRAW(master)

# REMOVAL OF LAST CELLS PRODUCED BY PREVIOUS MERGINGS
toRemove = [48,54,61]
master = REMOVE_CELLS(master, toRemove)
DRAW(master)
