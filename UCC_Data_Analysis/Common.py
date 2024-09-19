"""
Set of functions that will be common to all python scripts
File IO, Data Analysis etc. 


R. Sheehan 12 - 12 - 2014
"""

# In python this is known as a Module
# https://docs.python.org/3/tutorial/modules.html

#It should be possible to call the functions using
#import Common

#You need to tell whatever script you are writing where the Common.py file is stored.
#This is done in the file with the sys library

MOD_NAME_STR = "Common" # use this in exception handling messages

"""
Libraries
"""

# In python 3 the print(statement was replaced by a print(function
# see https://stackoverflow.com/questions/13415181/brackets-around-print-in-python
#from __future__ import print_function

import os
import glob
import re
import sys # access system routines

import math
import scipy
import numpy as np
import matplotlib.pyplot as plt

#from scipy.interpolate import interp1d # module for interpolation in 1D
#from scipy.interpolate import griddata # module for interpolation in 2D
#from pylab import *
#from scipy import *
#from scipy import optimize

"""
Constants
"""
ELECTRIC_CHARGE = 1.6e-19 # Fundamental charge in units of C
PLANCK_CONSTANT = 4.135667e-15# Planck's constant in eVs
SPEED_OF_LIGHT = 3.0e14 # speed of light in microns per second
HC = 1.23984193 # hc [eV.um]
TWO_PI = 2.0 * math.pi

"""
Dictionaries
"""
# define dictionary to contain the SI prefix values
SI_Prefices = {"femto":1.0e-15, "pico":1.0e-12, "nano":1.0e-9, "micro":1.0e-6, 
               "milli":1.0e-3, "one":1.0, "kilo":1.0e+3, "Mega":1.0e+6, "Giga":1.0e+9}

def dict_contains_key(dict, key):
    
    return True if key in dict else False

def dict_contains_value(dict, value):
    
    return True if value in dict.values() else False

"""
Test import
"""
def test_import():
    # simple check to see if the function definitions have been imported

    for i in range(0, 10, 1):
        print("The file Common.py has been imported correctly")

    return 24

"""
String Manipulation
"""

def extract_values_from_string(the_string):
    # extract all values from a string

    # this should return all integer and float values contained in a string
    values = re.findall("[-+]?\d+[\.]?\d*", the_string) 

    # this should return all integer, float and scientific notataion values contained in a string
    #match_number = re.compile('-?\ *[0-9]+\.?[0-9]*(?:[Ee]\ *-?\ *[0-9]+)?')
    #values = re.findall("-?\d+.?\d*(?:[Ee]-\d+)?", the_string) 

    if values:
        return values
    else:
        return None

def extract_strings_without_substring(the_strings, the_substring):
    # extract all strings from the list the_strings
    # that do not contain substring 

    if the_strings is not None:
        the_sub_list = []
        for s in the_strings:
            if the_substring not in s:
                the_sub_list.append(s)

        return the_sub_list
    else:
        return None

def isfloat(value):
    # is a string a float value?
    try:
        float(value)
        return True
    except ValueError:
        return False
"""
File IO
"""
def count_lines(thedata, thepath, quiet = 0):
    # count the number of lines in a file that has been opened and read into memory
    # thedata is the stream that contains the data from an open file
    # how do you know if thedata contains data?
    # assume that you only call count_lines inside another function for reading data
    # thepath is the name of the file containing the data
    # R. Sheehan 26 - 4 - 2014

    nlines=0
    for lines in thedata:
        nlines = nlines + 1
    if quiet:
        print("There are %(nlines)d lines in %(path)s"%{"nlines":nlines,"path":thepath})
    
    return nlines

def open_file(thepath):
    # given a filename thepath, open it for reading and return a file object that can be accessed
    # it may be an idea to return a dictionary or something
    # R. Sheehan 26 - 4 - 2014

    thefile = open(thepath,"r") # open file for reading

    # check that the files are available
    if thefile.closed:
        print("%(path)s could not be opened"%{"path":thepath})
        return 0
    else:
        print("%(path)s is open"%{"path":thepath})
        return thefile

def read_data(thepath, quiet = 0):
    # read data from an open file
    # R. Sheehan 26 - 4 - 2014
    # returns data as a numpy array

    if glob.glob(thepath):

        thefile = open(thepath,"r") # open file for reading

        # check that the files are available
        if thefile.closed:
            print("%(path)s could not be opened"%{"path":thepath})
            datapts = np.array([])
            return datapts # return an empty array
        else:
            if quiet:
                print("%(path)s is open"%{"path":thepath})

            thedata = thefile.readlines() # read the data from the file

            nlines = count_lines(thedata, thepath) # count the number of data points

            datapts = np.zeros([nlines]) # create an array of zeros of length nlines

            i=0
            for lines in thedata:
                datapts[i] = lines
                i = i + 1

            del thedata # clear thedata stream

            del thefile

            return datapts

def head(filename, nlines):
    
    # read the head (i.e. first N lines) of a file
    # store the result as a list of strings
    # R. Sheehan 1 - 3 - 2022

    FUNC_NAME = ".head()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        with open(filename) as myfile:
            head = [next(myfile) for x in range(nlines)]
        return head
    except Exception as e:
        print(ERR_STATEMENT)
        print(e)

def read_two_columns(name, delimiter = ',', quiet = 0):
    
    # read two columns of data from a file

    thefile = open(name,"r") # open file for reading

    success = -1

    # check that the files are available
    if thefile.closed:
        print("%(path)s could not be opened"%{"path":name})
        return [success, 0, 0, 0]
    else:
        if quiet:
            print("%(path)s is open"%{"path":name})

        thedata = thefile.readlines() # read the data from the file

        npts = len(thedata)

        # for this application looking to store
        # positions, data
        
        positions = [] # data from first column
        data = [] # data from second column
        
        for x in range(0,len(thedata),1):
            item = thedata[x].split(delimiter)
            positions.append(float(item[0])) # data from first column
            data.append(float(item[1])) # data from second column

        if len(positions) > 0 and len(data) > 0:
            success = +1

        return [success, positions, data]

