"""
Implementation of a library that shows how to use the Plotting.py library
The set of examples is not exhaustive but covers the most important / common types of plots
1. Plot showing single data set
2. Plot showing single data set with error bars
3. Plot showing linear fit to single data set
4. Plot showing linear fit to single data set including error bars
5. Plot showing multiple data sets
6. Plot showing multiple data sets with error bars
7. Plot showing linear fit to multiple data sets
8. Plot showing multiple data sets with imported data

R. Sheehan 19 - 9 - 2024
"""

# Name the module
MOD_NAME_STR = "Plotting_Examples"

# Import the necessary libraries
import math
import numpy
import Common
import Plotting

def Generate_Synthetic_Data(slope_val, make_it_noisy = True, include_errors = False, loud = False):

    """
    Generate a synthetic data set of the form Y = m X + c + noise

    Inputs: 
    slope_val (type: float) is the slope of the synthetic data set, assuming slope_val \in [-10, 10]
    make_it_noisy (type: boolean) tells the method whether or not to add a random noise term to the data, default is True
    include_errors (type: boolean) tells the method whether or not to include errors, default to False
    loud (type: boolean) tells the method whether or to print progress statements to screen, default is False

    n_pts will be fixed at 31
    x_data range will be fixed [0, 10]
    intercept value will be a random float in the range [-5, 5]
    
    Outputs: 
    the_data (type: list) list of the form [x_vals, y_vals, err_vals]
    """

    FUNC_NAME = ".Generate_Synthetic_Data()"
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME


    try:
        # Test the inputs to see if they are in the correct range
        c1 = True if math.fabs(slope_val) < 10.1 else False

        if c1:
            # Create a random intercept value 
            # This value is drawn randomly from a normal distribution with mean mu and std. dev. sigma
            mu = 0.0; sigma = 1.0; size = 1; 
            intrcpt_val = numpy.random.normal(mu, sigma, size)

            # Generate x_data
            x_strt = 0
            x_end = 10
            n_pts = 31
            x_data = numpy.linspace(x_strt, x_end, n_pts, endpoint = True)

            # Generate y_data
            y_data = numpy.array([]) # start with an empty array
            for i in range(0, n_pts, 1):
                y_val = slope_val * x_data[i] + intrcpt_val
                if make_it_noisy:
                    y_val = y_val + numpy.random.normal(mu, sigma, size)
                y_data = numpy.append(y_data, y_val)

            # Generate err_data, if required
            # These values are drawn randomly from a normal distribution with mean mu and std. dev. sigma
            mu = 0.0; sigma = 5.0; 
            err_data = numpy.abs( numpy.random.normal(mu, sigma, n_pts) ) if include_errors else numpy.array([])

            if loud:
                print("Intercept = ",intrcpt_val)
                print("x_data = ",x_data)
                print("y_data = ",y_data)
                print("err_data = ",err_data)

            return [x_data, y_data, err_data]
        else:
            ERR_STATEMENT = ERR_STATEMENT + "\nInput slope_val outside acceptable range\n"
            raise Exception
    except Exception as e: 
        print(ERR_STATEMENT)
        print(e)

def Single_Data_Set():

    """
    Make a plot showing a single data set
    """

    FUNC_NAME = ".Single_Data_Set()"
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME


    try:
        # Generate the data set
        slope = 2.5

        x_vals, y_vals, err_vals = Generate_Synthetic_Data(slope, include_errors=False, loud=False)

        # Create the arguments for the plot
        args = Plotting.plot_arg_single()

        CHANGE_ARG_VALS = True

        if CHANGE_ARG_VALS:
            # Assign different values to the default arguments

            args.x_label = 'Qtx (x units)' # name the x-axis
            args.y_label = 'Qty (y units)' # name the y-axis
            args.curve_label = 'Data Slope %(v1)0.1f'%{"v1":slope} # 
            args.marker = Plotting.labs_pts[5] # assign a plot marker, line style and colour to the curve
            args.plt_range = [1, 3, 2, 9] # change the plot range
            args.plt_title = 'Single Data Set Plot' # Give the plot a title
            args.loud = True # print the plot to the screen
            args.fig_name = 'Single_Data_Set' # assign fig_name to be non empty string to save the plot to a file
        else:
            # Generate the plot with default arguments
            args.loud = True # print the plot to the screen       

        # Generate the plot
        Plotting.plot_single_curve(x_vals, y_vals, args)

        # Delete the data when it is no longer needed
        # C++ will never die!
        del x_vals; del y_vals; del err_vals; 
    except Exception as e: 
        print(ERR_STATEMENT)
        print(e)

