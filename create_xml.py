import xml.etree.cElementTree as ET
import xml.dom.minidom
import math
import os

#### [ ]: To do
#### [x]: Done

### [ ] Excitation
f_start = 1e9 # Start frequency [Hz]
f_stop = 2e9 # Stop frequency [Hz]


### [ ] Geometry
e_r = 2.2

e_0 = 8.8541878128e-12
k = 1e-3 * 2 * math.pi * 2.45e9 * e_0 * e_r

objects = {
"/home/abc/Desktop/pyapi/Part__Feature001.stl": "PEC",
"/home/abc/Desktop/pyapi/Part__Feature002.stl": [e_r, k],
"/home/abc/Desktop/pyapi/Part__Feature.stl": "PEC"
}

### [x] Mesh
mesh = [
[-97,-90.5,-84,-77.5,-71,-64.5,-58,-51.5,-45,-38.5,-34.446575557,-30.73664388925,-27.0267122215,-16.6389035518,-8.8194517759,-1,7.8194517759,16.6389035518,27.0267122215,30.73664388925,34.446575557,38.5,45,51.5,58,64.5,71,77.5,84,90.5,97],
[-105,-97.5,-90,-82.5,-75,-67.5,-60,-52.5,-45,-37.5,-24.946575557,-17.5267122215,-10.01335611075,-2.5,2.5,10.01335611075,17.5267122215,24.946575557,37.5,45,52.5,60,67.5,75,82.5,90,97.5,105],
[-17.3684266666667,-16.1348733333333,-14.90132,-13.6677666666667,-12.4342133333333,-11.20066,-9.96710666666667,-8.73355333333333,-7.5,-6.26644666666667,-5.03289333333333,-3.5054,-2.41433333333333,-1.635,-1.07833333333333,-0.521666666666667,0.035,0.814333333333333,1.9054,3.43289333333333,5.571384,8.56527093333333,11.7826354666667,15,18.2173645333333,21.4347290666667,24.6520936,27.8694581333333,31.0868226666667,34.3041872,37.5215517333333,40.7389162666667]
]


### [ ] Port
Z = 50 # Port impedance [Ohm]
start = [1,2,3]
end = [1,2,3]
direction = [0,0,1]



### Generate XML
openEMS = ET.Element("openEMS")

## Simulation
FDTD = ET.SubElement(openEMS, "FDTD", NumberOfTimesteps="30000", endCriteria="0.0001", f_max="4000000000")
Excitation = ET.SubElement(FDTD, "Excitation", Type="0", f0="1000000000", fc="3000000000")
Excitation.text = "$"
BoundaryCond = ET.SubElement(FDTD, "BoundaryCond", xmin="PML_8", xmax="PML_8", ymin="PML_8", ymax="PML_8", zmin="PML_8", zmax="PML_8")
BoundaryCond.text = "$"

ContinuousStructure = ET.SubElement(openEMS, "ContinuousStructure", CoordSystem="0")
Properties = ET.SubElement(ContinuousStructure, "Properties")

## CAD
# Patch
Metal = ET.SubElement(Properties, "Metal", Name="patch")
Primitives = ET.SubElement(Metal, "Primitives")
PolyhedronReader = ET.SubElement(Primitives, "PolyhedronReader", Priority="1", FileName="/home/abc/Desktop/pyapi/Part__Feature001.stl", FileType="STL")
PolyhedronReader.text = "$"

# Ground
Metal = ET.SubElement(Properties, "Metal", Name="ground")
Primitives = ET.SubElement(Metal, "Primitives")
PolyhedronReader = ET.SubElement(Primitives, "PolyhedronReader", Priority="1", FileName="/home/abc/Desktop/pyapi/Part__Feature.stl", FileType="STL")
PolyhedronReader.text = "$"

# Substrate
Material = ET.SubElement(Properties, "Material", Name="substrate")
Property = ET.SubElement(Material, "Property", Epsilon="2.2", Kappa="0.00029985919010645")
Property.text = "$"
Primitives = ET.SubElement(Material, "Primitives")
PolyhedronReader = ET.SubElement(Primitives, "PolyhedronReader", Priority="10", FileName="/home/abc/Desktop/pyapi/Part__Feature002.stl", FileType="STL")
PolyhedronReader.text = "$"

