from datetime import datetime
from .models import File, Reading


def process_flow_file(file_path: str) -> File:
    current_mpan = None
    current_meter_id = None
    current_reading_type = None
    readings_data = []
    
    with open(file_path, 'r') as file:
        lines = file.readlines()
        
        # Process header (first line) and footer (last line)
        header = lines[0].strip()
        footer = lines[-1].strip()
        
        # Create File record
        file_name = file_path.split('/')[-1]
        file_record = File.objects.create(
            file_name=file_name,
            header=header,
            footer=footer
        )

        if len(lines) <= 1:
            raise ValueError("File is empty or incomplete")
        
        # Process data lines
        for line in lines[1:-1]:  # Skip header and footer
            data = line.strip().split('|')
            code = data[0]
            
            if code == '026':
                current_mpan = int(data[1])  # MPAN Core
                validation_status = data[2]
            elif code == '028':
                current_meter_id = data[1]  # Meter Id
                current_reading_type = data[2]  # Reading Type
            elif code == '030':
                # Process register reading
                reading_datetime = datetime.strptime(data[2], '%Y%m%d%H%M%S')
                md_reset_datetime = datetime.strptime(data[4], '%Y%m%d%H%M%S') if data[4] else None
                
                reading = Reading(
                    file_name=file_record,
                    mpan_core=current_mpan,
                    validation_status=validation_status,
                    meter_id=current_meter_id,
                    reading_type=current_reading_type,
                    meter_register_id=data[1],
                    reading_datetime=reading_datetime,
                    register_reading=float(data[3]),
                    md_reset_datetime=md_reset_datetime,
                    nb_md_resets=int(data[5]) if data[5] else 0,
                    meter_reading_flag=data[6] == 'T',
                    reading_method=data[7],
                    meter_reading_reason_code=None,  # Will be updated if code 032 follows
                    meter_reading_status=None  # Will be updated if code 032 follows
                )
                readings_data.append(reading)
            elif code == '032':
                # Should be present if meter_reading_flag is False
                if readings_data:
                    readings_data[-1].meter_reading_reason_code = data[1]
                    readings_data[-1].meter_reading_status = data[2] == 'V'
        
        Reading.objects.bulk_create(readings_data)
        
        return file_record 