def read_three_columns(name, quiet = 0):

    # read three columns of data from a file

    thefile = open(name,"r") # open file for reading

    success = -1

    # check that the files are available
    if thefile.closed:
        print("%(path)s could not be opened"%{"path":name})
        return [success, 0, 0, 0, 0]
    else:
        if quiet:
            print("%(path)s is open"%{"path":name})

        thedata = thefile.readlines() # read the data from the file

        npts = len(thedata)

        # for this application looking to store
        # positions, Total N carriers, Total P carriers

        positions = [] # data from first column
        Ndata = [] # data from second column
        Pdata = [] # data from third column
        
        for x in range(0,len(thedata),1):
            item = thedata[x].split(',')
            positions.append(float(item[0])) # data from first column
            Ndata.append(float(item[1])) # data from second column
            Pdata.append(float(item[2])) # data from third column

        if len(positions) > 0 and len(Ndata) > 0 and len(Pdata) > 0:
            success = +1

        return [success, positions, Ndata, Pdata]

#def read_four_columns(name, quiet = 0):
#    # read four columns of data from a file
#    thefile = file(name,"r") # open file for reading
#    success = -1
#    # check that the files are available
#    if thefile.closed:
#        print("%(path)s could not be opened"%{"path":name}
#        return [success, 0, 0, 0, 0]
#    else:
#        if quiet:
#            print("%(path)s is open"%{"path":name}
#        thedata = thefile.readlines() # read the data from the file
#        npts = len(thedata)
#        # for this application looking to store
#        # positions, Total N carriers, Total P carriers
#        positions = [] # data from first column
#        Ndata = [] # data from second column
#        Pdata = [] # data from third column
#        Qdata = [] # data from fourth column
#        for x in range(0,len(thedata),1):
#            item = thedata[x].split(',')
#            positions.append(float(item[0])) # data from first column
#            Ndata.append(float(item[1])) # data from second column
#            Pdata.append(float(item[2])) # data from third column
#            Qdata.append(float(item[3])) # data from fourth colum
#        if len(positions) > 0 and len(Ndata) > 0 and len(Pdata) > 0 and len(Qdata) > 0:
#            success = +1
#        return [success, positions, Ndata, Pdata, Qdata]

def read_five_columns(name):

    # useful for band diagram data

    thefile = open(name,"r") # open file for reading

    success = -1

    # check that the files are available
    if thefile.closed:
        print("%(path)s could not be opened"%{"path":name})
        datapts = -1
        return [success, 0, 0, 0, 0, 0, 0]
    else:
        print("%(path)s is open"%{"path":name})

        thedata = thefile.readlines() # read the data from the file

        # store names of columns from file
        #names = thedata[0].split(',')
        names = thedata[0]

        npts = -1 + len(thedata)

        # for this application looking to store
        # positions, Ec, Ev
        # with zero bias Efn = Efp = Ef

        positions = [] # distance along device p -> n
        Ecdata = [] # conduction band energy
        Efndata = [] # fermi level on n side
        Evdata = [] # valence band data
        Efpdata = [] # fermi level on p side
        
        for x in range(1,len(thedata),1):
            item = thedata[x].split(',')
            positions.append(float(item[0])) # distance along device p -> n
            Ecdata.append(float(item[1])) # conduction band energy
            Efndata.append(float(item[2])) # fermi level on n side
            Evdata.append(float(item[3])) # valence band data
            Efpdata.append(float(item[4])) # fermi level on p side

        if len(positions) > 0 and len(Ecdata) > 0 and len(Evdata) > 0:
            success = +1

        return [success, names, positions, Ecdata, Efndata, Evdata, Efpdata]

def write_two_columns(thepath, first_line, col1_data, col2_data, wr_mode):
    # write two lists to some file with name thepath
    
    try:

        c1 = True if col1_data is not None else False
        c2 = True if col2_data is not None else False
        c3 = True if len(col1_data) == len(col2_data) else False
        c4 = True if c1 and c2 and c3 else False

        if c4:
            if wr_mode == "w" or wr_mode == "a":
                thefile = open(thepath, wr_mode)
                if thefile.closed:
                    raise IOError
                else:
                    # file is open for writing
                    thefile.write(first_line + "\n")

                    for i in range(0, len(col1_data), 1):
                        thefile.write("%(v1)0.9f, %(v2)0.9f\n"%{"v1":col1_data[i], "v2":col2_data[i]})

                    thefile.close()
            else:
                raise IOError
        else:
            raise Exception
    except IOError:
        print("Error: Common.write_two_columns()")
        print("Could not open file",thepath)
    except Exception as e:
        print("Error: Common.write_two_columns()")
        print("Input lists were not defined correctly")
        print(e)

def write_data(thepath, thedata, loud = False):
    # write a vector containing data to a file
    # R. Sheehan 7 - 8 - 2014

    FUNC_NAME = ".write_data()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:

        c1 = True if thepath == '' else False
        #c2 = True if thedata == None else False
        c3 = True if len(thedata) == 0 else False
        c4 = c1 and c3

        if c4:
            raise Exception
        else:
            thefile = open(thepath, "w")
            if thefile.closed:
                raise Exception
            else:
                if loud: print("File:",thepath,"open for writing\n")

                for data in thedata:
                    thefile.write("%(num)0.9f\n"%{"num":data})

                thefile.close()
                
                if loud: print("File:",thepath,"closed\n")
    except Exception as e:
        print(ERR_STATEMENT)
        print(e)

