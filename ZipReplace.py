''' 
#####################################################################
TOPIC PYTHON OBJECT ORIENTED - ALL ACTION OBJECTS - MANAGERS - PART 1
#####################################################################
A program that does a find and replace action for text files stored in a compressed ZIP file. 
We'll need objects to represent the ZIP file and each individual text file 
(luckily, we don't have to write these classes, they're available in the Python standard library). 
The manager object will be responsible for ensuring three steps occur in order:
1. Unzipping the compressed file.
2. Performing the find and replace action.
3. Zipping up the new files

The class is initialized with the .zip filename and search and replace strings. 
We create a temporary directory to store the unzipped files in, so that the folder stays clean. 
The Python 3.4 pathlib library helps out with file and directory manipulation.

There are several advantages to separating the three steps:
1.Readability: The code for each step is in a self-contained unit that is easy to read and understand. The method names describe what the method does, and less additional documentation is required to understand what is going on.
2.Extensibility: If a subclass wanted to use compressed TAR files instead of ZIP files, it could override the zip and unzip methods without having to duplicate the find_replace method.
3.Partitioning: An external class could create an instance of this class and call the find_replace method directly on some folder without having to zip the content.
'''

import sys
import shutil
import zipfile
from pathlib import Path

class ZipReplace:
    def __init__(self, filename, search_string, replace_string):
        self.filename = filename
        self.search_string = search_string
        self.replace_string = replace_string
        # Define temp dir name
        self.temp_directory = Path("unzipped-{}".format(filename))
    
    # Delegator method
    def zip_find_replace(self):
        self.unzip_files()
        self.find_replace()
        self.zip_files()

    def unzip_files(self):
        # Create temp dir
        try:
            self.temp_directory.mkdir()
        except FileExistsError:
            print("WARNING: temp dir already present!")
        with zipfile.ZipFile(self.filename) as zip:
            zip.extractall(str(self.temp_directory))

    def find_replace(self):
        for filename in self.temp_directory.iterdir():
            with filename.open() as file:
                contents = file.read()
                contents = contents.replace(self.search_string, self.replace_string)
            with filename.open("w") as file:
                file.write(contents)

    def zip_files(self):
        with zipfile.ZipFile(self.filename, 'w') as file:
            for filename in self.temp_directory.iterdir():
                file.write(str(filename), filename.name)
        # Delete temp dir
        shutil.rmtree(str(self.temp_directory))

if __name__ == "__main__":
    if len(sys.argv[1:]) == 3:        
        ZipReplace(*sys.argv[1:4]).zip_find_replace()
        print("ZipReplace.zip_find_replace() executed with parameters: ",sys.argv[1:4])
    else:
        print("Please check the number of arguments")
        print("Usage example:\npython ZipReplace.py prova.zip Maria Mario")