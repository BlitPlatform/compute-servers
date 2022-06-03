from pyapi import generate_xml
import numpy as np
import trimesh
import math
import os

### Simulation properties
sim_parameters = {
	"f_min": 1e9,
	"f_max": 2e9,
	"port": [[-1,-37.5,-1.6], [-1,-37.5,0]],
	"Z": 50,
	"pml_x": 0
}

### Geometry
e_r_xml = 2.2

e_0_xml = 8.8541878128e-12
k_xml = 1e-3 * 2 * math.pi * 2.45e9 * e_0_xml * e_r_xml

objects = {
	"/home/abc/Desktop/api/Part__Feature001.stl": "PEC",
	"/home/abc/Desktop/api/Part__Feature002.stl": [e_r_xml, k_xml],
	"/home/abc/Desktop/api/Part__Feature.stl": "PEC"
}

#mesh = [
#	[-52.4286,-51.5,-50.5714,-49.6429,-48.7143,-47.7857,-46.8571,-45.9286,-45,-44.0714,-43.1429,-42.2143,-41.2857,-40.3571,-39.4286,-38.5,-37.6084,-36.7168,-35.8252,-34.9337,-34.0421,-33.1505,-32.2589,-31.3673,-30.4584,-29.8092,-29.3454,-28.6962,-27.7872,-26.8635,-25.9399,-25.0162,-24.0925,-23.1688,-22.2451,-21.3214,-20.3977,-19.474,-18.5503,-17.6266,-16.7029,-15.7792,-14.8555,-13.9318,-13.0081,-12.0844,-11.1607,-10.237,-9.31328,-8.38959,-7.46589,-6.54219,-5.61849,-4.69479,-3.77109,-2.8474,-1.9237,-1,-0.0713791,0.857242,1.78586,2.71448,3.6431,4.57173,5.50035,6.42897,7.35759,8.28621,9.21483,10.1435,11.0721,12.0007,12.9293,13.8579,14.7866,15.7152,16.6438,17.5724,18.501,19.4297,20.3583,21.2869,22.2155,23.1441,24.0728,25.0014,25.93,26.8586,27.7872,28.6962,29.3454,29.8092,30.4584,31.3673,32.2589,33.1505,34.0421,34.9337,35.8252,36.7168,37.6084,38.5,39.4286,40.3571,41.2857,42.2143,43.1429,44.0714,45,45.9286,46.8571,47.7857,48.7143,49.6429,50.5714,51.5,52.4286],
#	[-51.6667,-50.8333,-50,-49.1667,-48.3333,-47.5,-46.6667,-45.8333,-45,-44.1667,-43.3333,-42.5,-41.6667,-40.8333,-40,-39.1667,-38.3333,-37.5,-36.5804,-35.6609,-34.7413,-33.8217,-32.9022,-31.9826,-31.063,-30.1435,-29.2239,-28.3043,-27.3847,-26.4652,-25.5456,-24.626,-23.7065,-22.7869,-21.8673,-20.9584,-20.3092,-19.8454,-19.1962,-18.2872,-17.3586,-16.4299,-15.5013,-14.5726,-13.6439,-12.7153,-11.7866,-10.858,-9.92929,-9.00063,-8.07197,-7.14331,-6.21465,-5.28598,-4.35732,-3.42866,-2.5,-1.66667,-0.833333,0,0.833333,1.66667,2.5,3.42866,4.35732,5.28598,6.21465,7.14331,8.07197,9.00063,9.92929,10.858,11.7866,12.7153,13.6439,14.5726,15.5013,16.4299,17.3586,18.2872,19.1962,19.8454,20.3092,20.9584,21.8673,22.7869,23.7065,24.626,25.5456,26.4652,27.3847,28.3043,29.2239,30.1435,31.063,31.9826,32.9022,33.8217,34.7413,35.6609,36.5804,37.5,38.3333,39.1667,40,40.8333,41.6667,42.5,43.3333,44.1667,45,45.8333,46.6667,47.5,48.3333,49.1667,50,50.8333,51.6667],
#	[-14.0483,-13.2297,-12.4112,-11.5927,-10.7741,-9.9556,-9.13707,-8.31853,-7.5,-6.68147,-5.86293,-5.0444,-4.22586,-3.45911,-2.91143,-2.52023,-2.2408,-2.0412,-1.89864,-1.7968,-1.72407,-1.67211,-1.635,-1.60849,-1.58198,-1.55548,-1.52897,-1.50246,-1.47595,-1.44944,-1.42294,-1.39643,-1.36992,-1.34341,-1.3169,-1.2904,-1.26389,-1.23738,-1.21087,-1.18437,-1.15786,-1.13135,-1.10484,-1.07833,-1.05183,-1.02532,-0.99881,-0.972302,-0.945794,-0.919286,-0.892778,-0.86627,-0.839762,-0.813254,-0.786746,-0.760238,-0.73373,-0.707222,-0.680714,-0.654206,-0.627698,-0.60119,-0.574683,-0.548175,-0.521667,-0.495159,-0.468651,-0.442143,-0.415635,-0.389127,-0.362619,-0.336111,-0.309603,-0.283095,-0.256587,-0.230079,-0.203571,-0.177063,-0.150556,-0.124048,-0.0975397,-0.0710317,-0.0445238,-0.0180159,0.00849206,0.035,0.0721111,0.124067,0.196804,0.298637,0.441203,0.640796,0.920225,1.31143,1.85911,2.62586,3.50973,4.3936,5.27746,6.16133,7.0452,7.92906,8.81293,9.6968,10.5807,11.4645,12.3484,13.2323,14.1161,15,15.8839,16.7677,17.6516,18.5355,19.4193,20.3032,21.1871,22.0709]
#]