def write_matrix(thepath, thedata, delim = ', ', loud = False):
    # write a matrix of data to a file
    # R. Sheehan 7 - 8 - 2014

    # Attempted to update
    # but then I realised nunpy.save exists
    # https://numpy.org/doc/stable/reference/generated/numpy.savetxt.html
    # R. Sheehan 8 - 2 - 2024

    FUNC_NAME = ".write_matrix()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        thefile = open(thepath, "w")

        if thefile.closed:
            ERR_STATEMENT = ERR_STATEMENT + '\nCould not open: ' + thefile.name
            raise Exception
        else:
            if loud:
                print("The file",thefile.name,"is open")

            nrows = len(thedata)

            ncols = len(thedata[0])

            for i in range(nrows):
                for j in range(ncols):
                    if j == ncols - 1:
                        thefile.write("%(num)0.9f"%{"num":thedata[i][j]})
                    else:
                        thefile.write("%(num)0.9f%(v1)s"%{"num":thedata[i][j], "v1":delim})
                thefile.write("\n")

            thefile.close()

        # delete the file object
        del thefile
    except Exception as e:
        print(ERR_STATEMENT)
        print(e)

def read_matrix(thepath, delimiter = ',', ignore_first_line = False, loud = False):
    # read an array of data from a file
    # if ignore_first_line == True, this means the first line of the file
    # contains text and should not be counted when reading in data
    # R. Sheehan 8 - 8 - 2014

    thefile = open(thepath,"r") # open file for reading

    # check that the files are available
    if thefile.closed:
        print("%(path)s could not be opened"%{"path":thepath})
        datapts = -1
    else:
        if loud: print("%(path)s is open"%{"path":thepath})

        thedata = thefile.readlines() # read the data from the file

        nrows = count_lines(thedata, thepath) # count the number of rows

        if loud: print("Nrows = ",nrows)
        
        if ignore_first_line:
            ncols = len(thedata[1].split(delimiter)) # count the number of columns
            nrows -= 1 # substract one from the number of rows
        else:
            ncols = len(thedata[0].split(delimiter)) # count the number of columns

        if loud: print("rows = ",nrows,"cols = ",ncols)

        #datapts = np.zeros([nrows, ncols]) # create an array of zeros of length nlines
        datapts = list_2D_array(nrows, ncols)
            
        for i in range(0, nrows, 1 ):
            for j in range(0,ncols,1):
                if ignore_first_line:
                    datapts[i][j] = float(thedata[i+1].split(delimiter)[j])
                else:
                    datapts[i][j] = float(thedata[i].split(delimiter)[j])
        
    del thefile

    return datapts

def read_four_columns(name, loud = False):

    # read four columns of data from a file
    # useful for plotting multiple data sets

    thefile = open(name,"r") # open file for reading

    success = -1

    # check that the files are available
    if thefile.closed:
        print("%(path)s could not be opened"%{"path":name})
        return [success, 0, 0, 0, 0]
    else:
        if loud: print("%(path)s is open"%{"path":name})

        thedata = thefile.readlines() # read the data from the file

        separator = ',' # this takes the value ',' or '\t', others also possible

        # store names of columns from file
        names = thedata[0].split(separator) # returns an array
        #names = thedata[0] # split when you need it

        npts = -1 + len(thedata)

        # for this application looking to store
        # col1, col2, col2, col3

        col1 = [] # column 1
        col2 = [] # column 2
        col3 = [] # column 3
        col4 = [] # column 4
        
        for x in range(0,len(thedata),1):
            item = thedata[x].split(separator)
            col1.append(float(item[0])) # column 1
            col2.append(float(item[1])) # column 2
            col3.append(float(item[2])) # column 3
            col4.append(float(item[3])) # column 4

        if len(col1) > 0 and len(col2) > 0 and len(col3) > 0 and len(col4) > 0:
            success = +1

        return [success, col1, col2, col3, col4]

"""
2D Array / Matrix Functions

"""
def list_1D_array(size):
	# return a python list of length size whose elements are all set to zero
    # indexing starts at zero and ends at size-1
	# alternative is to use [None]*size
	# this method uses list comprehensions

    try:
        if size > 0:
            return [0 for i in range(size)]
        else:
            raise ValueError
    except ValueError:
        print("\nError: Common.list_1D_array")
        print("size <= 0\n")
        return None

def numpy_1D_array(size):
    # return a numpy array of length size whose elements are all set to zero
    # create an array of zeros of length nlines
    # indexing starts at zero and ends at size-1

    try:
        if size > 0:
            return np.zeros( [ size ] )
        else:
            raise ValueError
    except ValueError:
        print("\nError: Common.numpy_1D_array")
        print("size <= 0\n")
        return None

def numpy_2D_array(rows, columns):
    # return a 2D numpy array of size rows*columns whose elements are all set to zero
    # indexing starts at zero and ends at rows-1 / columns-1
    # array accessed as Z[row_index, col_index]

    try:
        if rows > 0 and columns > 0:
            return np.zeros( [ rows, columns ] )
        else:
            raise ValueError
    except ValueError:
        print("\nError: Common.numpy_2D_array")
        print("rows <= 0 or columns <=0\n")
        return None

def list_2D_array(rows, columns):
    # return a 2D python list of size rows*columns whose elements are all set to zero
    # indexing starts at zero and ends at rows-1 / columns-1
    # array accessed as Z[row_index, col_index]

    try:
        if rows > 0 and columns > 0:
            ret_lst = list_1D_array(rows)
            for i in range(rows):
                ret_lst[i] = list_1D_array(columns)

            return ret_lst
        else:
            raise ValueError
    except ValueError:
        print("\nError: Common.list_2D_array")
        print("rows <= 0 or columns <=0\n")
        return None

