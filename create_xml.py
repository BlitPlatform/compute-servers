import xml.etree.cElementTree as ET
import xml.dom.minidom
import math
import os

#### [ ]: To do
#### [x]: Done

### [x] Excitation
f_min_xml = 1e9 # Start frequency [Hz]
f_max_xml = 2e9 # Stop frequency [Hz]

f_min_xml = int(f_min_xml)
f_max_xml = int(f_max_xml)
f0_xml = int((f_min_xml+f_max_xml)/2)
fc_xml = int(f_max_xml-f0_xml)

### [x] Geometry
e_r_xml = 2.2

e_0_xml = 8.8541878128e-12
k_xml = 1e-3 * 2 * math.pi * 2.45e9 * e_0_xml * e_r_xml

objects = {
"/home/abc/Desktop/pyapi/Part__Feature001.stl": "PEC",
"/home/abc/Desktop/pyapi/Part__Feature002.stl": [e_r_xml, k_xml],
"/home/abc/Desktop/pyapi/Part__Feature.stl": "PEC"
}

### [x] Mesh
# coarse
#mesh = [
#[-97,-90.5,-84,-77.5,-71,-64.5,-58,-51.5,-45,-38.5,-34.446575557,-30.73664388925,-27.0267122215,-16.6389035518,-8.8194517759,-1,7.8194517759,16.6389035518,27.0267122215,30.73664388925,34.446575557,38.5,45,51.5,58,64.5,71,77.5,84,90.5,97],
#[-105,-97.5,-90,-82.5,-75,-67.5,-60,-52.5,-45,-37.5,-24.946575557,-17.5267122215,-10.01335611075,-2.5,2.5,10.01335611075,17.5267122215,24.946575557,37.5,45,52.5,60,67.5,75,82.5,90,97.5,105],
#[-17.3684266666667,-16.1348733333333,-14.90132,-13.6677666666667,-12.4342133333333,-11.20066,-9.96710666666667,-8.73355333333333,-7.5,-6.26644666666667,-5.03289333333333,-3.5054,-2.41433333333333,-1.635,-1.07833333333333,-0.521666666666667,0.035,0.814333333333333,1.9054,3.43289333333333,5.571384,8.56527093333333,11.7826354666667,15,18.2173645333333,21.4347290666667,24.6520936,27.8694581333333,31.0868226666667,34.3041872,37.5215517333333,40.7389162666667]
#]

