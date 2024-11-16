import os
import time
import shutil
import logging
import sys
from pathlib import Path

# Setup logging to log both to a file and console
def setup_logging(log_file):
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler(sys.stdout)
        ]
    )

# Sync the source folder with the replica folder
def sync_folders(source, replica):
    # Ensure replica folder exists
    if not os.path.exists(replica):
        os.makedirs(replica)
        logging.info(f"Replica folder created: {replica}")

    # Get list of files and directories in source
    source_files = set(os.listdir(source))
    replica_files = set(os.listdir(replica))

    # Copy new or updated files from source to replica
    for item in source_files:
        source_path = os.path.join(source, item)
        replica_path = os.path.join(replica, item)

        if os.path.isdir(source_path):
            # Recursively sync subdirectories
            sync_folders(source_path, replica_path)
        else:
            if item not in replica_files or os.path.getmtime(source_path) > os.path.getmtime(replica_path):
                shutil.copy2(source_path, replica_path)
                logging.info(f"File copied: {source_path} -> {replica_path}")

    # Remove files from replica that no longer exist in source
    for item in replica_files:
        replica_path = os.path.join(replica, item)
        if item not in source_files:
            if os.path.isdir(replica_path):
                shutil.rmtree(replica_path)
                logging.info(f"Directory removed: {replica_path}")
            else:
                os.remove(replica_path)
                logging.info(f"File removed: {replica_path}")

# Main function to handle command-line arguments and synchronization
def main():
    if len(sys.argv) != 4:
        print("Usage: python sync.py <source_folder> <log_file_path> <sync_interval_seconds>")
        sys.exit(1)

    # Get command line arguments
    source_folder = sys.argv[1]
    log_file_path = sys.argv[2]
    try:
        sync_interval = int(sys.argv[3])
    except ValueError:
        print("Sync interval must be an integer.")
        sys.exit(1)

    # Ensure the source folder exists
    if not os.path.exists(source_folder):
        print(f"Error: Source folder '{source_folder}' does not exist.")
        sys.exit(1)

    # Determine the replica folder path (script directory)
    script_dir = os.path.dirname(os.path.realpath(__file__))
    replica_folder = os.path.join(script_dir, "replica")

    # Setup logging
    setup_logging(log_file_path)

    logging.info(f"Starting synchronization from {source_folder} to {replica_folder} every {sync_interval} seconds.")

    # Periodic synchronization
    try:
        while True:
            sync_folders(source_folder, replica_folder)
            time.sleep(sync_interval)
    except KeyboardInterrupt:
        logging.info("Synchronization stopped by user.")

if __name__ == "__main__":
    main()
