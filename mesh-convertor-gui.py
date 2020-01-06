'''
@author: Hongwei Shao
'''

import sys
import os
import vtk
from PyQt5 import QtCore, QtGui, QtWidgets
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
import mesh.io
import mesh.filters

class MainWindow(QtWidgets.QMainWindow):
    '''
    '''

    def __init__(self, parent=None, flags=QtCore.Qt.WindowFlags()):
        super().__init__(parent=parent, flags=flags)

        self.setWindowTitle('Mesh Convertor')

        self.central_layout = QtWidgets.QGridLayout()

        self.central_frame = QtWidgets.QFrame(self)
        self.central_frame.setMinimumSize(960, 640)
        self.central_frame.setLayout(self.central_layout)
        self.setCentralWidget(self.central_frame)

        self.input_file_label = QtWidgets.QLabel('Input File:', self)
        self.input_file_edit = QtWidgets.QLineEdit('', self)
        self.input_file_button = QtWidgets.QToolButton(self)
        self.input_file_button.setText('...')
        self.input_file_button.clicked.connect(self.selectInputFile)
        self.input_type_label = QtWidgets.QLabel('Input Type:', self)
        self.input_type_combo = QtWidgets.QComboBox(self)
        self.input_type_combo.addItem('.stl')
        self.input_type_combo.addItem('.vtk')
        self.input_type_combo.addItem('.vtp')
        self.input_type_combo.addItem('.ply')
        self.input_type_combo.addItem('.obj')
        self.input_type_combo.addItem('.xyz')
        self.input_type_combo.addItem('.g')

        self.output_folder_label = QtWidgets.QLabel('Output Folder:', self)
        self.output_folder_edit = QtWidgets.QLineEdit('', self)
        self.output_folder_button = QtWidgets.QToolButton(self)
        self.output_folder_button.setText('...')
        self.output_folder_button.clicked.connect(self.selectOutputFolder)
        self.output_type_label = QtWidgets.QLabel('Output Type:', self)
        self.output_type_combo = QtWidgets.QComboBox(self)
        self.output_type_combo.addItem('.stl')
        self.output_type_combo.addItem('.vtk')
        self.output_type_combo.addItem('.vtp')
        self.output_type_combo.addItem('.ply')
        self.output_type_combo.addItem('.obj')
        self.output_type_combo.addItem('.xyz')
        self.output_type_combo.addItem('.g')

        self.decimate_label = QtWidgets.QLabel('Target Reduction:', self)
        self.decimate_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal, self)        
        self.decimate_slider.setTracking(True)
        self.decimate_slider.setRange(0, 100)
        self.decimate_slider.setSliderPosition(0)
        self.decimate_slider.valueChanged.connect(self.sliderValueChanged)
        self.decimate_edit = QtWidgets.QLineEdit('', self)
        self.decimate_edit.setMaximumWidth(80)
        self.decimate_edit.setReadOnly(True)
        self.decimate_edit.setText(str(self.decimate_slider.sliderPosition()/100.0))

        self.convert_button = QtWidgets.QPushButton('Convert', self)
        self.convert_button.clicked.connect(self.convert)

        self.render_widget = QVTKRenderWindowInteractor(self)
        self.render_widget.GetRenderWindow().GetInteractor().Initialize()
        self.interactor_style = vtk.vtkInteractorStyleTrackballCamera()
        self.render_widget.GetRenderWindow().GetInteractor().SetInteractorStyle(
            self.interactor_style)
        self.renderer = vtk.vtkRenderer()
        self.render_widget.GetRenderWindow().AddRenderer(self.renderer)
        self.mapper = vtk.vtkPolyDataMapper()
        self.actor = vtk.vtkActor()
        self.actor.SetMapper(self.mapper)
        self.renderer.AddActor(self.actor)
        
        self.central_layout.setColumnStretch(0, 0)
        self.central_layout.setColumnStretch(1, 1)
        self.central_layout.setColumnStretch(2, 1)
        self.central_layout.setColumnStretch(3, 0)
        self.central_layout.addWidget(self.input_file_label, 0, 0, 1, 1, QtCore.Qt.AlignRight)
        self.central_layout.addWidget(self.input_file_edit, 0, 1, 1, 2)
        self.central_layout.addWidget(self.input_file_button, 0, 3, 1, 1)
        self.central_layout.addWidget(self.input_type_label, 0, 4, 1, 1, QtCore.Qt.AlignRight)
        self.central_layout.addWidget(self.input_type_combo, 0, 5, 1 ,1)
        self.central_layout.addWidget(self.output_folder_label, 1, 0, 1, 1, QtCore.Qt.AlignRight)
        self.central_layout.addWidget(self.output_folder_edit, 1, 1, 1, 2)
        self.central_layout.addWidget(self.output_folder_button, 1, 3, 1, 1)
        self.central_layout.addWidget(self.output_type_label, 1, 4, 1, 1, QtCore.Qt.AlignRight)
        self.central_layout.addWidget(self.output_type_combo, 1, 5, 1 ,1)
        self.central_layout.addWidget(self.decimate_label, 2, 0, 1, 1, QtCore.Qt.AlignRight)
        self.central_layout.addWidget(self.decimate_slider, 2, 1, 1, 1)
        self.central_layout.addWidget(self.decimate_edit, 2, 2, 1 ,1)
        self.central_layout.addWidget(self.convert_button, 2, 4, 1, 2)
        self.central_layout.addWidget(self.render_widget, 3, 0, 1, 6)


    def sliderValueChanged(self, value):
        self.decimate_edit.setText(str(value/100.0))
        

    def selectInputFile(self):
        filters = 'All Files (*.*);;STL Files (*.stl);;VTK Files (*.vtk);;\
            VTP Files (*.vtp);;PLY Files (*.ply);; OBJ Files (*.obj);;\
                XYZ Files (*.xyz);; G Files (*.g)'
        filepath, filter = QtWidgets.QFileDialog.getOpenFileName(
            self, 'Select a file...', '', filters)
        if not os.path.exists(filepath):
            return

        _, extname = os.path.splitext(filepath)
        if extname != '':
            self.input_type_combo.setCurrentText(extname)

        self.input_file_edit.setText(filepath)
        inpolydata = mesh.io.read(
            filepath, self.input_type_combo.currentText())

        self.mapper.SetInputData(inpolydata)
        self.renderer.ResetCamera()

    def selectOutputFolder(self):
        folderpath = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select a folder...')
        if folderpath is not None:
            self.output_folder_edit.setText(folderpath)


    def convert(self):
        infilepath = self.input_file_edit.text()
        if len(infilepath) == 0:
            QtWidgets.QMessageBox.warning(
                self, 'Warning', 'Please select a input file!')
            return
        
        outfolderpath = self.output_folder_edit.text()
        if len(outfolderpath) == 0:
            QtWidgets.QMessageBox.warning(
                self, 'Warning', 'Please select a output folder!')
            return

        infilefolder, infilename = os.path.split(infilepath)
        infileshortname, infileext = os.path.splitext(infilename)
        outfilepath = outfolderpath + os.path.sep + infileshortname +\
            self.output_type_combo.currentText()

        inpolydata = mesh.io.read(
            infilepath, self.input_type_combo.currentText())

        target_reduction = self.decimate_slider.value() / 100.0
        if target_reduction != 0.0:
            mesh.io.write(
                mesh.filters.decimate(inpolydata, target_reduction),
                outfilepath)
        else:
            mesh.io.write(inpolydata, outfilepath)

        QtWidgets.QMessageBox.information(
                self, 'Information', 'Converted successfully!')