# fine
mesh = [
[-52.4286,-51.5,-50.5714,-49.6429,-48.7143,-47.7857,-46.8571,-45.9286,-45,-44.0714,-43.1429,-42.2143,-41.2857,-40.3571,-39.4286,-38.5,-37.6084,-36.7168,-35.8252,-34.9337,-34.0421,-33.1505,-32.2589,-31.3673,-30.4584,-29.8092,-29.3454,-28.6962,-27.7872,-26.8635,-25.9399,-25.0162,-24.0925,-23.1688,-22.2451,-21.3214,-20.3977,-19.474,-18.5503,-17.6266,-16.7029,-15.7792,-14.8555,-13.9318,-13.0081,-12.0844,-11.1607,-10.237,-9.31328,-8.38959,-7.46589,-6.54219,-5.61849,-4.69479,-3.77109,-2.8474,-1.9237,-1,-0.0713791,0.857242,1.78586,2.71448,3.6431,4.57173,5.50035,6.42897,7.35759,8.28621,9.21483,10.1435,11.0721,12.0007,12.9293,13.8579,14.7866,15.7152,16.6438,17.5724,18.501,19.4297,20.3583,21.2869,22.2155,23.1441,24.0728,25.0014,25.93,26.8586,27.7872,28.6962,29.3454,29.8092,30.4584,31.3673,32.2589,33.1505,34.0421,34.9337,35.8252,36.7168,37.6084,38.5,39.4286,40.3571,41.2857,42.2143,43.1429,44.0714,45,45.9286,46.8571,47.7857,48.7143,49.6429,50.5714,51.5,52.4286],
[-51.6667,-50.8333,-50,-49.1667,-48.3333,-47.5,-46.6667,-45.8333,-45,-44.1667,-43.3333,-42.5,-41.6667,-40.8333,-40,-39.1667,-38.3333,-37.5,-36.5804,-35.6609,-34.7413,-33.8217,-32.9022,-31.9826,-31.063,-30.1435,-29.2239,-28.3043,-27.3847,-26.4652,-25.5456,-24.626,-23.7065,-22.7869,-21.8673,-20.9584,-20.3092,-19.8454,-19.1962,-18.2872,-17.3586,-16.4299,-15.5013,-14.5726,-13.6439,-12.7153,-11.7866,-10.858,-9.92929,-9.00063,-8.07197,-7.14331,-6.21465,-5.28598,-4.35732,-3.42866,-2.5,-1.66667,-0.833333,0,0.833333,1.66667,2.5,3.42866,4.35732,5.28598,6.21465,7.14331,8.07197,9.00063,9.92929,10.858,11.7866,12.7153,13.6439,14.5726,15.5013,16.4299,17.3586,18.2872,19.1962,19.8454,20.3092,20.9584,21.8673,22.7869,23.7065,24.626,25.5456,26.4652,27.3847,28.3043,29.2239,30.1435,31.063,31.9826,32.9022,33.8217,34.7413,35.6609,36.5804,37.5,38.3333,39.1667,40,40.8333,41.6667,42.5,43.3333,44.1667,45,45.8333,46.6667,47.5,48.3333,49.1667,50,50.8333,51.6667],
[-14.0483,-13.2297,-12.4112,-11.5927,-10.7741,-9.9556,-9.13707,-8.31853,-7.5,-6.68147,-5.86293,-5.0444,-4.22586,-3.45911,-2.91143,-2.52023,-2.2408,-2.0412,-1.89864,-1.7968,-1.72407,-1.67211,-1.635,-1.60849,-1.58198,-1.55548,-1.52897,-1.50246,-1.47595,-1.44944,-1.42294,-1.39643,-1.36992,-1.34341,-1.3169,-1.2904,-1.26389,-1.23738,-1.21087,-1.18437,-1.15786,-1.13135,-1.10484,-1.07833,-1.05183,-1.02532,-0.99881,-0.972302,-0.945794,-0.919286,-0.892778,-0.86627,-0.839762,-0.813254,-0.786746,-0.760238,-0.73373,-0.707222,-0.680714,-0.654206,-0.627698,-0.60119,-0.574683,-0.548175,-0.521667,-0.495159,-0.468651,-0.442143,-0.415635,-0.389127,-0.362619,-0.336111,-0.309603,-0.283095,-0.256587,-0.230079,-0.203571,-0.177063,-0.150556,-0.124048,-0.0975397,-0.0710317,-0.0445238,-0.0180159,0.00849206,0.035,0.0721111,0.124067,0.196804,0.298637,0.441203,0.640796,0.920225,1.31143,1.85911,2.62586,3.50973,4.3936,5.27746,6.16133,7.0452,7.92906,8.81293,9.6968,10.5807,11.4645,12.3484,13.2323,14.1161,15,15.8839,16.7677,17.6516,18.5355,19.4193,20.3032,21.1871,22.0709]
]

### [x] Boundaries
# Number of cells for PML
pml_x_xml = 8

# Bounding box
bounds_xml = [
[mesh[0][int(pml_x_xml)], mesh[0][-int(pml_x_xml)-1]],
[mesh[1][int(pml_x_xml)], mesh[1][-int(pml_x_xml)-1]],
[mesh[2][int(pml_x_xml)], mesh[2][-int(pml_x_xml)-1]],
]

