# Energy Readings Project

My (Camille Clipet) submission to the Octopus Energy test.
A Django application for processing and storing electricity meter readings.

## Setup

1. Clone the repository:
```sh
git clone https://github.com/CamilleClipet/energy_readings
cd energy_readings
```

2. Create a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure PostgreSQL:
```bash
# Start PostgreSQL service if not already running
brew services start postgresql@14  # Or your installed PostgreSQL version

# Create the database
createdb energy_readings
```

5. Run migrations:
```bash
python manage.py migrate
```

## Run the tests

To run the tests:
```bash
cd energy_readings
pytest app/tests
```

## Import files
You can use the example file provided. In the root directory, run:
```bash
python3 manage.py import_flow energy_readings/example_file.txt
# you can also import a file external to this directory, just use the absolute path
python3 manage.py import_flow /Users/camilleclipet/Documents/example_file2.txt
```

## Use the admin view
First, create an admin superuser: at the root of the project, run:
```bash
python3 manage.py createsuperuser
# and follow the instructions
```
Then navigate to http://127.0.0.1:8000/admin/

You should be able to see the tables filled with the file you imported.

Try the search: you can search for a MPAN or a meter id (serial number). The search for serial numbers is space-insensitive.

## run the linting and formatting tools
```bash
black . && flake8 . && mypy .
```

## Project structure

- `energy_readings/` - Main project directory
  - `app/` - Application code
    - `management/commands/` - Where to find the command to import files
    - `models.py` - Database models
    - `utils.py` - Utility functions for data processing
    - `tests` - Tests folder