def Single_Data_Set_With_Errors():

    """
    Make a plot showing a single data set that also includes error bars
    """

    FUNC_NAME = ".Single_Data_Set_With_Errors()"
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        # Generate the data set
        slope = 3.7

        x_vals, y_vals, err_vals = Generate_Synthetic_Data(slope, include_errors=True, loud=False)

        # Create the arguments for the plot
        args = Plotting.plot_arg_single()

        CHANGE_ARG_VALS = True

        if CHANGE_ARG_VALS:
            # Assign different values to the default arguments

            args.x_label = 'Qtx (x units)' # name the x-axis
            args.y_label = 'Qty (y units)' # name the y-axis
            args.curve_label = 'Data Slope %(v1)0.1f'%{"v1":slope} # 
            args.marker = Plotting.labs_pts[1] # assign a plot marker, line style and colour to the curve
            #args.plt_range = [1, 3, 2, 9] # change the plot range
            args.plt_title = 'Single Data Set Plot Including Error Bars' # Give the plot a title
            args.loud = True # print the plot to the screen
            #args.fig_name = 'Single_Data_Set_With_Errors' # assign fig_name to be non empty string to save the plot to a file
        else:
            # Generate the plot with default arguments
            args.loud = True # print the plot to the screen       

        # Generate the plot
        Plotting.plot_single_curve_with_errors(x_vals, y_vals, err_vals, args)

        # Delete the data when it is no longer needed
        # C++ will never die!
        del x_vals; del y_vals; del err_vals; 
    except Exception as e: 
        print(ERR_STATEMENT)
        print(e)

def Single_Data_Set_Linear_Fit():

    """
    Make a plot showing a single data set that also includes a linear fit
    """

    FUNC_NAME = ".Single_Data_Set_Linear_Fit()"
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        # Generate the data set
        slope = 4.2

        x_vals, y_vals, err_vals = Generate_Synthetic_Data(slope, include_errors=True, loud=False)

        # Create the arguments for the plot
        args = Plotting.plot_arg_single()

        CHANGE_ARG_VALS = True

        if CHANGE_ARG_VALS:
            # Assign different values to the default arguments

            args.x_label = 'Qtx (x units)' # name the x-axis
            args.y_label = 'Qty (y units)' # name the y-axis
            args.curve_label = 'Data Slope %(v1)0.1f'%{"v1":slope} # 
            args.marker = Plotting.labs_pts[0] # assign a plot marker, line style and colour to the curve
            #args.plt_range = [1, 3, 2, 9] # change the plot range
            args.plt_title = 'Single Data Set Plot Including Linear Fit' # Give the plot a title
            args.loud = True # print the plot to the screen
            #args.fig_name = 'Single_Data_Set_Linear_Fit' # assign fig_name to be non empty string to save the plot to a file
        else:
            # Generate the plot with default arguments
            args.loud = True # print the plot to the screen       

        # Generate the plot
        # The method will not return the values associated with the linear fit
        Plotting.plot_single_linear_fit_curve(x_vals, y_vals, args)

        # If you want to see the parameters associated with the linear fit
        # You need to run the calculation yourself and print the results to screen
        lin_fit_pars = Common.linear_fit(x_vals, y_vals, [1, 1])
        print("Linear Fit Results Y = m X + c")
        print( "Fitted Intercept c = %(v1)0.2f"%{ "v1":lin_fit_pars[0] } )
        print( "Fitted Slope m = %(v1)0.2f"%{ "v1":lin_fit_pars[1] } )
        print( "Actual Slope m = %(v1)0.2f"%{ "v1":slope } )

        # Delete the data when it is no longer needed
        # C++ will never die!
        del x_vals; del y_vals; del err_vals; 
    except Exception as e: 
        print(ERR_STATEMENT)
        print(e)

