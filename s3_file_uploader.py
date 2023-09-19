from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import boto3
import time
import os


S3_BUCKET_NAME = 'unet-results-storage'
S3_PREFIX = ''
s3 = boto3.client('s3')


def upload_to_s3(filepath):
    filename = os.path.basename(filepath)
    try:
        s3.upload_file(filepath, S3_BUCKET_NAME, f'{S3_PREFIX}{filename}')
        print(f'Uploaded {filename} to S3 bucket {S3_BUCKET_NAME}')
        delete_file(filepath)
    except Exception as e:
        print(f'Error uploading {filename} to S3: {str(e)}')


def on_created(event):
    # Triggered when a new file is created in the monitored folder
    filepath = event.src_path
    upload_to_s3(filepath)


def delete_file(file_path):
    try:
        os.remove(file_path)
        print(f'Successfully deleted file: {file_path}')
    except OSError as e:
        print(f'Error: {e.strerror}')

if __name__ == "__main__":
    # Set the folder to monitor
    folder_to_monitor = './results'

    # Initialize file system event handler and observer
    event_handler = FileSystemEventHandler()
    event_handler.on_created = on_created

    observer = Observer()
    observer.schedule(event_handler, path=folder_to_monitor, recursive=False)

    print(f"Monitoring folder: {folder_to_monitor}")
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

