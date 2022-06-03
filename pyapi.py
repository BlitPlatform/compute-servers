import xml.etree.cElementTree as ET
import xml.dom.minidom
import os

def generate_xml(sim_parameters, objects, mesh, output="case.xml"):
	### Inputs
	f_min_xml = sim_parameters["f_min"]
	f_max_xml = sim_parameters["f_max"]
	start_xml = sim_parameters["port"][0]
	stop_xml = sim_parameters["port"][1]
	Z_xml = sim_parameters["Z"]
	pml_x_xml = sim_parameters["pml_x"]
	output = str(output)
	output = output.rsplit(".", maxsplit=1)[0]

	# Prepare frequency range for excitation
	f_min_xml = int(f_min_xml)
	f_max_xml = int(f_max_xml)
	f0_xml = int((f_min_xml+f_max_xml)/2)
	fc_xml = int(f_max_xml-f0_xml)

	### Boundaries
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

	# Voltage probe
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
	tree.write(output+".xml", short_empty_elements=False)

	# Prettify output
	dom = xml.dom.minidom.parse(output+".xml")
	pretty_xml_as_string = dom.toprettyxml(indent="  ")

	with open(output+".xml", "w") as xml_file:
		xml_file.write(pretty_xml_as_string)

	# Replace header
	with open(output+".xml") as xml_file:
		lines = xml_file.readlines()
	lines[0] = '<?xml version="1.0" encoding="UTF-8" standalone="yes" ?>\n'
	with open(output+".xml", "w") as xml_file:
		xml_file.writelines(lines)

	# Clean up empty elements
	with open(output+".xml", "r") as xml_in, open(output+"_tmp.xml", "w") as xml_out:
		data = xml_in.read()
		data = data.replace("$", "")
		xml_out.write(data)

	os.replace(output+"_tmp.xml", output+".xml")