class myMainWindow(QtWidgets.QMainWindow):

    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)

        self.frame = QtWidgets.QFrame()

        self.vl = QtWidgets.QVBoxLayout()
        self.vtkWidget = QVTKRenderWindowInteractor(self.frame)
        self.vl.addWidget(self.vtkWidget)

        self.ren = vtk.vtkRenderer()
        self.vtkWidget.GetRenderWindow().AddRenderer(self.ren)
        self.iren = self.vtkWidget.GetRenderWindow().GetInteractor()

        # Create source
        source = vtk.vtkConeSource()
        source.SetCenter(0, 0, 0)
        source.SetRadius(0.1)

        source1 = vtk.vtkSphereSource()
        source1.SetCenter(0, 0, 0)
        source1.SetRadius(0.5)

        # Create a mapper
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(source.GetOutputPort())

        mapper1 = vtk.vtkPolyDataMapper()
        mapper1.SetInputConnection(source1.GetOutputPort())

        # Create an actor
        actor = vtk.vtkActor()
        actor.SetMapper(mapper)

        actor1 = vtk.vtkActor()
        actor1.SetMapper(mapper1)

        self.ren.AddActor(actor)
        self.ren.AddActor(actor1)

        self.ren.ResetCamera()

        self.frame.setLayout(self.vl)
        self.setCentralWidget(self.frame)

        self.iren.Initialize()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())
