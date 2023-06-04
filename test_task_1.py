import csv
import unittest
from datetime import datetime, timedelta

UPDATED_FILE = 'Task_1_Files/enroll_data_anon_sd.csv'
OFFSET_FILE = 'Task_1_Files/enroll_data_offset_sd.csv'
ORIGINAL_FILE = 'Task_1_Files/enroll_data.csv'


class Task1TestCase(unittest.TestCase):

    # Testing if the modified date of consent is earlier than 1925
    def test_date_of_consent_before_1925(self):
        with open(UPDATED_FILE, 'r') as file:
            reader = csv.reader(file)
            data = list(reader)
        consent_date_index = data[0].index('date of consent')
        for row in data[1:]:
            date_of_consent = datetime.strptime(row[consent_date_index], '%m/%d/%Y')
            self.assertLess(date_of_consent.year, 1925, f'Date of consent is not before 1925: {date_of_consent}')

    # Testing if the original date of consent is the sum of modified date of consent and offset days
    def test_original_date_of_consent_after_offset(self):
        with open(UPDATED_FILE, 'r') as updated_file:
            reader = csv.reader(updated_file)
            modified_data = list(reader)
        modified_consent_date_index = modified_data[0].index('date of consent')

        with open(OFFSET_FILE, 'r') as offset_file:
            reader = csv.reader(offset_file)
            offsets = list(reader)

        with open(ORIGINAL_FILE, 'r') as original_file:
            reader = csv.reader(original_file)
            original_data = list(reader)
        original_consent_date_index = original_data[0].index('date of consent')

        for modified_row, offset_row, original_row in zip(modified_data[1:], offsets[1:], original_data[1:]):
            modified_date_of_consent = datetime.strptime(modified_row[modified_consent_date_index], '%m/%d/%Y')
            days_offset = int(offset_row[0])
            original_date_of_consent = datetime.strptime(original_row[original_consent_date_index], '%m/%d/%Y')
            original_date_from_task = modified_date_of_consent + timedelta(days=days_offset)
            self.assertEqual(original_date_from_task, original_date_of_consent,
                             'Original date of consent does not match when modified date is added to the offset.')


if __name__ == '__main__':
    unittest.main()