def get_matrix_dims(matrix):
    # retrieve the dimensions of a 2D array
    # R. Sheehan 18 - 5 - 2016

    try:
        if matrix is not None:
            row_size = len( matrix )
            col_size = len( matrix[0] )
            return [row_size, col_size]
        else:
            raise ValueError
    except ValueError:
        print("\nError: Common.get_matrix_dims")
        print("matrix = None\n")
        return None

def get_row(matrix, row_num):
    # return row number row_num from 2D array matrix

    try:
        if matrix is not None and row_num > -1:
            row_size = len( matrix )
            if row_num < row_size:
                return matrix[ row_num ]
            else:
                raise IndexError
        else:
            raise ValueError
    except ValueError:
        print("\nError: Common.get_row")
        print("matrix = None or row < 0\n")
        return None
    except IndexError:
        print("\nError: Common.get_row")
        print("requested row is outside valid range\n")
        return None

def get_col(matrix, col_num):
    # return col number col_num from 2D array matrix
    # this assumes that matrix is of numpy type

    # is there a way to distinuguish between numpy arrays and lists? 

    try:
        if matrix is not None and col_num > -1:
            row_size = len(matrix)
            col_size = len(matrix[0])

            if col_num < col_size:
                array = numpy_1D_array( row_size )

                for i in range(0,row_size,1):
                    array[i] = matrix[i][col_num]

                return array
            else:
                raise IndexError
        else:
            raise ValueError
    except ValueError:
        print("\nError: Common.get_col")
        print("matrix = None or col_num < 0\n")
        return None
    except IndexError:
        print("\nError: Common.get_col")
        print("requested column is outside valid range\n")
        return None
        
def store_col(matrix, col_num, array):
    # store the data in array in column col_num of matrix
    # length of array must equal number of rows in matrix
    # array must already exist and have correct size

    try:
        if matrix is not None and array is not None:

            row_size = len(matrix)
            col_size = len(matrix[0])

            if col_num < col_size and row_size == len(array):

                for i in range(0, row_size, 1):
                    matrix[i, col_num] = array[i]

            else:
                raise ValueError
        else:
            raise ValueError
    except ValueError:
        print("\nError: Common.store_col")
        print("matrix = None or col_num < 0\n")

"""
System Calls

"""
def delete_files(file_extension, proceed = False):
    # delete all files with extension file_extension
    # in a given directory

    if proceed:
        thefiles = glob.glob("*" + file_extension)

        # ask the user to ensure that they want to delete all files
        gonogo = False

        gonogo = input('Do you really want to delete all ' + file_extension + ' files: ')

        if gonogo:
            for name in thefiles: os.remove(name)

        del thefiles


"""
Data Analysis

"""
def average_data(file_str, loud = False):
    # compute the average of multiple sets of data
    # this assumes that all files contain the same number of data points
    # R. Sheehan 1 - 2 - 2016

    # this function requires a file name template as its input
    # it then checks for the existence of the files
    # what might be more useful is to input a list of known file names into the function

    try:

        f1 = glob.glob(file_str)

        if f1:

            nfiles = len(f1)

            ndata = len(read_data(f1[0]))

            data = numpy_2D_array(ndata, nfiles)

            average = []

            # read all the data into memory
            # store each file in a column of the array data
            for jj in range(0, len(f1), 1):
                store_col(data, jj, read_data(f1[jj]) )

            # average data across each row
            for ii in range(0, ndata, 1):
                      
                average.append( np.mean( get_row(data, ii) ) )
            
                if loud: print(average[ii])

            del data

            return average
        else:
            raise Exception
    except Exception as e:
        print("\nError: Common.average_data()")
        print(e)

def average_data_known_files(file_list, loud = False):
    # compute the average of multiple sets of data
    # file_list is a list of known file names
    # R. Sheehan 30 - 8 - 2016

    try:

        if file_list is not None:

            nfiles = len(file_list)

            ndata = len( read_data( file_list[0] ) )

            data = numpy_2D_array(ndata, nfiles)

            average = []

            # read all the data into memory
            # store each file in a column of the array data
            for jj in range(0, len(file_list), 1):
                store_col(data, jj, read_data( file_list[jj] ) )

            # average data across each row
            for ii in range(0, ndata, 1):
                      
                average.append( np.mean( get_row(data, ii) ) )
            
                if loud: print(average[ii])

            del data

            return average
        else:
            raise Exception
    except Exception as e:
        print("\nError: Common.average_data_known_files()")
        print("file_list is empty")
        print(e)

def average_error_data(file_str, avg_file_name, err_file_name, loud = False):
    # compute the average of multiple sets of data
    # as well as computing the max and min values
    # so that an error estimate can be computed
    # this assumes that all files contain the same number of data points
    # R. Sheehan 1 - 2 - 2016

    f1 = glob.glob(file_str)

    if f1:

        if loud: print(f1)

        nfiles = len(f1)

        ndata = len(read_data(f1[0]))

        data = numpy_2D_array(ndata, nfiles)

        average = []
        error = []

        # read all the data into memory
        # store each file in a column of the array data
        for jj in range(0, len(f1), 1):
            store_col(data, jj, read_data(f1[jj]))

        # average data across each row
        for ii in range(0, ndata, 1):
            
            row = get_row(data, ii)

            if loud: print(np.amax(row),",", np.amin(row),",",np.amax(row)-np.amin(row))
            
            average.append( np.mean( row ) )
            
            error.append( abs(np.amax(row) - np.amin(row)) )

            del row

        del data

        if loud:
            write_data(avg_file_name, average)
            write_data(err_file_name, error)

        return [average, error]
    else:
        return 0

