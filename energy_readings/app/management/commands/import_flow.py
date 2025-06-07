from django.core.management.base import BaseCommand
from energy_readings.app.utils import process_flow_file


class Command(BaseCommand):
    help = "Import one or more electricity flow files. Accepts several file paths separated by a space."

    def add_arguments(self, parser):
        parser.add_argument(
            "file_paths",
            nargs="+",
            type=str,
            help="Paths to the flow files"
        )

    def handle(self, *args, **options) -> None:
        file_paths = options["file_paths"]
        success_count = 0
        error_count = 0
        
        for file_path in file_paths:
            try:
                file_record = process_flow_file(file_path)
                self.stdout.write(
                    self.style.SUCCESS(f"Successfully imported file {file_record.file_name}")
                )
                success_count += 1
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f"Error importing file {file_path}: {str(e)}")
                )
                error_count += 1
        
        total = len(file_paths)
        self.stdout.write(
            self.style.SUCCESS(
                f"\nImport complete: {success_count} successful, {error_count} failed out of {total} files"
            )
        )