## Port
LumpedElement = ET.SubElement(Properties, "LumpedElement", Name="port_resist_1", Direction="2", Caps="1", R="50")
Primitives = ET.SubElement(LumpedElement, "Primitives")
Box = ET.SubElement(Primitives, "Box", Priority="5")
P1 = ET.SubElement(Box, "P1", X="-1", Y="-37.5", Z="-1.6")
P2 = ET.SubElement(Box, "P2", X="-1", Y="-37.5", Z="0")
P1.text = "$"
P2.text = "$"

Excitation = ET.SubElement(Properties, "Excitation", Name="port_excite_1", Type="0", Excite="-0,-0,-1")
Primitives = ET.SubElement(Excitation, "Primitives")
Box = ET.SubElement(Primitives, "Box", Priority="5")
P1 = ET.SubElement(Box, "P1", X="-1", Y="-37.5", Z="-1.6")
P2 = ET.SubElement(Box, "P2", X="-1", Y="-37.5", Z="0")
P1.text = "$"
P2.text = "$"

## Monitors
ProbeBox = ET.SubElement(Properties, "ProbeBox", Name="port_ut1", Type="0", Weight="-1")
Primitives = ET.SubElement(ProbeBox, "Primitives")
Box = ET.SubElement(Primitives, "Box", Priority="5")
P1 = ET.SubElement(Box, "P1", X="-1", Y="-37.5", Z="-1.6")
P2 = ET.SubElement(Box, "P2", X="-1", Y="-37.5", Z="0")
P1.text = "$"
P2.text = "$"

ProbeBox = ET.SubElement(Properties, "ProbeBox", Name="port_it1", Type="1", Weight="1", NormDir="2")
Primitives = ET.SubElement(ProbeBox, "Primitives")
Box = ET.SubElement(Primitives, "Box", Priority="5")
P1 = ET.SubElement(Box, "P1", X="-1", Y="-37.5", Z="-0.8")
P2 = ET.SubElement(Box, "P2", X="-1", Y="-37.5", Z="-0.8")
P1.text = "$"
P2.text = "$"

DumpBox = ET.SubElement(Properties, "DumpBox", Name="Ht_", DumpMode="2", DumpType="1")
Primitives = ET.SubElement(DumpBox, "Primitives")
Box = ET.SubElement(Primitives, "Box", Priority="0")
P1 = ET.SubElement(Box, "P1", X="-59", Y="-40", Z="2.6")
P2 = ET.SubElement(Box, "P2", X="59", Y="40", Z="2.6")
P1.text = "$"
P2.text = "$"

DumpBox = ET.SubElement(Properties, "DumpBox", Name="nf2ff_E_xn", DumpMode="1", DumpType="0", FileType="1")
Primitives = ET.SubElement(DumpBox, "Primitives")
Box = ET.SubElement(Primitives, "Box", Priority="0")
P1 = ET.SubElement(Box, "P1", X="-45", Y="-45", Z="-7.5")
P2 = ET.SubElement(Box, "P2", X="-45", Y="45", Z="7.5")
P1.text = "$"
P2.text = "$"

DumpBox = ET.SubElement(Properties, "DumpBox", Name="nf2ff_H_xn", DumpMode="1", DumpType="1", FileType="1")
Primitives = ET.SubElement(DumpBox, "Primitives")
Box = ET.SubElement(Primitives, "Box", Priority="0")
P1 = ET.SubElement(Box, "P1", X="-45", Y="-45", Z="-7.5")
P2 = ET.SubElement(Box, "P2", X="-45", Y="45", Z="7.5")
P1.text = "$"
P2.text = "$"

DumpBox = ET.SubElement(Properties, "DumpBox", Name="nf2ff_E_xp", DumpMode="1", DumpType="0", FileType="1")
Primitives = ET.SubElement(DumpBox, "Primitives")
Box = ET.SubElement(Primitives, "Box", Priority="0")
P1 = ET.SubElement(Box, "P1", X="45", Y="-45", Z="-7.5")
P2 = ET.SubElement(Box, "P2", X="45", Y="45", Z="7.5")
P1.text = "$"
P2.text = "$"

DumpBox = ET.SubElement(Properties, "DumpBox", Name="nf2ff_H_xp", DumpMode="1", DumpType="1", FileType="1")
Primitives = ET.SubElement(DumpBox, "Primitives")
Box = ET.SubElement(Primitives, "Box", Priority="0")
P1 = ET.SubElement(Box, "P1", X="45", Y="-45", Z="-7.5")
P2 = ET.SubElement(Box, "P2", X="45", Y="45", Z="7.5")
P1.text = "$"
P2.text = "$"