# Conditions
xmin_xml = "PML_"+str(int(pml_x_xml))
xmax_xml = "PML_"+str(int(pml_x_xml))
ymin_xml = "PML_"+str(int(pml_x_xml))
ymax_xml = "PML_"+str(int(pml_x_xml))
zmin_xml = "PML_"+str(int(pml_x_xml))
zmax_xml = "PML_"+str(int(pml_x_xml))

### [x] Port
Z_xml = 50 # Impedance [Ohm]
start_xml = [-1,-37.5,-1.6]
stop_xml = [-1,-37.5,0]

# Auto-detect excitation vector
direction_xml = [0,0,0]
for i, (u, v) in enumerate(zip(start_xml, stop_xml)):
	if u < v:
		direction_xml[i] = 1
	elif u > v:
		direction_xml[i] = -1

for i, u in enumerate(direction_xml):
	if u == 0:
		direction_xml[i] = "-0"
	else:
		direction_xml[i] = str(-u)

if "1" in direction_xml:
	dir_idx_xml = direction_xml.index("1")
else:
	dir_idx_xml = direction_xml.index("-1")

direction_xml = ",".join(str(x) for x in direction_xml)


### [ ] Monitors


### Generate XML
openEMS = ET.Element("openEMS")

## Simulation
FDTD = ET.SubElement(openEMS, "FDTD", NumberOfTimesteps="60000", endCriteria="1e-05", f_max=str(f_max_xml))
Excitation = ET.SubElement(FDTD, "Excitation", Type="0", f0=str(f0_xml), fc=str(fc_xml))
Excitation.text = "$"
BoundaryCond = ET.SubElement(FDTD, "BoundaryCond", xmin=xmin_xml, xmax=xmax_xml, ymin=ymin_xml, ymax=ymax_xml, zmin=zmin_xml, zmax=zmax_xml)
BoundaryCond.text = "$"

ContinuousStructure = ET.SubElement(openEMS, "ContinuousStructure", CoordSystem="0")
Properties = ET.SubElement(ContinuousStructure, "Properties")

## CAD
for i, (k, v) in enumerate(objects.items()):
	# Determine material
	if v == "PEC": # PEC
		Metal = ET.SubElement(Properties, "Metal", Name="metal_xml_"+str(i))
		Primitives = ET.SubElement(Metal, "Primitives")
		PolyhedronReader = ET.SubElement(Primitives, "PolyhedronReader", Priority="10", FileName=str(k), FileType="STL")
		PolyhedronReader.text = "$"
	else: # Dielectric
		Material = ET.SubElement(Properties, "Material", Name="material_xml_"+str(i))
		Property = ET.SubElement(Material, "Property", Epsilon=str(v[0]), Kappa=str(v[1]))
		Property.text = "$"
		Primitives = ET.SubElement(Material, "Primitives")
		PolyhedronReader = ET.SubElement(Primitives, "PolyhedronReader", Priority="1", FileName=str(k), FileType="STL")
		PolyhedronReader.text = "$"

## Port
LumpedElement = ET.SubElement(Properties, "LumpedElement", Name="port_resist_1", Direction=str(dir_idx_xml), Caps="1", R=str(Z_xml))
Primitives = ET.SubElement(LumpedElement, "Primitives")
Box = ET.SubElement(Primitives, "Box", Priority="5")
P1 = ET.SubElement(Box, "P1", X=str(start_xml[0]), Y=str(start_xml[1]), Z=str(start_xml[2]))
P2 = ET.SubElement(Box, "P2", X=str(stop_xml[0]), Y=str(stop_xml[1]), Z=str(stop_xml[2]))
P1.text = "$"
P2.text = "$"

Excitation = ET.SubElement(Properties, "Excitation", Name="port_excite_1", Type="0", Excite=str(direction_xml))
Primitives = ET.SubElement(Excitation, "Primitives")
Box = ET.SubElement(Primitives, "Box", Priority="5")
P1 = ET.SubElement(Box, "P1", X=str(start_xml[0]), Y=str(start_xml[1]), Z=str(start_xml[2]))
P2 = ET.SubElement(Box, "P2", X=str(stop_xml[0]), Y=str(stop_xml[1]), Z=str(stop_xml[2]))
P1.text = "$"
P2.text = "$"

