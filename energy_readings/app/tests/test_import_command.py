from django.core.management import call_command
from django.test import TestCase
from ..models import File, Reading
from pathlib import Path


class ImportFlowCommandTest(TestCase):
    def setUp(self):
        # Use the existing example file
        self.example_file_path = Path(__file__).parent.parent.parent.parent / "energy_readings" / "example_file.txt"

    def test_successful_import(self):
        call_command("import_flow", str(self.example_file_path))

        self.assertEqual(File.objects.count(), 1)
        
        file_obj = File.objects.first()
        self.assertIsNotNone(file_obj)

        reading = Reading.objects.first()
        self.assertIsNotNone(reading)