def scale_to_unity(thedata):
    # scale a data set so that it's max value is unity
    # R. Sheehan 28 - 4 - 2014

    FUNC_NAME = ".scale_to_unity()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        if thedata is not None and len(thedata) > 0:
            maxval = np.amax(thedata) # find the maximum value
            minval = np.amin(thedata) # find the minimum value

            if maxval > 0.0:
                scaleddata = thedata / maxval
            elif maxval == 0.0 and minval < 0.0:
                scaleddata = thedata / minval

            return scaleddata
        else:
            return None
            raise Exception
    except Exception as e:
        print(ERR_STATEMENT)
        print(e)

def scale_data(thedata, scale_value):
    # scale a data set by some value
    # thedata must be numpy array
    # can always use np.asarray(thedata) if thedata is a list
    # R. Sheehan 15 - 1 - 2019

    FUNC_NAME = ".scale_data()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        c1 = True if thedata is not None else False
        c2 = True if len(thedata) > 0 else False
        c3 = True if math.fabs(scale_value) > 0.0 else False

        if c1 and c2 and c3:   
            scaleddata = thedata * scale_value            
            return scaleddata
        else:
            return None
            raise Exception
    except Exception as e:
        print(ERR_STATEMENT)
        print(e)

def divide_vectors(vecA, vecB):
    # divide the contents of vecA by the contents of vecB
    # vectors must be of equal length and and elements in vecB
    # cannot equal zero
    # R. Sheehan 4 - 2 - 2016

    try:
        if len(vecA) == len(vecB):
            result = []
            for ii in range(0, len(vecA), 1):
                if abs(vecB[ii]) > 1.0e-12:
                    result.append(vecA[ii] / vecB[ii])
                else:
                    # divide by a small number that is not zero
                    result.append(vecA[ii] / 1.0e-12)

            return result
        else:
            return None
    except Exception as e:
        print("\nError: Common.divide_vectors()")
        print("Error: Cannot divide two vectors of unequal length\n")
        print(e)

def linear_fit(xdata, ydata, initial_apprs, loud = False):
    # generate a linear fit to the data sets that are input
    
    # input arrays must be of numpy type
    
    # initial_apprs is a list of inital approximations of the form [intersection, slope]

    # the object returned is a list of the form [intersection, slope]
    # p1[0] = intersection, p1[1] = slope
    
    # R. Sheehan 23 - 9 - 2014

    # if data is not originally stored as numpy array use the numpy command np.asarray( data ) when calling

    try:
        c1 = True if xdata is not None else False
        c2 = True if ydata is not None else False
        c3 = True if len(xdata) == len(ydata) else False

        if c1 and c2 and c3:

            from scipy.optimize import leastsq

            fitfunc = lambda p, x: p[0] + p[1]*x # target function
        
            errfunc = lambda p, x, y: fitfunc(p, x) - y # distance function
        
            p0 = initial_apprs # Initial guess for the parameters
        
            p1, success = scipy.optimize.leastsq( errfunc, p0[:], args=(xdata, ydata) )

            # you need to include more inputs and so some post-processing in order to get error estimates of the computed fit parameters
            # https://docs.scipy.org/doc/scipy-0.18.1/reference/generated/scipy.optimize.leastsq.html
            # retval = scipy.optimize.leastsq(errfunc, p0[:], args=(xdata, ydata), Dfun = None, full_output = 1)

            if success:
                if loud: 
                    print("Fit polynomial is ",p1[0],"+",p1[1],"x")
                    print("Intercept: ",p1[0])
                    print("Slope: ",p1[1])

                #if loud:
                #    plot(xdata, ydata, "r^", xdata, fitfunc(p1, xdata), "g-")
                #    # Legend the plot
                #    title("Fitted data")
                #    xlabel("x")
                #    ylabel("y")
                #    legend(('Data', 'Fit'),loc='best')
                #    ax = axes()
                #    axis( [np.min(xdata), np.max(xdata), np.min(ydata), np.max(ydata)] )
                #    show()

                return p1
            else:
                print("Fit procedure was not successful")
                return None
        else:
            raise Exception
    except Exception as e:
        print("\nError: Common.linear_fit()")
        if c1 == False: print("Error: xdata is empty or not an array")
        if c2 == False: print("Error: ydata is empty or not an array")
        if c3 == False: print("Error: xdata and ydata have different lengths")
        print(e)
        return None

def quadratic_fit(xdata, ydata, initial_apprs, show_plots = 0):
    # generate a quadratic fit to the data sets that are input
    # input arrays must be of numpy type
    # return list contains quadratic coefficients of the form [c, b, a]
    # for quadratic a x^{2} + b x + c
    # R. Sheehan 23 - 9 - 2014

    # if data is not originally stored as numpy array use the numpy command np.asarray( data ) when calling

    try:
        c1 = True if xdata is not None else False
        c2 = True if ydata is not None else False
        c3 = True if len(xdata) == len(ydata) else False

        if c1 and c2 and c3:
            from scipy.optimize import leastsq

            fitfunc = lambda p, x: p[0] + p[1]*x + p[2]*(x**2) # target function
        
            errfunc = lambda p, x, y: fitfunc(p, x) - y # distance function
        
            p0 = initial_apprs # Initial guess for the parameters
        
            p1, success = scipy.optimize.leastsq(errfunc, p0[:], args=(xdata, ydata))

            if success:

                min_loc = (-1.0*p1[1]) / (2.0*p1[2])
                min_val = ( p1[0] - (p1[1]**2)/(4.0*p1[2]) )

                print("\nFit polynomial is ",p1[0],"+",p1[1],"x +",p1[2],"x**2")
                print("Turning point is located at x =",min_loc)
                if p1[2] > 0.0:
                    print("Minimum value of quadratic is f =",min_val,"\n")
                else:
                    print("Maximum value of quadratic is f =",min_val,"\n")

                return p1
            else:
                print("Fit procedure was not successful")
                return None
        else:
            raise Exception
    except Exception as e:
        print("Error: Common.quadratic_fit()")
        if c1 == False: print("Error: xdata is empty or not an array")
        if c2 == False: print("Error: ydata is empty or not an array")
        if c3 == False: print("Error: xdata and ydata have different lengths")
        print(e)
        return None

