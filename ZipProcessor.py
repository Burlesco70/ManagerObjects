''' 
#####################################################################
TOPIC PYTHON OBJECT ORIENTED - ALL ACTION OBJECTS - MANAGERS - PART 2
#####################################################################
 Removing duplicate code 
 Often the code in management style classes such as ZipReplace is quite generic and can be applied in a variety of ways. 
 It is possible to use either composition or inheritance to help keep this code in one place, thus eliminating duplicate code. 
 
 Let's explore two ways we can reuse existing code. 
 After writing our code to replace strings in a ZIP file full of text files, 
 we are later contracted to scale all the images in a ZIP file to 640 x 480. 
 
 Looks like we could use a very similar paradigm to what we used in ZipReplace. 
 The first impulse might be to save a copy of that file and change the find_replace method to scale_image or something similar.
 
 But, that's uncool. What if someday we want to change the unzip and zip methods to also open TAR files? 
 Or maybe we want to use a guaranteed unique directory name for temporary files. 
 In either case, we'd have to change it in two different places! 
 We'll start by demonstrating an inheritance-based solution to this problem. 
 First we'll modify our original ZipReplace class into a superclass for processing generic ZIP files.

 This code is a bit shorter than the original version, since it inherits its ZIP processing abilities from the parent class. 
 We first import the base class we just wrote and make ZipReplace extend that class. 
 Then we use super() to initialize the parent class. 
 The find_replace method is still here, but we renamed it to process_files so the parent class can call it from its management interface. 
 Because this name isn't as descriptive as the old one, we added a docstring to describe what it is doing. 
 Now, that was quite a bit of work, considering that all we have now is a program that is functionally not different from the one we started with! 
 But having done that work, it is now much easier for us to write other classes that operate on files in a ZIP archive, such as the (hypothetically requested) photo scaler. 
 Further, if we ever want to improve or bug fix the zip functionality, we can do it for all classes by changing only the one ZipProcessor base class. 
 Maintenance will be much more effective.
'''

import sys
import shutil
import zipfile
from pathlib import Path

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

class ZipReplace(ZipProcessor):
    def __init__(self, filename, search_string, replace_string):
        super().__init__(filename)
        self.search_string = search_string
        self.replace_string = replace_string

    def process_files(self):
        '''Perform search and replace for each file'''
        for filename in self.temp_directory.iterdir():
            with filename.open() as file:
                contents = file.read()
                contents = contents.replace(self.search_string, self.replace_string)
            with filename.open("w") as file:
                file.write(contents)

if __name__ == "__main__":
    if len(sys.argv[1:]) == 3:        
        ZipReplace(*sys.argv[1:4]).process_zip()
        print("ZipReplace.zip_find_replace() executed with parameters: ",sys.argv[1:4])
    else:
        print("Please check the number of arguments")
        print("Usage example:\npython ZipReplace.py prova.zip Maria Mario")    