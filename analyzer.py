import argparse # Importing argparse for command-line argument parsing
import os # Importing os for file operations
import psutil # Importing psutil for system and process utilities (CPU and memory usage statisitcs)
from datetime import datetime # Importing datetime for timestamping

from google.cloud import storage # Importing Google Cloud Storage client library

# ... (other functions) ...
  
def analyze_file(file_path):
    if os.path.exists(file_path):
        try:
            file_stats = os.stat(file_path)
            print(f"File: {file_path}")
            print(f"Size: {file_stats.st_size} bytes")
            print(f"Last Modified: {datetime.fromtimestamp(file_stats.st_mtime)}")
            print(f"Permissions: {oct(file_stats.st_mode)}")
        except Exception as e:
            print(f"Error analyzing file: {e}")
    else:
        print(f"File not found: {file_path}")

def analyze_system():
    try:
        cpu_percent = psutil.cpu_percent(interval=1)
        memory_percent = psutil.virtual_memory().percent
        print("System Information:")
        print(f"CPU Usage: {cpu_percent}%")
        print(f"Memory Usage: {memory_percent}%")
    except Exception as e:
        print(f"Error analyzing system: {e}")
    
def list_gcs_bucket(bucket_name):
    try:
        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        blobs = bucket.list_blobs()
        for blob in blobs:
            print(blob.name)
    except Exception as e:
        print(f"Error listing GCS bucket: {e}")

def download_gcs_file(bucket_name, file_name, local_path):
    try:
        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(file_name)
        blob.download_to_filename(local_path)
        print(f"Downloaded {file_name} to {local_path}")
    except Exception as e:
        print(f"Error downloading GCS file: {e}")
  
def main():
    parser = argparse.ArgumentParser(description="System and file analyzer")
    parser.add_argument("-f", "--file", help="Analyze a file.")
    parser.add_argument("-s", "--system", action="store_true", help="Display system info.")
    parser.add_argument("--list-gcs", help="List files in a GCS bucket.")
    parser.add_argument("--download-gcs", nargs=3, help="Download a file from GCS. Usage: --download-gcs <bucket_name> <file_name> <local_path>")
    args = parser.parse_args()
 
  # Handle arguments
    if args.file:
        analyze_file(args.file)
    elif args.system:
        analyze_system()
    elif args.list_gcs:
        list_gcs_bucket(args.list_gcs)
    elif args.download_gcs:
        bucket_name, file_name, local_path = args.download_gcs
        download_gcs_file(bucket_name, file_name, local_path)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()