def index_max_val(data):
    # return the list index at which a maximum value occurs
    # this only works for python lists, not numpy arrays

    try:
        if data is not None:
            max_val = max(data)
            max_indx = data.index(max_val)

            return [max_val, max_indx]
        else:
            raise Exception
    except Exception as e:
        print("\nError: Common.index_max_val")
        print("data is None")
        print(e)

def index_max_val_numpy(data):
    # return the index at which a maximum values occurs
    # this is the numpy version

    try:
        if data is not None:
            max_val = np.amax(data)
            max_indx = np.where(data == max_val)

            return [max_val, max_indx]
        else:
            raise Exception
    except Exception as e:
        print("\nError: Common.index_max_val_numpy")
        print("data is None")
        print(e)

def index_some_val_numpy(data, value):
    # find the closest element in a numpy array to value

    try:
        if data is not None:
            the_indx = np.where(data == value)

            return [value, the_indx]
        else:
            raise Exception
    except Exception as e:
        print("\nError: Common.index_some_val_numpy")
        print("data is None")
        print(e)

def sort_multi_col(data):
    # given a data set of the form data = [ [v1, v2, ..., vn], [v1, v2, ..., vn], [v1, v2, ..., vn],.... ]
    # sort the columns of the data according to the data in the first column
    # sort is performed in place

    data.sort(key=lambda data: float(data[0]) )
    
def sort_two_col(list1, list2):
        
    # sort two lists according to data in list1
    # R. Sheehan 9 - 7 - 2021
    
    try:
        if list1 is not None and list2 is not None:
            toSrt = sorted( zip( list1, list2 ) ) # sort the two lists together
            tuples = zip( *toSrt ) # form a list of tuples
            # unpack the data into two sorted lists
            return [list(tuple) for tuple in tuples]
        else:
            raise Exception
    except Exception as e:
        print("\nError: Common.sort_two_col")
        print("one of the inputs is empty")
        print(e)

def transpose_multi_col(data):
    # generate the transpose of a multi-column list
    # this will return the transpose of an array in a manner
    # that is convenient for plotting
    # this is arguably more convenient, and pythonic, than using the get_col or get_row method
    # this method assumes that each column has the same length

    return list( map( list, zip(*data) ) )

def integrate(x_data, y_data):
    # estimate the area under a given data set using the trapezoidal rule
    # R. Sheehan 12 - 5 - 2017

    try:
        c1 = True if x_data is not None else False
        c2 = True if y_data is not None else False
        c3 = True if len(x_data) == len(y_data) else False

        if c1 and c2 and c3:
            
            sum = 0.0
            k=0
            while k < len(x_data)-1:
                sum += (x_data[k+1] - x_data[k])*(y_data[k+1] + y_data[k])
                k+=1
            sum *= 0.5
            return sum

        else:
            raise Exception
    except Exception as e:
        print("Error: Common.integrate()")
        if c1 == False: print("x_data is not defined")
        if c2 == False: print("y_data is not defined")
        if c3 == False: print("x_data and y_data have different lengths")
        print(e)

def list_diff(x_lst, y_lst): 
    # compute the difference between two lists
    # return x_lst - y_lst
    # R. Sheehan 7 - 7 - 2017

    try:        
        if len(x_lst) == len(y_lst):
            diff = []
            for i in range(0, len(x_lst), 1):
                diff.append(x_lst[i] - y_lst[i])
            return diff
        else:
            return None
            raise Exception
    except Exception as e:
        print("Error: Common.list_diff")
        print("input lists have different lengths")
        print(e)

def list_convert_dBm_mW(x_lst): 
    # convert values in a list from dBm to mW
    # R. Sheehan 19 - 7 - 2017

    try:        
        if x_lst is not None:
            new_lst = []
            for i in range(0, len(x_lst), 1):
                new_lst.append(convert_PdBm_PmW(x_lst[i]))
            return new_lst
        else:
            return None
            raise Exception
    except Exception as e:
        print("Error: Common.list_convert_dBm_mW")
        print("input list is empty")
        print(e)

def list_convert_mW_dBm(x_lst): 
    # convert values in a list from mW to dBm
    # R. Sheehan 4 - 9 - 2017

    try:        
        if x_lst is not None:
            new_lst = []
            for i in range(0, len(x_lst), 1):
                new_lst.append(convert_PmW_PdBm(x_lst[i]))
            return new_lst
        else:
            return None
            raise Exception
    except Exception as e:
        print("Error: Common.list_convert_mW_dBm")
        print("input list is empty")
        print(e)