def Single_Data_Set_Linear_Fit_With_Errors():

    """
    Make a plot showing a single data set that also includes a linear fit and error bars
    Note the linear fit does not take account of the error bars, although this is possible to implement
    """

    FUNC_NAME = ".Single_Data_Set_Linear_Fit_With_Errors()"
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        # Generate the data set
        slope = 1.6

        x_vals, y_vals, err_vals = Generate_Synthetic_Data(slope, include_errors=True, loud=False)

        # Create the arguments for the plot
        args = Plotting.plot_arg_single()

        CHANGE_ARG_VALS = True

        if CHANGE_ARG_VALS:
            # Assign different values to the default arguments

            args.x_label = 'Qtx (x units)' # name the x-axis
            args.y_label = 'Qty (y units)' # name the y-axis
            args.curve_label = 'Data Slope %(v1)0.1f'%{"v1":slope} # 
            #args.marker = Plotting.labs_pts[6] # assign a plot marker, line style and colour to the curve
            #args.plt_range = [1, 3, 2, 9] # change the plot range
            args.plt_title = 'Single Data Set Plot With Errors Including Linear Fit' # Give the plot a title
            args.loud = True # print the plot to the screen
            #args.fig_name = 'Single_Data_Set_Linear_Fit_With_Errors' # assign fig_name to be non empty string to save the plot to a file
        else:
            # Generate the plot with default arguments
            args.loud = True # print the plot to the screen       

        # Generate the plot
        # The method will not return the values associated with the linear fit
        Plotting.plot_single_linear_fit_curve_with_errors(x_vals, y_vals, err_vals, args)

        # If you want to see the parameters associated with the linear fit
        # You need to run the calculation yourself and print the results to screen
        lin_fit_pars = Common.linear_fit(x_vals, y_vals, [1, 1])
        print( "Linear Fit Results Y = m X + c" )
        print( "Fitted Intercept c = %(v1)0.2f"%{ "v1":lin_fit_pars[0] } )
        print( "Fitted Slope m = %(v1)0.2f"%{ "v1":lin_fit_pars[1] } )
        print( "Actual Slope m = %(v1)0.2f"%{ "v1":slope } )

        # Delete the data when it is no longer needed
        # C++ will never die!
        del x_vals; del y_vals; del err_vals; 
    except Exception as e: 
        print(ERR_STATEMENT)
        print(e)

