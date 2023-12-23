# delete.py

import glob
import os

def delete_csv_files(folder_path):
    # Use glob to get a list of all CSV files in the folder
    csv_files = glob.glob(os.path.join(folder_path, '*.csv'))

    # Loop through the list of CSV files and delete each one
    for file in csv_files:
        os.remove(file)
