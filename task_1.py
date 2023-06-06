# Importing required libraries
import dropbox
from dropbox.exceptions import DropboxException
import csv
import random
from datetime import datetime, timedelta
import os

# Dropbox API credentials
ACCESS_TOKEN = 'YOUR_DROPBOX_ACCESS_TOKEN'  # Create one here https://www.dropbox.com/developers/apps

# Defining file paths and names
WORKING_DIRECTORY = './'

DROPBOX_DOWNLOAD_FILE_PATH = '/recruitment_project/enroll_data.csv'
LOCAL_DOWNLOAD_FILE_PATH = WORKING_DIRECTORY + 'Task_1_Files/enroll_data.csv'

DROPBOX_UPLOAD_FILE_PATH = '/recruitment_project/enroll_data_anon_sd.csv'
LOCAL_UPLOAD_FILE_PATH = WORKING_DIRECTORY + 'Task_1_Files/enroll_data_anon_sd.csv'

DROPBOX_OFFSET_FILE_PATH = '/recruitment_project/enroll_data_offset_sd.csv'
LOCAL_UPLOAD_OFFSET_FILE_PATH = WORKING_DIRECTORY + 'Task_1_Files/enroll_data_offset_sd.csv'

OUTPUT_FILENAME = 'enroll_data_anon_sd.csv'
OFFSET_FILENAME = 'enroll_data_offset_sd.csv'


class Task1:
    def __init__(self):
        # Creating Task_1_Files directory if it doesn't exist
        if not os.path.exists(WORKING_DIRECTORY + 'Task_1_Files'):
            os.makedirs(WORKING_DIRECTORY + 'Task_1_Files')

        dbx = self.connect_to_dropbox()
        self.download_file_from_dropbox(dropbox_object=dbx)
        self.anonymize()
        self.upload_file_to_dropbox(dbx, LOCAL_UPLOAD_FILE_PATH, DROPBOX_UPLOAD_FILE_PATH)
        self.upload_file_to_dropbox(dbx, LOCAL_UPLOAD_OFFSET_FILE_PATH, DROPBOX_OFFSET_FILE_PATH)

    # Connecting to Dropbox
    def connect_to_dropbox(self, access_token=ACCESS_TOKEN):
        try:
            # Initialize Dropbox API client
            print('Initializing the connection to dropbox')
            return dropbox.Dropbox(access_token)

        except dropbox.exceptions.AuthError as auth_error:
            print('Error: Dropbox authentication failed.')
            # Handle the authentication error, e.g., notify the user or retry with different credentials

        except dropbox.exceptions.ApiError as api_error:
            print('Error: Dropbox API error occurred.')
            # Handle the API error, e.g., log the error or handle specific error codes

        except dropbox.exceptions.HttpError as http_error:
            print('Error: Dropbox HTTP error occurred.')
            # Handle the HTTP error, e.g., retry the operation or handle specific status codes

        except Exception as e:
            print('Error: An unexpected error occurred.')
            print(str(e))
            # Handle any other unexpected errors

    # Downloading Files from Dropbox
    def download_file_from_dropbox(self, dropbox_object, local_file_path=LOCAL_DOWNLOAD_FILE_PATH,
                                   dropbox_file_path=DROPBOX_DOWNLOAD_FILE_PATH):
        try:
            print(f'Downloading the file...{dropbox_file_path}.')
            dropbox_object.files_download_to_file(local_file_path, dropbox_file_path)
            print(f'File {local_file_path} downloaded successfully.')
            # Handle the validation error, e.g., prompt the user to provide a valid file path
        except dropbox.exceptions.ApiError as e:
            print(f'Error downloading file: {e}')

    # Uploading Files to Dropbox
    def upload_file_to_dropbox(self, dropbox_object, local_file_path, dropbox_file_path):
        try:
            print(f'Uploading the file...{local_file_path}.')
            # Open the file in binary mode
            with open(local_file_path, 'rb') as file:
                # Upload the file to Dropbox
                dropbox_object.files_upload(file.read(), dropbox_file_path)
            print(f'File uploaded successfully at {dropbox_file_path}.')
        except dropbox.exceptions.ApiError as e:
            print(f'Error uploading file: {e}')

    # Anonymizing Date of Consent and replacing Date of Birth with Age
    def anonymize(self, file_path=LOCAL_DOWNLOAD_FILE_PATH):
        # Read the original CSV file
        with open(file_path, 'r') as file:
            reader = csv.reader(file)
            data = list(reader)

        # Get the column index of the date of consent and birthdate columns
        consent_date_index = data[0].index('date of consent')
        birth_date_index = data[0].index('birth date')

        data[0][birth_date_index] = 'age'

        # Generate a random offset for each subject
        random.seed(42)  # Set a fixed seed for reproducibility, change or remove if desired
        offsets = []

        print(f'Anonymizing the file...{file_path}')

        for i, row in enumerate(data[1:]):
            original_date = datetime.strptime(row[consent_date_index], '%m/%d/%Y')

            # Replacing birthdate column with age in years at the original date of consent
            birth_date = datetime.strptime(row[birth_date_index], '%Y-%m-%d')
            age = original_date.year - birth_date.year
            if original_date.month < birth_date.month or (
                    original_date.month == birth_date.month and original_date.day < birth_date.day):
                age -= 1
            row[birth_date_index] = str(age)

            # Modifying the dates of consent making sure the year is earlier than 1925
            min_offset = (original_date - datetime(1925, 1, 1)).days
            offset = random.randint(min_offset, min_offset * 2)
            offsets.append(offset)
            modified_date = original_date - timedelta(days=offsets[i])
            row[consent_date_index] = modified_date.strftime('%m/%d/%Y')

        # Writing the output file
        print(f'Writing {OUTPUT_FILENAME} file.')
        with open(LOCAL_UPLOAD_FILE_PATH, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(data)

        # Writing the offset file
        print(f'Writing {OFFSET_FILENAME} file.')
        with open(LOCAL_UPLOAD_OFFSET_FILE_PATH, 'w', newline='') as offset_file:
            writer = csv.writer(offset_file)
            writer.writerow(['days_offset'])
            writer.writerows([[offset] for offset in offsets])


Task1()
