
input_file = 'Data/Input/Stephen/AlmostMaxInhale01/AlmostMaxInhale01.proc.mha'
output_file = 'Data/Output/AlmostMaxInhale01.proc.preblur.mha'

sigma = 1.0

import SimpleITK as sitk

image = sitk.ReadImage(input_file)
for ii in range(3):
    image = sitk.RecursiveGaussian(image, sigma, direction=ii)

sitk.WriteImage(image, output_file)
