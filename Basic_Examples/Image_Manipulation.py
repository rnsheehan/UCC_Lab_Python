# Import libraries
# You should try an import the bare minimum of modules
import sys # access system routines
import os
import glob
import re

import math
import matplotlib.pyplot as plt



def main():
    pass

if __name__ == '__main__':
    main()

    pwd = os.getcwd() # get current working directory

    home = pwd

    print(pwd)

    DATA_HOME = 'C:/Users/Robert/Research/Publications/SPIE_Europe_2018/Sample_Images/'

    try:
        if os.path.isdir(DATA_HOME):

            from PIL import Image
            from StringIO import StringIO

            os.chdir(DATA_HOME)

            print(os.getcwd())

            img_files = glob.glob("*.png")

            for f in img_files:
                f_out = f.replace(".png",".eps") # rename the files
                #f_out = f.replace(".png","")
                #print f,",",f_out
                print(f_out)
                img = Image.open(f,"r")
                print("File Attributes")
                print("Image Size:",img.size)
                print("Image Format:",img.format)
                print("Image Mode:",img.mode)
                print("Image Palette:",img.palette)
                print("Image Info:",img.info)
                #print(img.histogram()) # return a histogram of the image
                #img.save(f_out,".eps") # Can't seem to get the save function working
        else:
            raise EnvironmentError
    except EnvironmentError:
        print("Error: Image_Format_Convert_Test")
        print("Cannot find",DATA_HOME)
    except Exception:
        print("Error: Image_Format_Convert_Test")
    
