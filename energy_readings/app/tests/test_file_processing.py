import os
import pytest
from django.test import TestCase
from energy_readings.app.models import File, Readings
from energy_readings.app.utils import process_flow_file


class TestFlowFileProcessing(TestCase):
    def setUp(self):
        self.test_file_path = 'app/tests/test_flow.txt'

    def test_file_import(self):
        file_record = process_flow_file(self.test_file_path)
        
        # Check file record
        self.assertEqual(file_record.file_name, 'test_flow.txt')
        self.assertTrue(file_record.header.startswith('ZHV|'))
        self.assertTrue(file_record.footer.startswith('ZPT|'))
        
        # Check readings
        readings = Readings.objects.filter(file_name=file_record)
        self.assertEqual(readings.count(), 2)
        
        # Check first reading details
        first_reading = readings.order_by('reading_datetime').first()
        self.assertEqual(first_reading.mpan_core, 1200023305967)
        self.assertEqual(first_reading.meter_id, 'F75A 00802')
        self.assertEqual(first_reading.reading_type, 'D')
        self.assertEqual(first_reading.meter_register_id, 'S')
        self.assertEqual(first_reading.register_reading, 56311)
        self.assertTrue(first_reading.meter_reading_flag)
        self.assertEqual(first_reading.reading_method, 'N')
        self.assertEqual(first_reading.meter_reading_reason_code, None)
        self.assertEqual(first_reading.meter_reading_status, None)
    

    def test_invalid_file_format(self):
        with open('invalid_test.txt', 'w') as f:
            f.write('empty|0000475656| |V|')
        
        with pytest.raises(ValueError):
            process_flow_file('invalid_test.txt')
        
        os.remove('invalid_test.txt')
    

    def test_missing_file(self):
        with pytest.raises(FileNotFoundError):
            process_flow_file('nonexistent_file.txt')
