#!/usr/bin/env pgpython

# Use for center.
base_transform_file = './Data/Output/AlmostMaxInhale01.Transform.h5'
tmp_transform_file = '/tmp/MonteCarlo.transform.h5'
output_transform_file = '/tmp/MonteCarlo.result.transform.h5'
output_dir = './Data/Output/MonteCarlo'
base_parameters_file = './Analysis/Tuner.json'
tmp_parameters_file = '/tmp/MonteCarlo.json'
registration_exe = '/home/matt/bin/TubeTK-Clang-RelWithDebInfo/TubeTK-build/bin/RegisterImageToTubesUsingRigidTransform'
tube_transform_exe = '/home/matt/bin/TubeTK-Clang-RelWithDebInfo/TubeTK-build/bin/TubeTransform'
input_tubes_file = './Data/Input/Stephen/AlmostMaxInhale01/vessels-aligned-trimmed.tre'
tmp_tubes_file = '/tmp/MonteCarlo.tre'

angle_min_max = 0.1
translation_min_max = 3.0
n_experiments = 100
iterations_space = [4, 8, 12]
fractional_importance_space = [0.0, 0.5, 0.8]

import json
import os
import subprocess
import numpy as np
import SimpleITK as sitk

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

with open(base_parameters_file, 'r') as fp:
    base_parameters = json.load(fp)

io_params = base_parameters['ParameterGroups'][0]['Parameters']
input_volume = io_params[0]['Value']

base_transform = sitk.ReadTransform(base_transform_file)

def monte_carlo(fractional_importance, iterations):
    results = np.recarray((n_experiments,), dtype=[('AngleError', float),
        ('TranslationError', float)])

    for ii in range(n_experiments):
        sample = np.random.random_sample(6)
        angles = sample[:3] * 2 * angle_min_max - angle_min_max
        translations = sample[3:] * 2 * translation_min_max - translation_min_max

        new_transform = sitk.Transform(base_transform)
        new_transform.SetParameters(np.concatenate((angles, translations)))
        sitk.WriteTransform(new_transform, tmp_transform_file)

        subprocess.check_call([tube_transform_exe,
            '--transformFile', tmp_transform_file,
            input_tubes_file, tmp_tubes_file])

        new_parameters = base_parameters
        new_parameters['AngleOfIncidenceWeightFunction']['FractionalImportance'] \
            = fractional_importance
        new_parameters['GradientDescentOptimizer']['NumberOfIterations'] = iterations
        with open(tmp_parameters_file, 'w') as fp:
            json.dump(new_parameters, fp)

        subprocess.check_call([registration_exe,
                              '--parameterstorestore', tmp_parameters_file,
                              input_volume,
                              tmp_tubes_file,
                              output_transform_file])

        output_transform = sitk.ReadTransform(output_transform_file)
        output_parameters = output_transform.GetParameters()
        expected = -1 * np.array(new_transform.GetParameters())
        result = np.array(output_transform.GetParameters())
        angle_error = np.mean(np.abs(expected[:3] - result[:3]))
        results[ii]['AngleError'] = angle_error
        translation_error = np.mean(np.abs(expected[3:] - result[3:]))
        results[ii]['TranslationError'] = translation_error

    analysis_name = 'alpha = ' + str(fractional_importance)
    analysis_name += ', Iterations = ' + str(iterations)
    output_path = os.path.join(output_dir, analysis_name) + '.npy'
    np.save(output_path, results)

for fractional_importance in fractional_importance_space:
    for iterations in iterations_space:
        monte_carlo(fractional_importance, iterations)