def Multiple_Data_Set():

    """
    Make a plot showing multiple data sets
    """

    FUNC_NAME = ".Multiple_Data_Set()"
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    # The main difference to be aware of when generating plots of multiple data sets
    # is how the data is input into the plotting methods
    # Several sets of (X, Y) data pairs are created, each pair is assigned a plot marker and plot label
    # The data are then gathered together into lists of the form
    # hv_data = [ (X1, Y1), (X2, Y2), ...., (Xn, Yn)]
    # mark_list = [marker1, marker2, ..., markern]
    # label_list = [label1, label2, ..., labeln]
    # hv_data is then passed into the plotting method, mark_list and label_list are assigned to the plotting_arguments object
    # This will make sense with an example

    try:
        # Generate the data sets
        slope1 = 1.6
        x_vals_1, y_vals_1, err_vals_1 = Generate_Synthetic_Data(slope1, include_errors=False, loud=False)

        slope2 = -2.1
        x_vals_2, y_vals_2, err_vals_2 = Generate_Synthetic_Data(slope2, include_errors=False, loud=False)

        slope3 = 3.4
        x_vals_3, y_vals_3, err_vals_3 = Generate_Synthetic_Data(slope3, include_errors=False, loud=False)

        slope4 = -4.6
        x_vals_4, y_vals_4, err_vals_4 = Generate_Synthetic_Data(slope4, include_errors=False, loud=False)

        # Form the list needed to input the data into plotting methods
        # Obviously in reality you would loop over this setup
        # But it's best to be stupidly explicit here
        hv_data = []
        mark_list = []
        label_list = []

        hv_data.append([x_vals_1, y_vals_1]); mark_list.append(Plotting.labs_pts[0]); label_list.append("Slope = %(v1)0.1f"%{"v1":slope1})
        hv_data.append([x_vals_2, y_vals_2]); mark_list.append(Plotting.labs_pts[1]); label_list.append("Slope = %(v1)0.1f"%{"v1":slope2})
        hv_data.append([x_vals_3, y_vals_3]); mark_list.append(Plotting.labs_pts[3]); label_list.append("Slope = %(v1)0.1f"%{"v1":slope3})
        hv_data.append([x_vals_4, y_vals_4]); mark_list.append(Plotting.labs_pts[4]); label_list.append("Slope = %(v1)0.1f"%{"v1":slope4})

        # Create the arguments for the plot
        # A different object is needed to pass the arguments into the multi-curve plot
        args = Plotting.plot_arg_multiple()

        CHANGE_ARG_VALS = True

        if CHANGE_ARG_VALS:
            # Assign different values to the default arguments

            args.x_label = 'Qtx (x units)' # name the x-axis
            args.y_label = 'Qty (y units)' # name the y-axis
            args.crv_lab_list = label_list # assign the label_list in the plot_arguments object
            args.mrk_list = mark_list # assign the mark_list in the plot_arguments object
            args.loud = True # print the plot to the screen
            #args.fig_name = 'Multiple_Data_Set' # assign fig_name to be non empty string to save the plot to a file
        else:
            # Generate the plot with default arguments
            args.loud = True # print the plot to the screen       

        # Generate the plot
        Plotting.plot_multiple_curves(hv_data, args)

        # Delete the data when it is no longer needed
        # C++ will never die!
        del x_vals_1; del y_vals_1; del err_vals_1;
        del x_vals_2; del y_vals_2; del err_vals_2;
        del x_vals_3; del y_vals_3; del err_vals_3;
        del x_vals_4; del y_vals_4; del err_vals_4;
        del hv_data; del label_list; del mark_list; 
    except Exception as e: 
        print(ERR_STATEMENT)
        print(e)

