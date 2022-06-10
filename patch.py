from pyapi import generate_xml
import numpy as np
import trimesh
import math
import os

### Simulation properties
sim_parameters = {
	"f_min": 1e9,
	"f_max": 2e9,
	#"port": [[-50,-50,-50],[-50,-50,-49]], #monopole (random)
	"port": [[-1,-37.5,-1.6], [-1,-37.5,0]], ##patch
	"Z": 50,
	"pml_x": 8
}

### Geometry
e_r_xml = 2.2

e_0_xml = 8.8541878128e-12
k_xml = 1e-3 * 2 * math.pi * 2.45e9 * e_0_xml * e_r_xml

# PATCH
objects = {
	"/home/abc/Desktop/api/Part__Feature001.stl": "PEC",
	"/home/abc/Desktop/api/Part__Feature002.stl": [e_r_xml, k_xml],
	"/home/abc/Desktop/api/Part__Feature.stl": "PEC"
}

# MONOPOLE
#objects = {
#	"/home/abc/Desktop/aeg/attempt2_jet/monopole.stl": "PEC"
#}


### Mesh

# Define min and max cell size
factor = 40
factor_space = 10
fraction = 1000
res_fraction = 6
cell_ratio = 2

# Number of mesh lines to apply to local edge
n = [3, 3, 3]

### Generate mesh
unit = 1000 # 1000 = mm
c = 299792458
lambda_min = unit*c/sim_parameters["f_max"]
lambda_max = unit*c/sim_parameters["f_min"]

max_cell = lambda_min/factor
max_cell_space = lambda_min/factor_space
min_cell = lambda_min/fraction

# Generate tetrahedral mesh
mesh = trimesh.load("/home/abc/Desktop/aeg/attempt2_jet/Jet.stl")

# Fetch node coordinates
vertices = mesh.vertices

# Add single mesh line to port
#vertices = np.concatenate(sim_parameters["port"], vertices)
#vertices = np.append(vertices, np.array(sim_parameters["port"][0]))

np.set_printoptions(threshold=np.inf)

# Clear duplicate axis entries
x = np.unique(vertices[:,0])
y = np.unique(vertices[:,1])
z = np.unique(vertices[:,2])

# Refine port
x = np.append(x, [sim_parameters["port"][0][0], sim_parameters["port"][1][0]])
y = np.append(y, [sim_parameters["port"][0][1], sim_parameters["port"][1][1]])
z = np.append(z, [sim_parameters["port"][0][2], sim_parameters["port"][1][2]])

# Apply edge refinement
res = [max_cell/res_fraction, max_cell/res_fraction, max_cell/res_fraction]

mesh = []
for i, axis in enumerate([x,y,z]):
	fine = np.array([])
	for node in axis:
		edge_refinement = np.array([])
		for m in range(-n[i],n[i]+1):
			edge_refinement = np.concatenate((np.array([node+m*res[i]]), edge_refinement))
		fine = np.concatenate((edge_refinement, fine))
	fine.sort()

	"""
	# Detect distances exceeding max cell size
	distances = np.diff(fine)
	while np.where(distances > max_cell)[0].size != 0:
		for j in np.where(distances > max_cell)[0]:
			global_cells = int(distances[j]/max_cell)
			u = np.array([])
			for k in range(-global_cells,global_cells):
				u = np.concatenate((np.array([fine[j+1]+k*(max_cell-0.001)]), u))
			fine = np.concatenate((u, fine))
		fine = np.unique(fine)
		distances = np.diff(fine)
	"""
	mesh.append(fine.tolist())

# Add lambda/4 padding for bounding box
padding = (lambda_min+lambda_max)/8 + sim_parameters["pml_x"]*max_cell

mesh[0] = np.insert(mesh[0], 0, mesh[0][0]-padding)
mesh[0] = np.append(mesh[0], mesh[0][-1]+padding)
mesh[1] = np.insert(mesh[1], 0, mesh[1][0]-padding)
mesh[1] = np.append(mesh[1], mesh[1][-1]+padding)
mesh[2] = np.insert(mesh[2], 0, mesh[2][0]-padding)
mesh[2] = np.append(mesh[2], mesh[2][-1]+padding)

# Global refinement
for i, axis in enumerate(mesh):
	"""
	distances = np.diff(axis)
	while np.where(distances > max_cell)[0].size != 0:
		for j in np.where(distances > max_cell)[0]:
			global_cells = int(distances[j]/max_cell)
			u = np.array([])
			for k in range(-global_cells,global_cells):
				u = np.concatenate((np.array([axis[j+1]+k*(max_cell-0.001)]), u))
			axis = np.concatenate((u, axis))
		axis = np.unique(axis)
		distances = np.diff(axis)
	"""
	# Add line to every vertex
	axis = np.unique(np.concatenate((np.unique(vertices[:,i]), axis)))

	to_delete = (np.argwhere(np.ediff1d(axis) <= min_cell) + 1)
	q = 1
	axis_tmp = axis.copy()
	to_delete_tmp = np.array([])
	while (np.argwhere(np.ediff1d(axis_tmp) <= min_cell) + 1).size > 1:
		to_delete_tmp = np.delete(to_delete, np.arange(0, to_delete.size, q))
		axis_tmp = np.delete(axis, to_delete_tmp)
		q += 1

	if to_delete_tmp.size != 0:
		axis = np.delete(axis, to_delete_tmp)

	j_tot = (np.argwhere(np.abs(np.ediff1d(axis)) >= max_cell) + 1).size
	for count, j in enumerate((np.argwhere(np.abs(np.ediff1d(axis)) >= max_cell) + 1)):
		if count != 0 and count != j_tot-1:
			n = int(np.abs((axis[j-1]-axis[j])/max_cell)+1)
		else:
			n = int(np.abs((axis[j-1]-axis[j])/max_cell_space)+1)
		delta = np.abs(axis[j-1]-axis[j])/n
		for k in range(n):
			axis = np.append(axis, axis[j-1]+k*delta)

	# Assert no cell exceeds minimum cell size (e.g. 35 um trace thickness)
	axis = np.delete(axis, np.argwhere(np.ediff1d(axis) <= min_cell) + 1)

	axis = np.unique(axis)
	axis.sort()
	#axis = np.unique(np.concatenate((np.unique(vertices[:,i]), axis)))

	mesh[i] = axis.tolist()

"""
# [EXPERIMENTAL] Assert neighboring cell ratio
for i, axis in enumerate(mesh):
	axis = np.array(axis)
	distances = np.diff(axis)
	ratios = distances[:-1]/distances[1:]

	count_ratio = 1
	for idx, ratio in enumerate(ratios):
		if ratio > cell_ratio or ratio < 1/cell_ratio:
			axis = np.insert(axis, idx+count_ratio, (axis[idx]+axis[idx+1])/2)
			count_ratio += 1
	mesh[i] = axis.tolist()
"""

# Print dimensions and number of cells
print(str(len(mesh[0]))+"x"+str(len(mesh[1]))+"x"+str(len(mesh[0]))+"="+str(len(mesh[0])*len(mesh[1])*len(mesh[2])))

# Prepare XML
generate_xml(sim_parameters, objects, mesh, output="patch.xml")

#os.rename("/home/abc/Desktop/api/patch.xml", "/home/abc/Desktop/api/sim/patch.xml")
