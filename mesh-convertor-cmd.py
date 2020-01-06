'''
@author: Hongwei Shao
'''

import sys
import os
import argparse
import mesh.io
import mesh.filters

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.description = 'Convert surface mesh file type.'
    parser.add_argument('-i', '--input', help='Input file')
    parser.add_argument('-o', '--output', help='Output file')
    parser.add_argument('-d', '--decimate', help='Target reduction for decimation', type=float)

    args = parser.parse_args()
    if not args.input:
        print('Please specify the input!')
        sys.exit(2)
    if not args.output:
        print('Please specify the output!')
        sys.exit(2)

    in_polydata = mesh.io.read(args.input)
    if in_polydata is None:
        print('Failed to read file \"%s\"' % args.input)

    if args.decimate:
        mesh.io.write(
            mesh.filters.decimate(in_polydata, args.decimate),
            args.output)
    else:
        mesh.io.write(in_polydata, args.output)