def Multiple_Data_Set_With_Errors():

    """
    Make a plot showing multiple data sets that also includes error bars
    """

    FUNC_NAME = ".Multiple_Data_Set_With_Errors()"
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    # The main difference to be aware of when generating plots of multiple data sets
    # is how the data is input into the plotting methods
    # Several sets of (X, Y, Err) data pairs are created, each set is assigned a plot marker and plot label
    # The data are then gathered together into lists of the form
    # hv_data = [ (X1, Y1, Err1), (X2, Y2, , Err2), ...., (Xn, Yn, , Errn)]
    # mark_list = [marker1, marker2, ..., markern]
    # label_list = [label1, label2, ..., labeln]
    # hv_data is then passed into the plotting method, mark_list and label_list are assigned to the plotting_arguments object
    # This will make sense with an example

    try:
        # Generate the data sets
        slope1 = 1.6
        x_vals_1, y_vals_1, err_vals_1 = Generate_Synthetic_Data(slope1, include_errors=True, loud=False)

        slope2 = -2.1
        x_vals_2, y_vals_2, err_vals_2 = Generate_Synthetic_Data(slope2, include_errors=True, loud=False)

        slope3 = 3.4
        x_vals_3, y_vals_3, err_vals_3 = Generate_Synthetic_Data(slope3, include_errors=True, loud=False)

        slope4 = -4.6
        x_vals_4, y_vals_4, err_vals_4 = Generate_Synthetic_Data(slope4, include_errors=True, loud=False)

        # Form the list needed to input the data into plotting methods
        # Obviously in reality you would loop over this setup
        # But it's best to be stupidly explicit here
        hv_data = []
        mark_list = []
        label_list = []

        hv_data.append([x_vals_1, y_vals_1, err_vals_1]); mark_list.append(Plotting.labs_pts[0]); label_list.append("Slope = %(v1)0.1f"%{"v1":slope1})
        hv_data.append([x_vals_2, y_vals_2, err_vals_2]); mark_list.append(Plotting.labs_pts[1]); label_list.append("Slope = %(v1)0.1f"%{"v1":slope2})
        hv_data.append([x_vals_3, y_vals_3, err_vals_3]); mark_list.append(Plotting.labs_pts[3]); label_list.append("Slope = %(v1)0.1f"%{"v1":slope3})
        hv_data.append([x_vals_4, y_vals_4, err_vals_4]); mark_list.append(Plotting.labs_pts[4]); label_list.append("Slope = %(v1)0.1f"%{"v1":slope4})

        # Create the arguments for the plot
        # A different object is needed to pass the arguments into the multi-curve plot
        args = Plotting.plot_arg_multiple()

        CHANGE_ARG_VALS = True

        if CHANGE_ARG_VALS:
            # Assign different values to the default arguments

            args.x_label = 'Qtx (x units)' # name the x-axis
            args.y_label = 'Qty (y units)' # name the y-axis
            args.crv_lab_list = label_list # assign the label_list in the plot_arguments object
            args.mrk_list = mark_list # assign the mark_list in the plot_arguments object
            args.loud = True # print the plot to the screen
            #args.fig_name = 'Multiple_Data_Set_With_Errors' # assign fig_name to be non empty string to save the plot to a file
        else:
            # Generate the plot with default arguments
            args.loud = True # print the plot to the screen       

        # Generate the plot
        Plotting.plot_multiple_curves_with_errors(hv_data, args)

        # Delete the data when it is no longer needed
        # C++ will never die!
        del x_vals_1; del y_vals_1; del err_vals_1;
        del x_vals_2; del y_vals_2; del err_vals_2;
        del x_vals_3; del y_vals_3; del err_vals_3;
        del x_vals_4; del y_vals_4; del err_vals_4;
        del hv_data; del label_list; del mark_list;
    except Exception as e: 
        print(ERR_STATEMENT)
        print(e)

