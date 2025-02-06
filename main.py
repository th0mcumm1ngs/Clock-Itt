import subprocess
from datetime import datetime
import exifread

def get_exif_capture_date(image_path):
    try:
        with open(image_path, 'rb') as img_file:
            tags = exifread.process_file(img_file)
            if 'EXIF DateTimeOriginal' in tags:
                return str(tags.get('EXIF DateTimeOriginal'))
            else:
                print(f"No EXIF DateTimeOriginal tag found in {image_path}.")
                return None
    except (FileNotFoundError, IOError) as e:
        print(f"Error reading EXIF data from {image_path}: {e}")
        return None

def exif_date_to_timestamp(exif_date):
    try:
        dt = datetime.strptime(exif_date, '%Y:%m:%d %H:%M:%S')
        return dt.timestamp()
    except ValueError as e:
        print(f"Error parsing date {exif_date}: {e}")
        return None

def set_file_creation_date(path, timestamp):
    try:
        dt = datetime.fromtimestamp(timestamp)
        formatted_date = dt.strftime('%m/%d/%Y %H:%M:%S')
        subprocess.run(['SetFile', '-d', formatted_date, path], check=True)
        print(f"Creation date of {path} set to {formatted_date}.")
    except subprocess.CalledProcessError as e:
        print(f"Error setting creation date for {path}: {e}")
    except ValueError as e:
        print(f"Error formatting date for {path}: {e}")

def update_image_creation_date(image_path):
    exif_date = get_exif_capture_date(image_path)
    if exif_date:
        timestamp = exif_date_to_timestamp(exif_date)
        if timestamp:
            set_file_creation_date(image_path, timestamp)

if __name__ == '__main__':
    file_path = input("Enter the path to the image file: ")
    update_image_creation_date(file_path)
