import unittest
import csv
from datetime import datetime, timedelta

UPDATED_FILE = 'Task_1_Files/enroll_data_anon_sd.csv'
OFFSET_FILE = 'Task_1_Files/enroll_data_offset_sd.csv'


class MyTestCase(unittest.TestCase):

    def test_date_of_consent(self):
        with open(UPDATED_FILE, 'r') as file:
            reader = csv.reader(file)
            data = list(reader)
        consent_date_index = data[0].index('date of consent')
        for row in data:
            date_of_consent = datetime.strptime(row[consent_date_index], '%Y/%m/%d')
            self.assertLess(date_of_consent.year, 1925, f"Date of consent is not before 1925: {date_of_consent}")

    def test_modified_date_of_consent(self):
        with open(UPDATED_FILE, 'r') as file:
            reader = csv.reader(file)
            data = list(reader)
        consent_date_index = data[0].index('date of consent')
        with open(OFFSET_FILE, 'r') as file:
            reader = csv.reader(file)
            offsets = list(reader)
        for row, offset_row in zip(data, offsets):
            modified_date_of_consent = datetime.strptime(row[consent_date_index], '%Y/%m/%d')
            days_offset = int(offset_row[0])
            original_date_of_consent = modified_date_of_consent + timedelta(days=days_offset)
            self.assertEqual(original_date_of_consent, datetime.strptime(row[consent_date_index], '%m/%d/%Y'),
                             "Modified date of consent and offset do not match")


if __name__ == '__main__':
    unittest.main()
