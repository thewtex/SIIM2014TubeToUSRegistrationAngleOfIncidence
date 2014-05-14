#!/bin/sh

config=$(dirname $0)/Tuner.json
python=/home/matt/bin/simpleitk-venv/bin/python
tuner="/home/matt/src/TubeTK/Applications/RegisterImageToTubesUsingRigidTransform/Testing/../RegisterImageToTubesUsingRigidTransformTuner.py"

$python $tuner $config
