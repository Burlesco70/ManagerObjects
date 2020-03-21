''' 
#####################################################################
TOPIC PYTHON OBJECT ORIENTED - ALL ACTION OBJECTS - MANAGERS - PART 3
#####################################################################
See how simple it is now to create a photo scaling class that takes advantage of the ZipProcessor functionality. 

(Note: this class requires the third-party pillow library to get the PIL module. 
You can install it with pip install pillow

Look how simple this class is! 
All that work we did earlier paid off. 
All we do is open each file (assuming that it is an image; 
it will unceremoniously crash if a file cannot be opened), scale it, and save it back. 
The ZipProcessor class takes care of the zipping and unzipping without any extra work on our part
'''

import sys
import shutil
import zipfile
from pathlib import Path
from PIL import Image

class ZipProcessor:
    def __init__(self, filename):
        self.filename = filename
        # Define temp dir name
        self.temp_directory = Path("unzipped-{}".format(filename))
    
    # Delegator method
    def process_zip(self):
        self.unzip_files()
        self.process_files()
        self.zip_files()

    def unzip_files(self):
        # Create temp dir
        try:
            self.temp_directory.mkdir()
        except FileExistsError:
            print("WARNING: temp dir already present!")
        with zipfile.ZipFile(self.filename) as zip:
            zip.extractall(str(self.temp_directory))

    def process_files(self):
        pass

    def zip_files(self):
        with zipfile.ZipFile(self.filename, 'w') as file:
            for filename in self.temp_directory.iterdir():
                file.write(str(filename), filename.name)
        # Delete temp dir
        shutil.rmtree(str(self.temp_directory))

class ScaleZip(ZipProcessor):
    def process_files(self):
        '''Scale each image to 640x480'''
        for filename in self.temp_directory.iterdir():
            im = Image.open(str(filename))
            scaled = im.resize((640, 480))
            scaled.save(str(filename))

if __name__ == "__main__":
    if len(sys.argv[1:]) == 1:
        ScaleZip(*sys.argv[1:2]).process_zip()
        print("ScaleZip.process_zip() executed with parameters: ",sys.argv[1:2])
    else:
        print("Please check the number of arguments")
        print("Usage example:\npython ScaleZip.py immagini.zip")    