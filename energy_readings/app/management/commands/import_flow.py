from django.core.management.base import BaseCommand
from energy_readings.app.utils import process_flow_file


class Command(BaseCommand):
    help = "Import electricity flow file"

    def add_arguments(self, parser):
        parser.add_argument("file_path", type=str, help="Path to the flow file")

    def handle(self, *args, **options) -> None:
        file_path = options["file_path"]
        try:
            file_record = process_flow_file(file_path)
            self.stdout.write(
                self.style.SUCCESS(f"Successfully imported file {file_record.file_name}")
            )
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error importing file: {str(e)}"))
