import os
import time
import csv
import logging
import sys


file_handler = logging.FileHandler(filename='tmp.log')
stdout_handler = logging.StreamHandler(stream=sys.stdout)
handlers = [file_handler, stdout_handler]

logging.basicConfig(
    level=logging.DEBUG, 
    format='[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s - %(message)s',
    handlers=handlers
)

logger = logging.getLogger('mylogger')

# Define the list of folders you want to track
folders_to_track = [
    "PATH HERE"
    # Add more folder paths as needed
]

# Create a dictionary to store the initial modification timestamps for all files
initial_modification_times = {}

# Define the CSV file to store the changes
csv_file_path = "file_changes.csv"

# Define the sleep interval in seconds (adjust as needed)
sleep_interval = 60  # Check every minute

# Create or open the CSV file and write the header
with open(csv_file_path, mode='w', newline='') as csv_file:
    logging.info(f"Opening {csv_file_path}...")
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(["File", "Initial date", "Last modified date"])

def track_files_in_folder(folder_path):
    logging.info(f"Tracking {folder_path}...")
    for root, _, files in os.walk(folder_path):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            try:
                # Get the current modification timestamp
                current_modification_time = time.ctime(os.path.getmtime(file_path))
                # Check if the file has been modified
                if file_path not in initial_modification_times:
                    initial_modification_times[file_path] = current_modification_time
                elif current_modification_time != initial_modification_times[file_path]:
                    
                    logger.info(f"File '{file_path}' was modified. Date: {current_modification_time}")

                    # Write the change to the CSV file
                    with open(csv_file_path, mode='a', newline='') as csv_file:
                        
                        csv_writer = csv.writer(csv_file)
                        csv_writer.writerow([os.path.basename(file_path),
                                             initial_modification_times[file_path],
                                             current_modification_time])
                        logger.info(f"Writing to {csv_file_path}...")

                    # Update the initial modification timestamp
                    initial_modification_times[file_path] = current_modification_time

            except Exception as e:
                logger.error(f"An error occurred while checking '{file_path}': {str(e)}")

while True:
    for folder_path in folders_to_track:
        track_files_in_folder(folder_path)

    # Sleep for the specified interval before checking again
    time.sleep(sleep_interval)
