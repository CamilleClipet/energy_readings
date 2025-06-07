from django.core.management import call_command
from django.test import TestCase
from ..models import File, Reading
from pathlib import Path


class ImportFlowCommandTest(TestCase):
    def setUp(self):
        self.example_file_path = Path(__file__).parent.parent.parent.parent / "energy_readings" / "example_file.txt"
        self.example_file2_path = Path(__file__).parent.parent.parent.parent / "energy_readings" / "example_file2.txt"

    def test_single_file_import(self):
        call_command("import_flow", str(self.example_file_path))

        self.assertEqual(File.objects.count(), 1)
        file_obj = File.objects.first()
        self.assertIsNotNone(file_obj)

        reading = Reading.objects.first()
        self.assertIsNotNone(reading)

    def test_multiple_files_import(self):
        call_command("import_flow", str(self.example_file_path), str(self.example_file2_path))

        self.assertEqual(File.objects.count(), 2)
        
        readings = Reading.objects.all()
        self.assertGreater(readings.count(), 0)
        
        distinct_files = set(readings.values_list('file_name', flat=True))
        self.assertEqual(len(distinct_files), 2)
