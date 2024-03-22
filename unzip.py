import zipfile
import os
from pathlib import Path

def create_bld_directory():
    bld_dir = Path("bld")
    if not bld_dir.exists():
        bld_dir.mkdir()

def unzip_file(zip_file, extract_to):
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        zip_ref.extractall(extract_to)

if __name__ == "__main__":
    create_bld_directory()
    zip_file = "src/climate_shocks/data/survey_data.csv.zip"
    extract_to = "bld"
    unzip_file(zip_file, extract_to)