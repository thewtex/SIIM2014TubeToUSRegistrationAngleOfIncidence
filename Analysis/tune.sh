#!/bin/sh

config=$(dirname $0)/Tuner.json
python=pgpython
tuner="/home/matt/src/TubeTK/Applications/RegisterImageToTubesUsingRigidTransform/Testing/../RegisterImageToTubesUsingRigidTransformTuner.py"

$python $tuner $config
