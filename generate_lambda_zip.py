### Customize this to your liking
pipLibraries = ['requests']
outputFilename = "lambda.zip"
pythonCodeLocation = "python"
pipTempLocation = "tmp"

### Script imports and utils below ###

import os
from os.path import basename
import sys
import subprocess
from zipfile import ZipFile

class cd:
    """Context manager for changing the current working directory"""
    def __init__(self, newPath):
        self.newPath = os.path.expanduser(newPath)
    def __enter__(self):
        self.savedPath = os.getcwd()
        os.chdir(self.newPath)
    def __exit__(self, etype, value, traceback):
        os.chdir(self.savedPath)

def zip_folders(folders, filename):
    """Function for creating a zipfile manager for changing the current working directory"""
    output_file = os.path.join(os.getcwd(),filename)
    with ZipFile(output_file, 'w') as zipObj:
        for folder in folders:
            print("Zipping " + folder + " to " + output_file)
            with cd(folder):
                for folderName, subfolders, filenames in os.walk("."):
                    for filename in filenames:  
                        filePath = os.path.join(folderName, filename)
                        zipObj.write(filePath, filePath)


### SCRIPT STARTS HERE ###
print("===\n= Installing libraries to " + pipTempLocation + "\n===\n")

# Install libraries to tmp
pip = [sys.executable,'-m','pip', 'install', '--target', pipTempLocation]
args = pip + pipLibraries
subprocess.check_call(args)

print("\n===\n= Generating Final Zip file..\n===\n")

zip_folders([pythonCodeLocation,pipTempLocation], outputFilename)