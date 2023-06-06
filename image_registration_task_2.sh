#!/bin/bash

# Checking if antsRegistration is installed
if ! command -v antsRegistration &>/dev/null; then
  echo "antsRegistration command not found. Please install ANTs (Advanced Normalization Tools) and make sure it is added to the system PATH or running in ANTs installed environment."
  exit 1
fi

# Checking if input files exist
if [ ! -f "Task_2_Files/atlas-T1w.nii.gz" ] || [ ! -f "Task_2_Files/given-T1w.nii.gz" ]; then
  echo "Input files not found. Make sure 'Task_2_Files/atlas-T1w.nii.gz' and 'Task_2_Files/given-T1w.nii.gz' exist."
  exit 1
fi

# Registering the given T1 image to the space of atlas-T1w.nii.gz
antsRegistration --dimensionality 3 --output [output_,Task_2_Files/registered_image.nii.gz, Task_2_Files/affine_matrix.mat] --interpolation LanczosWindowedSinc --winsorize-image-intensities [0.005,0.995] --use-histogram-matching 1 --transform Rigid[0.1] --metric MI[Task_2_Files/atlas-T1w.nii.gz,Task_2_Files/given-T1w.nii.gz,1,32,Regular,0.25] --convergence [1000x500x250x0,1e-6,10] --shrink-factors 8x4x2x1 --smoothing-sigmas 3x2x1x0vox --verbose 1 2>/dev/null

# Some of the other commands that were used
# antsRegistration --dimensionality 3 --output [output_,output.nii.gz, affine_matrix.mat] --interpolation Linear --winsorize-image-intensities [0.005,0.995] --use-histogram-matching 0 --transform Rigid[0.1] --metric MI[Task_2_Files/atlas-T1w.nii.gz,Task_2_Files/given-T1w.nii.gz,1,32,Regular,0.25] --convergence [1000x500x250x0,1e-6,10] --shrink-factors 8x4x2x1 --smoothing-sigmas 3x2x1x0vox --verbose 1 2>/dev/null
# antsRegistration --dimensionality 3 --output [output_,output.nii.gz, affine_matrix.mat] --interpolation LanczosWindowedSinc --winsorize-image-intensities [0.005,0.995] --use-histogram-matching 0 --transform Rigid[0.1] --metric MI[Task_2_Files/atlas-T1w.nii.gz,Task_2_Files/given-T1w.nii.gz,1,32,Regular,0.25] --convergence [1000x500x250x0,1e-6,10] --shrink-factors 8x4x2x1 --smoothing-sigmas 3x2x1x0vox --verbose 1 2>/dev/null
