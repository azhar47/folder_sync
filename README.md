A simple Python script that synchronizes a source folder with a replica folder, ensuring the replica matches the source. It performs periodic synchronization by copying new or updated files and deleting outdated ones.


To run in CMD:

python sync.py "<source_folder_path>" "<log_file_path>" <sync_interval_seconds>

Note: 
<source_folder_path>: Provide the path to the folder you want to copy files from.

<log_file_path>: Provide the path where the log file should be saved, including the log file's name.

<sync_interval_seconds>: Specify the time interval (in seconds) between each sync operation.

For an example :
python sync.py "C:\Users\CopyFolder" "C:\Users\Log\log.text" 10

In this example:
Files from the folder "C:\Users\CopyFolder" will be synced.
Logs will be saved to "C:\Users\Log\log.txt".
The script will sync every 10 seconds.
