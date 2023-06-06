# PNL Recruitment Project
This repository contains code for performing Task 1 and Task 2. Please follow the instructions below to run each task individually.

## Prerequisites

- Python 3.x
- NumPy
- NiBabel
- tqdm
- pandas
- dropbox (for Task 1)

## Task 1

Task 1 involves downloading a CSV file from a shared Dropbox folder using the Dropbox API. The downloaded file needs to be anonymized by replacing consent dates with dates earlier than 1925 and generating random offsets for each subject. Additionally, the birth date column should be replaced with the subjects' age in years at the original date of consent. Save the modified CSV file and the offset values in separate files. Finally, utilize the Dropbox API to upload both modified files back to the Dropbox folder.

### Setup

1. Install the required libraries by running the following command:
```bash
pip install numpy nibabel tqdm pandas dropbox
```

2. Obtain a Dropbox access token by creating a Dropbox app [here](https://www.dropbox.com/developers/apps).

3. Update the `ACCESS_TOKEN` variable in the code with your Dropbox access token.


### Usage

1. Run the Python code by executing the script.

2. The script will connect to Dropbox, download the `enroll_data.csv` file, anonymize the data, and upload the anonymized files (`enroll_data_anon_sd.csv` and `enroll_data_offset_sd.csv`) to specified Dropbox folder.

### Additional Information

- The script requires an internet connection to access Dropbox.

- Please ensure that the file paths and directory structure match the instructions provided above.

- Feel free to customize the code and file paths according to your needs.

## Task 2

In Task 2, the goal is to compute volumes of different brain regions by superimposing a given T1w image onto a standard image known as an atlas. The atlas contains integer labels that define region boundaries. The volumes of the brain regions are obtained by counting the labels after superimposition. The workflow involves registering the given T1 image to the atlas space using ANTs, binarizing the atlas for each label, multiplying the registered image with the binary image, and counting the non-zero values to determine the volumes. The FreeSurfer lookup table needs to be processed to extract the brain region names. The results are saved in a CSV file with three columns: label, name, and volume. 

### Prerequisites

- bash (shell scripting)
- ANTs (Advanced Normalization Tools) for image registration
- Python 3.x
- NumPy
- NiBabel
- tqdm
- pandas

### Setup

1. Install the required libraries by running the following command:
```bash 
pip install numpy nibabel tqdm pandas
```

2. Place the necessary files in the appropriate directory:
- The atlas image file should be named `atlas-T1w.nii.gz` and located in the `Task_2_Files` directory.
- The given T1 image file should be named `given-T1w.nii.gz` and located in the `Task_2_Files` directory.
- The image registration script should be named `image_registration_task_2.sh` and located in the root directory.

### Usage

1. Execute the image registration script by running either of the following commands:
```bash
bash image_registration_task_2.sh
```
or
```bash
/bin/bash image_registration_task_2.sh
```
If the script throws any permission error, please use the command below:
```bash
chmod +x image_registration_task_2.sh
```
The provided bash script is used for image registration using the ANTs (Advanced Normalization Tools) software. It first checks if the required command antsRegistration is installed and verifies the existence of the input files. If all prerequisites are met, it proceeds to perform the registration process, aligning the given T1 image with the atlas image. The resulting registered image and the affine transformation matrix are then saved as output files. It's important to note that the subsequent steps of this task are independent of the specific registration method used.

2. After the script execution, the registered image file (`registered_image.nii.gz`) will be created in the `Task_2_Files` directory.

3. Run the Python code `task_2.py` to complete the remaining part of the task.

4. After execution, the results will be saved in a CSV file named `brain_volumes.csv` in the `Task_2_Files` directory.

### Additional Information

- Please ensure that the file paths and directory structure match the instructions provided above.


