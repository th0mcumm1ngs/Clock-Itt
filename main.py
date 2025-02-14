import subprocess
import os
from datetime import datetime
import exifread

def get_file_modification_date(path):
    """Retrieves the modification date of a file."""
    return datetime.fromtimestamp(os.path.getmtime(path))

def get_exif_capture_date(path):
    """Returns the capture date of an image from its EXIF data as a datetime object."""
    try:
        with open(path, 'rb') as img_file:
            tags = exifread.process_file(img_file)
            if 'EXIF DateTimeOriginal' in tags:
                return datetime.strptime(str(tags.get('EXIF DateTimeOriginal')), '%Y:%m:%d %H:%M:%S')
            print(f"No EXIF DateTimeOriginal tag found in {path}.")
            return None
    except (FileNotFoundError, IOError) as e:
        print(f"Error reading EXIF data from {path}: {e}")
        return None

def set_file_creation_date(path, date):
    """Sets the creation date of a file."""
    try:
        formatted_date = date.strftime('%m/%d/%Y %H:%M:%S')
        subprocess.run(['SetFile', '-d', formatted_date, path], check=True)
        print(f"Creation date of {path} set to {formatted_date}.")
    except subprocess.CalledProcessError as e:
        print(f"Error setting creation date for {path}: {e}")
    except ValueError as e:
        print(f"Error formatting date for {path}: {e}")

def set_file_modification_date(path, date):
    """Sets the modification date of a file."""
    try:
        formatted_date = date.strftime('%m/%d/%Y %H:%M:%S')
        subprocess.run(['SetFile', '-m', formatted_date, path], check=True)
        print(f"Modification date of {path} set to {formatted_date}.")
    except subprocess.CalledProcessError as e:
        print(f"Error setting modification date for {path}: {e}")
    except ValueError as e:
        print(f"Error formatting date for {path}: {e}")

def verify_sensible_date(modification_date, exif_date):
    """Verifies that the modification date is sensible compared to the EXIF date. i.e. the modification date is not earlier than the EXIF date, which will become the new creation date."""
    if modification_date < exif_date:
        print(f"Modification date {modification_date} is earlier than EXIF date {exif_date}.")
        return False
    return True

def update_image_creation_date(path):
    """Updates the creation date of an image file based on its EXIF data."""
    exif_date = get_exif_capture_date(path)
    if exif_date:
        if not verify_sensible_date(get_file_modification_date(path), exif_date):
            set_file_modification_date(path, exif_date)
        set_file_creation_date(path, exif_date)

if __name__ == '__main__':
    file_path = input("Enter the path to the image file: ")
    update_image_creation_date(file_path)
