#!/usr/bin/env pgpython

# Use for center.
input_transform = './Data/Output/AlmostMaxInhale01.Transform.h5'
output_transform = './Data/Input/Stephen/AlmostMaxInhale01/AlmostMaxInhale01.new-transform.h5'

import SimpleITK as sitk
import numpy as np

transform = sitk.ReadTransform(input_transform)
parameters = np.array(transform.GetParameters())
parameters[:3] = 0.1
parameters[3:] = 5.0
transform.SetParameters(parameters)
sitk.WriteTransform(transform, output_transform)

tube_transform = '/home/matt/bin/TubeTK-Clang-RelWithDebInfo/TubeTK-build/bin/TubeTransform'
input_tubes = './Data/Input/Stephen/AlmostMaxInhale01/vessels-aligned-trimmed.tre'
output_tubes = './Data/Input/Stephen/AlmostMaxInhale01/vessels-aligned-trimmed-new.tre'

import subprocess
subprocess.check_call([tube_transform,
    '--transformFile', output_transform,
    input_tubes, output_tubes])