DumpBox = ET.SubElement(Properties, "DumpBox", Name="nf2ff_E_yn", DumpMode="1", DumpType="0", FileType="1")
Primitives = ET.SubElement(DumpBox, "Primitives")
Box = ET.SubElement(Primitives, "Box", Priority="0")
P1 = ET.SubElement(Box, "P1", X="-45", Y="-45", Z="-7.5")
P2 = ET.SubElement(Box, "P2", X="45", Y="-45", Z="7.5")
P1.text = "$"
P2.text = "$"

DumpBox = ET.SubElement(Properties, "DumpBox", Name="nf2ff_H_yn", DumpMode="1", DumpType="1", FileType="1")
Primitives = ET.SubElement(DumpBox, "Primitives")
Box = ET.SubElement(Primitives, "Box", Priority="0")
P1 = ET.SubElement(Box, "P1", X="-45", Y="-45", Z="-7.5")
P2 = ET.SubElement(Box, "P2", X="45", Y="-45", Z="7.5")
P1.text = "$"
P2.text = "$"

DumpBox = ET.SubElement(Properties, "DumpBox", Name="nf2ff_E_yp", DumpMode="1", DumpType="0", FileType="1")
Primitives = ET.SubElement(DumpBox, "Primitives")
Box = ET.SubElement(Primitives, "Box", Priority="0")
P1 = ET.SubElement(Box, "P1", X="-45", Y="45", Z="-7.5")
P2 = ET.SubElement(Box, "P2", X="45", Y="45", Z="7.5")
P1.text = "$"
P2.text = "$"

DumpBox = ET.SubElement(Properties, "DumpBox", Name="nf2ff_H_yp", DumpMode="1", DumpType="1", FileType="1")
Primitives = ET.SubElement(DumpBox, "Primitives")
Box = ET.SubElement(Primitives, "Box", Priority="0")
P1 = ET.SubElement(Box, "P1", X="-45", Y="45", Z="-7.5")
P2 = ET.SubElement(Box, "P2", X="45", Y="45", Z="7.5")
P1.text = "$"
P2.text = "$"

DumpBox = ET.SubElement(Properties, "DumpBox", Name="nf2ff_E_zn", DumpMode="1", DumpType="0", FileType="1")
Primitives = ET.SubElement(DumpBox, "Primitives")
Box = ET.SubElement(Primitives, "Box", Priority="0")
P1 = ET.SubElement(Box, "P1", X="-45", Y="-45", Z="-7.5")
P2 = ET.SubElement(Box, "P2", X="45", Y="45", Z="-7.5")
P1.text = "$"
P2.text = "$"

DumpBox = ET.SubElement(Properties, "DumpBox", Name="nf2ff_H_zn", DumpMode="1", DumpType="1", FileType="1")
Primitives = ET.SubElement(DumpBox, "Primitives")
Box = ET.SubElement(Primitives, "Box", Priority="0")
P1 = ET.SubElement(Box, "P1", X="-45", Y="-45", Z="-7.5")
P2 = ET.SubElement(Box, "P2", X="45", Y="45", Z="-7.5")
P1.text = "$"
P2.text = "$"

DumpBox = ET.SubElement(Properties, "DumpBox", Name="nf2ff_E_zp", DumpMode="1", DumpType="0", FileType="1")
Primitives = ET.SubElement(DumpBox, "Primitives")
Box = ET.SubElement(Primitives, "Box", Priority="0")
P1 = ET.SubElement(Box, "P1", X="-45", Y="-45", Z="7.5")
P2 = ET.SubElement(Box, "P2", X="45", Y="45", Z="7.5")
P1.text = "$"
P2.text = "$"

DumpBox = ET.SubElement(Properties, "DumpBox", Name="nf2ff_H_zp", DumpMode="1", DumpType="1", FileType="1")
Primitives = ET.SubElement(DumpBox, "Primitives")
Box = ET.SubElement(Primitives, "Box", Priority="0")
P1 = ET.SubElement(Box, "P1", X="-45", Y="-45", Z="7.5")
P2 = ET.SubElement(Box, "P2", X="45", Y="45", Z="7.5")
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