def list_search(x_lst, value, start_here, tolerance, loud = False, rec_depth = 0):

    # determine if x_lst contains value to within specified tolerance
    # return index at which list element closest to value occurs and value at that element
    
    # find out if there is a standard search algorithm that you can use
    # the idea here is to have an alternative to list.index(item)

    # x_lst is the list containing the data items
    # value is the element sought inside x_lst
    # start_here is the index where the element search should begin
    # tolerance is the accuracy to which the element is sought
    # loud dictates whether print(statements are executed
    # rec_depth is the recursion depth, number of recursions that function is allowed to execute, this is limited to 3

    # R. Sheehan 3 - 10-  2017

    try:
        max_rec_depth = 4 # maximum number of recursive calls allowed
        c1 = True if x_lst is not None else False
        if c1:
            c2 = True if start_here > -1 and start_here < len(x_lst) else False
            c3 = True if tolerance > 0.0 else False
            if c1 and c2:
                fabs_val = math.fabs(value)
                if fabs_val < math.fabs(x_lst[0]) or fabs_val > math.fabs(x_lst[-1]):
                    print("Element:",value," is not contained in x_lst")
                    return None
                else:
                    if loud: print("x_lst contains",value)
                    
                    indx = start_here; x_lst_val = x_lst[start_here];
                    for i in range(start_here, len(x_lst), 1):
                        if math.fabs(value - x_lst[i]) < tolerance:
                            if loud: print("Element:",value,"found at position",i,"with value",x_lst[i])
                            indx = i; x_lst_val = x_lst[i]; 
                            break
                    
                    if indx > start_here:
                        if loud:
                            print("rec-depth",rec_depth,", tol:",tolerance)
                        return [indx, x_lst_val]
                    else:
                        # value was not found to within tolerance
                        # increase tolerance by factor of 10 and search again
                        rec_depth += 1
                        if rec_depth < max_rec_depth:
                            return list_search(x_lst, value, start_here, 10.0*tolerance, False, rec_depth)
                        else:
                            print("Recursion Depth Exceeded")
                            return [indx, x_lst_val]
            else:
                raise Exception
        else:
            raise Exception
    except Exception as e:
        print("\nError: Common.list_search()")
        print(e)

def list_has_negative(data):
    # check that all values in data are positive
    # return = True if data contains negative value

    # use the built-in any() function
    # https://docs.python.org/3/library/functions.html#any
    
    # alternatively could use the all() function
    # https://docs.python.org/3/library/functions.html#all
    
    # R. Sheehan 13 - 11 - 2017

    try:
        if data is not None and len(data) > 0:
            return any(item < 0 for item in data)
        else:
            raise Exception
    except Exception as e:
        print("Error: Common.list_has_negative()")
        print(e)

"""
Unit Conversions

""" 

def convert_deg_rad(degValue):
    # convert value in degrees to value in radians
    # V_{rad} = pi V_{deg} / 180

    return (math.pi * degValue / 180)

def convert_rad_deg(radValue):
    # convert value in radians to value in degrees
    # V_{deg} = 180 V_{rad} / pi

    return (180 * radValue / math.pi)

def convert_um_cm(umValue):
    # convert a length in microns to centimetres
    # V_{cm} = 1e-4 V_{um}

    return (1e-4*umValue)

def convert_nm_um(nmValue):
    # convert a length in nanometres to microns
    # V_{um} = 1000 V_{nm}

    return (1.0e-3*nmValue)

def convert_angs_nm(angsValue):
    # convert Angstroms to nanometres
    # V_{nm} = 0.1 V_{Angstroms}

    return (0.1*angsValue)

def convert_nm_angs(nmValue):
    # convert nanometres to Angstroms
    # V_{Angstroms} = 10 V_{nm}

    return (10*nmValue)

def convert_invcm_nm(invcmValue):
    # convert inverse centimetres to nanometres
    # R. Sheehan 13 - 11 - 2018

    try:
        if invcmValue > 0.0:
            return (1.0e+7 / invcmValue)
        else:
            raise RuntimeError
    except RuntimeError:
        print("Error: Common.convert_invcm_nm()")
        return 0.0

def convert_PmW_PdBm(mWvalue):
    # convert power in mW to power in dBm
    # P_{dBm} = 10 * \log_{10}{ ( P_{mW} / 1 mW ) }

    if mWvalue < 0.0 or mWvalue == 0.0:
        return 1.0e-10
    else:
        return ( 10.0*( math.log10( mWvalue ) ) )

def convert_PdBm_PmW(dBmvalue):
    # convert power in dBm to power in mW
    # P_{mW} = 1 mW * 10^{P_{dBm} / 10}
    
    return (  math.pow( 10, (dBmvalue/10.0) ) )

def convert_PdBm_PW(dBmvalue):
    # convert power in dBm to power in W
	# firstly convert value to P_{mW} then convert to W
    # P_{W} = (1 mW * 10^{P_{dBm} / 10}) / 1000
    
    return (  math.pow( 10, (dBmvalue/10.0) ) / 1000.0 )

def convert_PmW_PW(mWvalue):
	# convert power in mW to power in W
	# P_{W} = P_{mW} / 1000
	
	return ( mWvalue / 1000.0 )

def convert_dB(value, ref_level):
    # convert some value to dB scale relative to reference ref_level
    # V_{dB} = 10 log_{10}(value / ref_level)

    FUNC_NAME = ".convert_dB()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        if abs(ref_level) > 0.0:
            ratio = abs(value) / abs(ref_level)
            if ratio < 0.0 or ratio == 0.0:
                return 1.0e-6
            else:
                return 10.0*math.log10(ratio)
        else:
            return -1.0
            raise Exception
    except Exception as e:
        print(ERR_STATEMENT)
        print(e)


def convert_C_K(Cvalue):
    # convert temperature in degrees Celcius to degrees Kelvin
    # T_{K} = T_{C} + 273.15

    return (Cvalue + 273.15)

def convert_K_C(Kvalue):
    # convert temperature in degrees Kelvin to degrees Celcius
    # T_{C} = T_{K} - 273.15

    return (Kvalue - 273.15)

def convert_Split_Power_Reading(power_value, split_ratio_low, split_ratio_high):
    # convert single measured power reading from a splitter
    # R. Sheehan 23 - 3 - 2017

    try:

        sr_sum = (split_ratio_low + split_ratio_high)
        srr = (split_ratio_high/split_ratio_low)

        c1 = True if power_value != 0.0 else False
        c2 = True if sr_sum == 1.0 else False
        c3 = True if split_ratio_low > 0.0 else False

        if c1 and c2 and c3:
            # convert the (dBm) data to (mW) scale and multiply by splitter value
            mW_value = srr*convert_PdBm_PmW( power_value )
            return convert_PmW_PdBm(mW_value)
        else: 
            raise Exception
    except Exception as e:
        print("Error: Common.convert_Split_Power_Reading")
        if c1 == False: print("Error: power_value = 0")
        if c2 == False: print("Error: split_ratio does not sum to unity")
        if c3 == False: print("Error: split_ratio_low is not positive")
        print(e)
        return -1

