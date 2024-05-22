# CENG328 - Operating Systems - Auto Compile Scripts

## Description
This repository provides tools to handle homework submissions, process data, and generate necessary outputs for the operating systems course.

It includes two Python scripts and a bash script designed to automate the compilation for the student's submissions.


## Repository Structure
- **archives/**: Directory to place bulk-downloaded zip files.
- **data/**: Directory where the script outputs results.
- **scripts/**: Contains the Python and bash scripts.
- **static/**: Directory for static resources.
- **requirements.txt**: Lists Python dependencies.


## Prerequisites
- Ensure Python is installed on your machine.
- If you are not planning to use the `bulkrunner` script install necessary Python packages from  `requirements.txt`:
  ```bash
  pip install -r requirements.txt
  ```
- If you are planning to use the `bulkrunner` script, make sure that it has the required permissions:
  ```bash
  chmod +x scripts/bulkrunner
  ```

## Usage:

- You can individually run the python scripts:
  ```bash
  python3 scripts/process_submissions.py
  python3 scripts/create_more_data.py
  ```
- Or you can run the `bulkrunner` script:
  ```bash
  ./scripts/bulkrunner
  ``` 