def Multiple_Data_Set_Linear_Fit():

    """
    Make a plot showing multiple data sets that also includes linear fits
    """

    FUNC_NAME = ".Multiple_Data_Set_Linear_Fit()"
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    # The main difference to be aware of when generating plots of multiple data sets
    # is how the data is input into the plotting methods
    # Several sets of (X, Y) data pairs are created, each set is assigned a plot marker and plot label
    # The data are then gathered together into lists of the form
    # hv_data = [ (X1, Y1), (X2, Y2), ...., (Xn, Yn)]
    # mark_list = [marker1, marker2, ..., markern]
    # label_list = [label1, label2, ..., labeln]
    # hv_data is then passed into the plotting method, mark_list and label_list are assigned to the plotting_arguments object
    # This will make sense with an example

    try:
        # Generate the data sets
        # Form the list needed to input the data into plotting methods
        # Loops are the ebst way to do this
        slopes = [1.6, -2.1, 3.4, -4.6]    
        hv_data = []
        mark_list = []
        label_list = []
        for i in range(0, len(slopes), 1):
            x_vals, y_vals, err_vals = Generate_Synthetic_Data(slopes[i])
            hv_data.append([x_vals, y_vals])
            mark_list.append( Plotting.labs_pts[ i % len( Plotting.labs_pts ) ] )
            label_list.append("Slope = %(v1)0.1f"%{"v1":slopes[i]})
    
        # Create the arguments for the plot
        # A different object is needed to pass the arguments into the multi-curve plot
        args = Plotting.plot_arg_multiple()

        CHANGE_ARG_VALS = True

        if CHANGE_ARG_VALS:
            # Assign different values to the default arguments

            args.x_label = 'Qtx (x units)' # name the x-axis
            args.y_label = 'Qty (y units)' # name the y-axis
            args.crv_lab_list = label_list # assign the label_list in the plot_arguments object
            args.mrk_list = mark_list # assign the mark_list in the plot_arguments object
            args.loud = True # print the plot to the screen
            #args.fig_name = 'Multiple_Data_Set_Linear_Fit' # assign fig_name to be non empty string to save the plot to a file
        else:
            # Generate the plot with default arguments
            args.loud = True # print the plot to the screen       

        # Generate the plot
        Plotting.plot_multiple_linear_fit_curves(hv_data, args)

        # If you want to see the parameters associated with the linear fit
        # You need to run the calculation yourself and print the results to screen
        print("Linear Fit Results Y = m X + c")
        for i in range(0, len(hv_data), 1):
            lin_fit_pars = Common.linear_fit(numpy.asarray( hv_data[i][0] ), numpy.asarray( hv_data[i][1] ), [1, 1])        
            print("Data set",i+1)
            print( "Fitted Intercept c = %(v1)0.2f"%{ "v1":lin_fit_pars[0] } )
            print( "Fitted Slope m = %(v1)0.2f"%{ "v1":lin_fit_pars[1] } )
            print( "Actual Slope m = %(v1)0.2f\n"%{ "v1":slopes[i] } )

        # Delete the data when it is no longer needed
        # C++ will never die!
        del x_vals; del y_vals; del err_vals; 
        del hv_data; del label_list; del mark_list;
    except Exception as e: 
        print(ERR_STATEMENT)
        print(e)

def Multiple_Data_Set_Imported():
    """
    Make a plot of multiple data sets by importing the data from multiple files

    The data is a real measurement of the VI curve of a lossy diode, i.e. a diode with a series resistance
    The data comprises several files containing columns of measured Current (mA) and Voltage (V) data
    """

    FUNC_NAME = ".Multiple_Data_Set_Imported()"
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        import os # needed to access os utilities
        import glob # glob is great

        DATA_HOME = 'Diode_Fit_Test_Data/'

        # test to see if the directory DATA_HOME exists
        if os.path.isdir(DATA_HOME):
            HOME = os.getcwd()
            os.chdir(DATA_HOME) # move to the directory containing the data
            print(os.getcwd())

            the_files = glob.glob("FR1001*.txt") # Determine the no. of files that need to be analysed

            print("There are ",len(the_files)," files to be analysed")
            #print(the_files)

            Rlist = ['000','010','022','047','067']
            file_template = 'FR1001_Rs_%(v1)s.txt'

            # plot all the measured data together
            hv_data = []; marks = []; labels = []; 
            count = 0
            for r in Rlist: 
                the_file = file_template%{"v1":r}
                if glob.glob(the_file):
                    data = numpy.loadtxt(the_file, delimiter = '\t', unpack = True)
                    hv_data.append(data)
                    marks.append( Plotting.labs_pts[ count % len( Plotting.labs_pts ) ] )
                    labels.append('$R_{s}$  = %(v2)d $\Omega$'%{"v2":int(r)})
                    count = count + 1

            # Make the plot
            args = Plotting.plot_arg_multiple()

            args.loud = True
            args.crv_lab_list = labels
            args.mrk_list = marks
            args.x_label = 'Current / mA'
            args.y_label = 'Voltage / V'
            args.fig_name = 'Lossy_Diode_Data'
            args.plt_range = [0, 100, 0, 8]

            Plotting.plot_multiple_curves(hv_data, args)

            os.chdir(HOME) # return to original wd
            print(os.getcwd())

            del hv_data; del labels; del marks;
        else:
            ERR_STATEMENT = ERR_STATEMENT + '\nCannot locate: ' + DATA_HOME
            raise Exception
    except Exception as e: 
        print(ERR_STATEMENT)
        print(e)