def convert_Split_Power_Readings(power_data, split_ratio_low, split_ratio_high):

    # convert a power reading through a splitter into another ratio
    # data must be in units of dBm
    # R. Sheehan 20 - 3 - 2017

    try:

        c1 = True if power_data != None else False
        c2 = True if len(power_data) > 0 else False

        if c1 and c2:

            converted_power_data = []

            for j in range(0, len(power_data), 1):
                converted_power_data.append( convert_Split_Power_Reading(power_data[j], split_ratio_low, split_ratio_high) )

            return converted_power_data
        else:
            raise Exception
    except Exception as e:
        print("\nError: Common.convert_Split_Power_Readings()")
        if c1 == False or c2 == False: print("Cannot operate on empty list\n")
        print(e)
        return None

def convert_Log_Scale(the_data):

    # convert elements of a list to log scale
    # R. Sheehan 20 - 3 - 2017

    try:

        c1 = True if the_data != None else False
        c2 = True if len(the_data) > 0 else False

        if c1 and c2:

            converted_data = []

            for j in range(0, len(the_data), 1):

                converted_data.append( math.log10( the_data[j] ) )

            return converted_data
        else:
            raise Exception
    except Exception as e:
        print("\nError: Common.convert_Log_Scale()")
        if c1 == False or c2 == False: print("Cannot operate on empty list\n")
        print(e)
        return None

# generic plot function
def plot_this(h_data, v_data, curve_label = "", x_label = "X (units)", y_label = "Y (units)", plt_title = "", plt_range = None, fig_name = "", loud = False):
    # a much needed generic plot function
    # R. Sheehan 3 - 4 - 2017

    try:
        c1 = True if h_data is not None else False
        c2 = True if v_data is not None else False
        c3 = True if len(h_data) > 0 else False
        c4 = True if len(v_data) > 0 else False
        c5 = True if len(h_data) == len(v_data) else False
        c6 = True if c1 and c2 and c3 and c4 and c5 else False

        if c6:
            # make the plot
            fig = plt.figure()
            ax = fig.add_subplot(111)

            if curve_label is not "":
                ax.plot(h_data, v_data, "r*", lw = 2, ms = 10, label = curve_label)
                ax.legend(loc = 'best')
            else:
                ax.plot(h_data, v_data, "r*", lw = 2, ms = 10)
            
            plt.xlabel(x_label, fontsize = 17)
            plt.ylabel(y_label, fontsize = 17)
            
            if plt_title is not "": plt.title(plt_title)
            if plt_range is not None: plt.axis( plt_range )

            # plot endmatter
            if fig_name is not "": plt.savefig(fig_name)
            if loud: plt.show()
            plt.clf()
            plt.cla()
            plt.close()
        else:
            raise Exception
    except Exception as e:
        print("\nError: Common.plot_this()")
        if c1 == False: print("h_data is not defined")
        if c2 == False: print("v_data is not defined")
        if c3 == False: print("h_data has no elements")
        if c4 == False: print("v_data has no elements")
        if c5 == False: print("h_data and v_data have different lengths")
        print(e)

def plot_this_with_linear_fit(h_data, v_data, curve_label = "", x_label = "X (units)", y_label = "Y (units)", plt_title = "", plt_range = None, fig_name = "", loud = False):
    # a much needed generic plot function
    # R. Sheehan 3 - 4 - 2017

    try:
        c1 = True if h_data is not None else False
        c2 = True if v_data is not None else False
        c3 = True if len(h_data) > 0 else False
        c4 = True if len(v_data) > 0 else False
        c5 = True if len(h_data) == len(v_data) else False
        c6 = True if c1 and c2 and c3 and c4 and c5 else False

        if c6:

            lin_fit = linear_fit(np.asarray(h_data), np.asarray(v_data), [3.0, -5.0])

            # make the plot
            fig = plt.figure()
            ax = fig.add_subplot(111)

            if curve_label is not "":
                ax.plot(h_data, v_data, "r*", ms = 10, label = curve_label)
                ax.plot([ h_data[0], h_data[-1] ], 
                    [ lin_fit[0] + lin_fit[1]*h_data[0], lin_fit[0] + lin_fit[1]*h_data[-1] ], 
                    "r-", lw = 2)
                ax.legend(loc = 'best')
            else:
                ax.plot(h_data, v_data, "r*", lw = 2, ms = 10)
                ax.plot([ h_data[0], h_data[-1] ], 
                    [ lin_fit[0] + lin_fit[1]*h_data[0], lin_fit[0] + lin_fit[1]*h_data[-1] ], 
                    "r-", lw = 2)
            
            plt.xlabel(x_label, fontsize = 17)
            plt.ylabel(y_label, fontsize = 17)
            
            if plt_title is not "": plt.title(plt_title)
            if plt_range is not None: plt.axis( plt_range )

            # plot endmatter
            if fig_name is not "": plt.savefig(fig_name)
            if loud: plt.show()
            plt.clf()
            plt.cla()
            plt.close()
        else:
            raise Exception
    except Exception as e:
        print("\nError: Common.plot_this()")
        if c1 == False: print("h_data is not defined")
        if c2 == False: print("v_data is not defined")
        if c3 == False: print("h_data has no elements")
        if c4 == False: print("v_data has no elements")
        if c5 == False: print("h_data and v_data have different lengths")
        print(e)