##\ Voltage probe
ProbeBox = ET.SubElement(Properties, "ProbeBox", Name="port_ut1", Type="0", Weight="-1")
Primitives = ET.SubElement(ProbeBox, "Primitives")
Box = ET.SubElement(Primitives, "Box", Priority="5")
P1 = ET.SubElement(Box, "P1", X=str(start_xml[0]), Y=str(start_xml[1]), Z=str(start_xml[2]))
P2 = ET.SubElement(Box, "P2", X=str(stop_xml[0]), Y=str(stop_xml[1]), Z=str(stop_xml[2]))
P1.text = "$"
P2.text = "$"

# Current probe
ProbeBox = ET.SubElement(Properties, "ProbeBox", Name="port_it1", Type="1", Weight="1", NormDir="2")
Primitives = ET.SubElement(ProbeBox, "Primitives")
Box = ET.SubElement(Primitives, "Box", Priority="5")
P1 = ET.SubElement(Box, "P1", X=str((start_xml[0]+stop_xml[0])/2), Y=str((start_xml[1]+stop_xml[1])/2), Z=str((start_xml[2]+stop_xml[2])/2))
P2 = ET.SubElement(Box, "P2", X=str((start_xml[0]+stop_xml[0])/2), Y=str((start_xml[1]+stop_xml[1])/2), Z=str((start_xml[2]+stop_xml[2])/2))
P1.text = "$"
P2.text = "$"

## Field monitors
DumpBox = ET.SubElement(Properties, "DumpBox", Name="Ht_", DumpMode="2", DumpType="1")
Primitives = ET.SubElement(DumpBox, "Primitives")
Box = ET.SubElement(Primitives, "Box", Priority="0")
P1 = ET.SubElement(Box, "P1", X="-59", Y="-40", Z="2.6")
P2 = ET.SubElement(Box, "P2", X="59", Y="40", Z="2.6")
P1.text = "$"
P2.text = "$"

## Boundaries
DumpBox = ET.SubElement(Properties, "DumpBox", Name="nf2ff_E_xn", DumpMode="1", DumpType="0", FileType="1")
Primitives = ET.SubElement(DumpBox, "Primitives")
Box = ET.SubElement(Primitives, "Box", Priority="0")
P1 = ET.SubElement(Box, "P1", X=str(bounds_xml[0][0]), Y=str(bounds_xml[1][0]), Z=str(bounds_xml[2][0]))
P2 = ET.SubElement(Box, "P2", X=str(bounds_xml[0][0]), Y=str(bounds_xml[1][1]), Z=str(bounds_xml[2][1]))
P1.text = "$"
P2.text = "$"

DumpBox = ET.SubElement(Properties, "DumpBox", Name="nf2ff_H_xn", DumpMode="1", DumpType="1", FileType="1")
Primitives = ET.SubElement(DumpBox, "Primitives")
Box = ET.SubElement(Primitives, "Box", Priority="0")
P1 = ET.SubElement(Box, "P1", X=str(bounds_xml[0][0]), Y=str(bounds_xml[1][0]), Z=str(bounds_xml[2][0]))
P2 = ET.SubElement(Box, "P2", X=str(bounds_xml[0][0]), Y=str(bounds_xml[1][1]), Z=str(bounds_xml[2][1]))
P1.text = "$"
P2.text = "$"

DumpBox = ET.SubElement(Properties, "DumpBox", Name="nf2ff_E_xp", DumpMode="1", DumpType="0", FileType="1")
Primitives = ET.SubElement(DumpBox, "Primitives")
Box = ET.SubElement(Primitives, "Box", Priority="0")
P1 = ET.SubElement(Box, "P1", X=str(bounds_xml[0][1]), Y=str(bounds_xml[1][0]), Z=str(bounds_xml[2][0]))
P2 = ET.SubElement(Box, "P2", X=str(bounds_xml[0][1]), Y=str(bounds_xml[1][1]), Z=str(bounds_xml[2][1]))
P1.text = "$"
P2.text = "$"