# Generate mesh ### NOTE THE UNIT (1000) to convert m to mm
c = 299792458
lambda_min = 1000*c/sim_parameters["f_max"]
lambda_max = 1000*c/sim_parameters["f_min"]

# Define max cell size (lambda/15)
factor = 15
max_cell = lambda_min/factor

# Generate tetrahedral mesh
mesh = trimesh.load('/home/abc/Desktop/aeg/attempt2_jet/Jet.stl')

# Fetch node coordinates
vertices = mesh.vertices

# Clear duplicate axis entries
x = np.unique(vertices[:,0])
y = np.unique(vertices[:,1])
z = np.unique(vertices[:,2])

# Edge resolution (step) for each axis
res = [0.5, 0.5, 0.5]

# Number of mesh lines to apply to local edge
n = [3, 3, 3]

# Apply edge refinement
mesh = []
for i, axis in enumerate([x,y,z]):
	fine = np.array([])
	for node in axis:
		edge_refinement = np.array([])
		for m in range(-n[i],n[i]+1):
			edge_refinement = np.concatenate((np.array([node+m*res[i]]), edge_refinement))
		fine = np.concatenate((edge_refinement, fine))
	fine.sort()

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

	mesh.append(fine.tolist())

# Add lambda/4 padding for bounding box
padding = (lambda_min+lambda_max)/8 + sim_parameters["pml_x"]*max_cell

mesh[0] = np.insert(mesh[0], 0, mesh[0][0]-padding)
mesh[0] = np.append(mesh[0], mesh[0][-1]+padding)
mesh[1] = np.insert(mesh[1], 0, mesh[1][0]-padding)
mesh[1] = np.append(mesh[1], mesh[1][-1]+padding)
mesh[2] = np.insert(mesh[2], 0, mesh[2][0]-padding)
mesh[2] = np.append(mesh[2], mesh[2][-1]+padding)

# Post-bounding-box-padding global refinement
for i, axis in enumerate(mesh):
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

	mesh[i] = axis.tolist()

# Prepare XML
generate_xml(sim_parameters, objects, mesh, output="patch.xml")

# Run simulation
os.rename("/home/abc/Desktop/api/patch.xml", "/home/abc/Desktop/api/sim/patch.xml")
