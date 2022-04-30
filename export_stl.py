import sys
# Set FreeCAD Python PATH
sys.path = ['/usr/share/freecad/Mod/Web', '/usr/share/freecad/Mod/Raytracing', '/usr/share/freecad/Mod/Material', '/usr/share/freecad/Mod/Show', '/usr/share/freecad/Mod/Start', '/usr/share/freecad/Mod/Spreadsheet', '/usr/share/freecad/Mod/PartDesign', '/usr/share/freecad/Mod/Part', '/usr/share/freecad/Mod/Complete', '/usr/share/freecad/Mod/Path', '/usr/share/freecad/Mod/Image', '/usr/share/freecad/Mod/Import', '/usr/share/freecad/Mod/Robot', '/usr/share/freecad/Mod/Points', '/usr/share/freecad/Mod/Surface', '/usr/share/freecad/Mod/Test', '/usr/share/freecad/Mod/Tux', '/usr/share/freecad/Mod/Sketcher', '/usr/share/freecad/Mod/MeshPart', '/usr/share/freecad/Mod/Fem', '/usr/share/freecad/Mod/Measure', '/usr/share/freecad/Mod/Ship', '/usr/share/freecad/Mod/Drawing', '/usr/share/freecad/Mod/Plot', '/usr/share/freecad/Mod/Idf', '/usr/share/freecad/Mod/ReverseEngineering', '/usr/share/freecad/Mod/OpenSCAD', '/usr/share/freecad/Mod/Draft', '/usr/share/freecad/Mod/TechDraw', '/usr/share/freecad/Mod/Arch', '/usr/share/freecad/Mod/AddonManager', '/usr/share/freecad/Mod/Inspection', '/usr/share/freecad/Mod/Mesh', '/usr/share/freecad/Mod', '/usr/lib/freecad/lib64', '/usr/lib/freecad-python3/lib', '/usr/share/freecad/Ext', '/usr/lib/freecad/bin', '/usr/lib/python38.zip', '/usr/lib/python3.8', '/usr/lib/python3.8/lib-dynload', '/usr/local/lib/python3.8/dist-packages', '/usr/lib/python3/dist-packages', '', '/usr/lib/freecad/Macro']

# Initiate GUI
from PySide2 import QtCore, QtGui, QtWidgets
import FreeCAD, FreeCADGui

class MainWindow(QtWidgets.QMainWindow):
	def showEvent(self, event):
		FreeCADGui.showMainWindow()
		self.setCentralWidget(FreeCADGui.getMainWindow())

app=QtWidgets.QApplication(sys.argv)
mw=MainWindow()
mw.resize(1200,800)
mw.show()

# Update GUI
app.processEvents()
app.processEvents()
app.processEvents()

# Import step file
exec(open('/usr/share/freecad/Mod/Start/StartPage/LoadNew.py').read())
App.setActiveDocument("Unnamed")
App.ActiveDocument=App.getDocument("Unnamed")
Gui.ActiveDocument=Gui.getDocument("Unnamed")
import ImportGui
ImportGui.insert(u"/home/apostolos/Desktop/patch_cenos.step","Unnamed")
Gui.SendMsgToActiveView("ViewFit")

# Export STL
obj_list = []
for obj in FreeCAD.ActiveDocument.Objects:
	if hasattr(obj,"Shape"):
		obj_list.append(obj.Name)

for object in obj_list:
	__objs__=[]
	__objs__.append(FreeCAD.getDocument("Unnamed").getObject(str(object)))

	import Mesh
	Mesh.export(__objs__,u"/home/apostolos/Desktop/"+str(object)+".stl")

	del __objs__