DumpBox = ET.SubElement(Properties, "DumpBox", Name="nf2ff_H_xp", DumpMode="1", DumpType="1", FileType="1")
Primitives = ET.SubElement(DumpBox, "Primitives")
Box = ET.SubElement(Primitives, "Box", Priority="0")
P1 = ET.SubElement(Box, "P1", X=str(bounds_xml[0][1]), Y=str(bounds_xml[1][0]), Z=str(bounds_xml[2][0]))
P2 = ET.SubElement(Box, "P2", X=str(bounds_xml[0][1]), Y=str(bounds_xml[1][1]), Z=str(bounds_xml[2][1]))
P1.text = "$"
P2.text = "$"

DumpBox = ET.SubElement(Properties, "DumpBox", Name="nf2ff_E_yn", DumpMode="1", DumpType="0", FileType="1")
Primitives = ET.SubElement(DumpBox, "Primitives")
Box = ET.SubElement(Primitives, "Box", Priority="0")
P1 = ET.SubElement(Box, "P1", X=str(bounds_xml[0][0]), Y=str(bounds_xml[1][0]), Z=str(bounds_xml[2][0]))
P2 = ET.SubElement(Box, "P2", X=str(bounds_xml[0][1]), Y=str(bounds_xml[1][0]), Z=str(bounds_xml[2][1]))
P1.text = "$"
P2.text = "$"

DumpBox = ET.SubElement(Properties, "DumpBox", Name="nf2ff_H_yn", DumpMode="1", DumpType="1", FileType="1")
Primitives = ET.SubElement(DumpBox, "Primitives")
Box = ET.SubElement(Primitives, "Box", Priority="0")
P1 = ET.SubElement(Box, "P1", X=str(bounds_xml[0][0]), Y=str(bounds_xml[1][0]), Z=str(bounds_xml[2][0]))
P2 = ET.SubElement(Box, "P2", X=str(bounds_xml[0][1]), Y=str(bounds_xml[1][0]), Z=str(bounds_xml[2][1]))
P1.text = "$"
P2.text = "$"

DumpBox = ET.SubElement(Properties, "DumpBox", Name="nf2ff_E_yp", DumpMode="1", DumpType="0", FileType="1")
Primitives = ET.SubElement(DumpBox, "Primitives")
Box = ET.SubElement(Primitives, "Box", Priority="0")
P1 = ET.SubElement(Box, "P1", X=str(bounds_xml[0][0]), Y=str(bounds_xml[1][1]), Z=str(bounds_xml[2][0]))
P2 = ET.SubElement(Box, "P2", X=str(bounds_xml[0][1]), Y=str(bounds_xml[1][1]), Z=str(bounds_xml[2][1]))
P1.text = "$"
P2.text = "$"

DumpBox = ET.SubElement(Properties, "DumpBox", Name="nf2ff_H_yp", DumpMode="1", DumpType="1", FileType="1")
Primitives = ET.SubElement(DumpBox, "Primitives")
Box = ET.SubElement(Primitives, "Box", Priority="0")
P1 = ET.SubElement(Box, "P1", X=str(bounds_xml[0][0]), Y=str(bounds_xml[1][1]), Z=str(bounds_xml[2][0]))
P2 = ET.SubElement(Box, "P2", X=str(bounds_xml[0][1]), Y=str(bounds_xml[1][1]), Z=str(bounds_xml[2][1]))
P1.text = "$"
P2.text = "$"

