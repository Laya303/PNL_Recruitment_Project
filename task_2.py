# Importing required libraries
import numpy as np
import nibabel as nib
from tqdm import tqdm
import pandas as pd


class Task2:
    def __init__(self):
        # Loading the registered image and the atlas
        registered_image = nib.load("Task_2_Files/registered_image.nii.gz").get_fdata()
        atlas_label_image = nib.load("Task_2_Files/atlas-integer-labels.nii.gz").get_fdata()

        # Getting the unique labels from the atlas
        labels = np.unique(atlas_label_image).astype(int)

        # Creating a dictionary to store the volumes
        volumes = {}

        # Iterating over the labels
        for label in tqdm(labels):
            # Binarizing the atlas for each integer label
            binary_image = np.zeros_like(atlas_label_image)
            binary_image[atlas_label_image == label] = 1

            # Multiplying the registered image with the binary image
            masked_image = registered_image * binary_image

            # Computing the number of non-zeros in the resultant image
            volume = np.count_nonzero(masked_image)

            # Store the volume in the dictionary
            volumes[label] = volume

        # Parsing the lookup table into a dictionary
        label_names = {}
        with open('Task_2_Files/FsTutorial_AnatomicalROI_FreeSurferColorLUT.txt', 'r') as f:
            lines = f.readlines()[3:]  # Skipping the header lines
            for line in lines:
                parts = line.strip().split()
                if len(parts) >= 5:
                    try:
                        label = int(parts[0])
                        name = ' '.join(parts[1:-4])
                        label_names[label] = name
                    except ValueError:
                        continue

        # Extracting the brain region names from the lookup table
        region_names = [label_names.get(label, 'Unknown') for label in volumes.keys()]

        # Creating a DataFrame to store the results
        results_df = pd.DataFrame(
            {'label': list(volumes.keys()), 'name': region_names, 'volume': list(volumes.values())})

        # Saving the results to a CSV file
        results_df.to_csv('Task_2_Files/brain_volumes.csv', index=False, sep='\t')

        # Printing the results
        print(results_df)


Task2()
