'''
@author: Hongwei Shao
'''

import os
import vtk


def triangulate(polydata):
    if polydata is None:
        return None

    triangle_filter = vtk.vtkTriangleFilter()
    triangle_filter.SetInputData(polydata)
    triangle_filter.SetPassVerts(0)
    triangle_filter.SetPassLines(0)
    triangle_filter.Update()

    return triangle_filter.GetOutput()


def decimate(polydata, target_reduction):
    if polydata is None:
        print('Input polydata is none!')
        return None

    if target_reduction < 0.0:
        target_reduction = 0.0
    if target_reduction > 1.0:
        target_reduction = 1.0

    decimation = vtk.vtkQuadricDecimation()
    decimation.SetInputData(polydata)
    decimation.SetAttributeErrorMetric(0)
    decimation.SetTargetReduction(target_reduction)
    decimation.Update()

    return decimation.GetOutput()