DumpBox = ET.SubElement(Properties, "DumpBox", Name="nf2ff_E_zn", DumpMode="1", DumpType="0", FileType="1")
Primitives = ET.SubElement(DumpBox, "Primitives")
Box = ET.SubElement(Primitives, "Box", Priority="0")
P1 = ET.SubElement(Box, "P1", X=str(bounds_xml[0][0]), Y=str(bounds_xml[1][0]), Z=str(bounds_xml[2][0]))
P2 = ET.SubElement(Box, "P2", X=str(bounds_xml[0][1]), Y=str(bounds_xml[1][1]), Z=str(bounds_xml[2][0]))
P1.text = "$"
P2.text = "$"

DumpBox = ET.SubElement(Properties, "DumpBox", Name="nf2ff_H_zn", DumpMode="1", DumpType="1", FileType="1")
Primitives = ET.SubElement(DumpBox, "Primitives")
Box = ET.SubElement(Primitives, "Box", Priority="0")
P1 = ET.SubElement(Box, "P1", X=str(bounds_xml[0][0]), Y=str(bounds_xml[1][0]), Z=str(bounds_xml[2][0]))
P2 = ET.SubElement(Box, "P2", X=str(bounds_xml[0][1]), Y=str(bounds_xml[1][1]), Z=str(bounds_xml[2][0]))
P1.text = "$"
P2.text = "$"

DumpBox = ET.SubElement(Properties, "DumpBox", Name="nf2ff_E_zp", DumpMode="1", DumpType="0", FileType="1")
Primitives = ET.SubElement(DumpBox, "Primitives")
Box = ET.SubElement(Primitives, "Box", Priority="0")
P1 = ET.SubElement(Box, "P1", X=str(bounds_xml[0][0]), Y=str(bounds_xml[1][0]), Z=str(bounds_xml[2][1]))
P2 = ET.SubElement(Box, "P2", X=str(bounds_xml[0][1]), Y=str(bounds_xml[1][1]), Z=str(bounds_xml[2][1]))
P1.text = "$"
P2.text = "$"

DumpBox = ET.SubElement(Properties, "DumpBox", Name="nf2ff_H_zp", DumpMode="1", DumpType="1", FileType="1")
Primitives = ET.SubElement(DumpBox, "Primitives")
Box = ET.SubElement(Primitives, "Box", Priority="0")
P1 = ET.SubElement(Box, "P1", X=str(bounds_xml[0][0]), Y=str(bounds_xml[1][0]), Z=str(bounds_xml[2][1]))
P2 = ET.SubElement(Box, "P2", X=str(bounds_xml[0][1]), Y=str(bounds_xml[1][1]), Z=str(bounds_xml[2][1]))
P1.text = "$"
P2.text = "$"

## Mesh
RectilinearGrid = ET.SubElement(ContinuousStructure, "RectilinearGrid", DeltaUnit="0.001", CoordSystem="0")
XLines = ET.SubElement(RectilinearGrid, "XLines").text = ",".join(str(x) for x in mesh[0])
YLines = ET.SubElement(RectilinearGrid, "YLines").text = ",".join(str(y) for y in mesh[1])
ZLines = ET.SubElement(RectilinearGrid, "ZLines").text = ",".join(str(z) for z in mesh[2])



### Write XML to file
tree = ET.ElementTree(openEMS)
tree.write("filename.xml", short_empty_elements=False)

# Prettify output
dom = xml.dom.minidom.parse("filename.xml")
pretty_xml_as_string = dom.toprettyxml(indent="  ")

with open("filename.xml", "w") as xml_file:
	xml_file.write(pretty_xml_as_string)

# Replace header
with open("filename.xml") as xml_file:
	lines = xml_file.readlines()
lines[0] = '<?xml version="1.0" encoding="UTF-8" standalone="yes" ?>\n'
with open("filename.xml", "w") as xml_file:
	xml_file.writelines(lines)

# Clean up empty elements
with open("filename.xml", "r") as xml_in, open("filename_tmp.xml", "w") as xml_out:
	data = xml_in.read()
	data = data.replace("$", "")
	xml_out.write(data)

os.replace("filename_tmp.xml", "filename.xml")
