'''
@author: Hongwei Shao
'''

import os
import vtk


def read(filepath, filetype=None):
    if not os.path.exists(filepath):
        return None

    if filetype is None:
        _, filetype = os.path.splitext(filepath)

    reader = None
    if filetype == '.stl':
        reader = vtk.vtkSTLReader()
    elif filetype == '.vtk':
        reader = vtk.vtkPolyDataReader()
    elif filetype == '.vtp':
        reader = vtk.vtkXMLPolyDataReader()
    elif filetype == '.ply':
        reader = vtk.vtkPLYReader()
    elif filetype == '.obj':
        reader = vtk.vtkOBJReader()
    elif filetype == '.xyz':
        reader = vtk.vtkSimplePointsReader()
    elif filetype == '.g':
        reader = vtk.vtkBYUReader()
    else:
        return None

    reader.SetFileName(filepath)
    reader.Update()

    return reader.GetOutput()


def write(polydata, filepath, filetype=None):
    if polydata is None or filepath == '':
        return

    if filetype is None:
        _, filetype = os.path.splitext(filepath)
        
    writer = None
    if filetype == '.stl':
        writer = vtk.vtkSTLWriter()
    elif filetype == '.vtk':
        writer = vtk.vtkPolyDataWriter()
    elif filetype == '.vtp':
        writer = vtk.vtkXMLPolyDataWriter()
    elif filetype == '.ply':
        writer = vtk.vtkPLYWriter()
    elif filetype == '.obj':
        writer = vtk.vtkOBJWriter()
    elif filetype == '.xyz':
        writer = vtk.vtkSimplePointsWriter()
    elif filetype == '.g':
        writer = vtk.vtkBYUWriter()
    else:
        return

    writer.SetInputData(polydata)
    writer.SetFileName(filepath)
    writer.Update()
