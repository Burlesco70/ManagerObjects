''' 
#####################################################################
TOPIC PYTHON OBJECT ORIENTED - ALL ACTION OBJECTS - MANAGERS - PART 4
#####################################################################
 Using composition instead of Inheritance

 Now look at the inheritance-based ZipProcessor. 
 It might be reasonable to use composition instead of inheritance here. 
 Instead of extending the class in the ZipReplace and ScaleZip classes, 
 you could pass instances of those classes into the ZipProcessor constructor 
 and call them to do the processing part. Implement this...

 Which version do you find easier to use? 
 Which is more elegant? What is easier to read? 
 These are subjective questions; the answer varies for each of us. 
 Knowing the answer, however, is important; 
 if you find you prefer inheritance over composition, 
 you have to pay attention that you don't overuse inheritance in your daily coding. 
 If you prefer composition, 
 make sure you don't miss opportunities to create an elegant inheritance-based solution
'''

import sys
import shutil
import zipfile
from pathlib import Path
from PIL import Image

# Any processor class is passed to ZipProcessor
# Composition instead of Inheritance
class ZipProcessor:
    def __init__(self, processor: object, filename: str):
        self.filename = filename
        # Processor is the object with implements "process_files"
        self.processor = processor
        # Define temp dir name
        self.temp_directory = Path("unzipped-{}".format(filename))
    
    # Delegator method
    def process_zip(self):
        self.unzip_files()
        # Call process_files() of composite, passing self as parameter
        self.processor.process_files(self)
        self.zip_files()

    def unzip_files(self):
        # Create temp dir
        try:
            self.temp_directory.mkdir()
        except FileExistsError:
            print("WARNING: temp dir already present!")
        with zipfile.ZipFile(self.filename) as zip:
            zip.extractall(str(self.temp_directory))

    def zip_files(self):
        with zipfile.ZipFile(self.filename, 'w') as file:
            for filename in self.temp_directory.iterdir():
                file.write(str(filename), filename.name)
        # Delete temp dir
        shutil.rmtree(str(self.temp_directory))

# To be used inside ZipProcessor must implement process_files()
class ZipReplace():
    def __init__(self, search_string: str, replace_string: str):
        self.search_string = search_string
        self.replace_string = replace_string

    def process_files(self, zipprocessor: ZipProcessor):
        '''Perform search and replace for each file'''
        for fname in zipprocessor.temp_directory.iterdir():
            with fname.open() as file:
                contents = file.read()
                contents = contents.replace(self.search_string, self.replace_string)
            with fname.open("w") as file:
                file.write(contents)

# To be used inside ZipProcessor must implement process_files()
class ScaleZip():

    def process_files(self, zipprocessor: ZipProcessor):
        '''Scale each image to 640x480'''
        for fname in zipprocessor.temp_directory.iterdir():
            im = Image.open(str(fname))
            scaled = im.resize((640, 480))
            scaled.save(str(fname))

# Examples of calls
sz = ScaleZip()
ZipProcessor(sz, 'Immagini.zip').process_zip()
zr = ZipReplace('Mario', 'Maria')
ZipProcessor(zr, 'provaReplace.zip').process_zip()
