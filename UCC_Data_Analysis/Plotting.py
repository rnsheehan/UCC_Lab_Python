"""
This module contains methods to produce several different types of plot
There is a generic plot method that can be used to plot single curves
The arguments to this method are passed by a class plot_arguments
I also want the option to be able to plot multiple curves on the same figure

NO DATA FORMATTING TO BE PERFORMED INSIDE PLOTTING METHODS!!!!!

R. Sheehan 28 - 4 - 2017
"""

# import pre-requisite modules
import numpy as np
import matplotlib.pyplot as plt

import Common

# colors = [red - r, green - g, blue - b, magenta - m, cyan - c, yellow - y, black - k]
# https://matplotlib.org/api/colors_api.html

# plot markers
# https://matplotlib.org/api/markers_api.html

# line style
# https://matplotlib.org/2.1.2/api/_as_gen/matplotlib.pyplot.plot.html

labs = ['r*-', 'g^-', 'b+-', 'md-', 'cp-', 'yh-', 'kx-' ] # plot labels
labs_lins = ['r-', 'g-', 'b-', 'm-', 'c-', 'y-', 'k-' ] # plot labels
labs_dashed = ['r--', 'g--', 'b--', 'm--', 'c--', 'y--', 'k--' ] # plot labels
labs_dotted = ['r:', 'g:', 'b:', 'm:', 'c:', 'y:', 'k:' ] # plot labels
labs_dotdash = ['r-.', 'g-.', 'b-.', 'm-.', 'c-.', 'y-.', 'k-.' ] # plot labels
labs_pts = ['r*', 'g^', 'b+', 'md', 'cp', 'yh', 'kx' ] # plot labels

labs_mrk_only = ['k*', 'k^', 'kd', 'kp'] # plot labels
# ‘solid’ | ‘dashed’, ‘dashdot’, ‘dotted’ 
# '-' | '--' | '-.' | ':'
labs_line_only = ['k-', 'k--', 'k:', 'k-.'] # plot labels

# This is the plot argument object
# R. Sheehan 28 - 4 - 2017

# The object should contain the following information
# string: x-axis title
# string: y-axis title
# string: plot title
# string: name of figure to be saved
# string: curve label

# list of strings: curve labels
# list of floats: plot range

# The pass keyword allows you to declare methods without defining them fully
# It's a sort of virtualisation feature
# Details here http://stackoverflow.com/questions/13886168/how-to-use-the-pass-statement-in-python 
# Details here https://docs.python.org/2/tutorial/classes.html#odds-and-ends

# The object keyword seems to be there as part of the new-style python class declaration
# http://stackoverflow.com/questions/4015417/python-class-inherits-object

# There could be an issue around type safety when using this object
# What if x_label gets assigned to some integer? 
# It seems there's no easy way to fix it other than check the type of each individual member, which seems quite cumbersome
# It seems that there's actually no need for this
# It looks like python knows that the type should be since I given the data member a default argument in constructor
# A general Exception is raised when an attempt is made to assign a member to a type that differs from the default value

class plot_arguments(object):
    # this is the base class for the derived classes plot_arg_single and plot_arg_multiple
    # is there anyway to prevent this class from being used? 
    # i.e. to declare it as private?
    # constructor
    # define default arguments inside
    def __init__(self):
        try: 
            # axis and plot labels
            self.x_label = "X (units)" # label for x-axis
            self.x_label_2 = "Xalt (units)" # label for a second x-axis if required
            self.y_label = "Y (units)" # label for y-axis
            self.y_label_2 = "Yalt (units)" # label for a second y-axis if required
            self.plt_title = "" # label for the plot
            self.plt_range = None # list to contain the bounds of the plot
            self.xold = None # array for holding x-axis values in the case of 2 x-axis plot
            self.xnew = None # array for holding x-axis values in the case of 2 x-axis plot
            self.fig_name = "" # string to name the figure to be saved
            self.loud = False # decide whether or not plot should be printed to screen

            # The legend
            self.show_leg = True

            # plot markers
            self.thick = 2 # line thickness
            self.msize = 10 # point size

            # specialisations
            self.log_x = False # decide if you want to plot horizontal values on log scale
            self.log_y = False # decide if you want to plot vertical values on log scale

            # add the ability to define custom tick-labels and custom tick-markers
            # when these are being used you must have self.log_x = self.log_y = False
            # custom ticks are invoked by the command: plt.(x)(y)ticks( tck_vals, tck_labs)
            self.y_tck_vals = None; self.y_tck_labs = None; 
            self.x_tck_vals = None; self.x_tck_labs = None; 

            # I'm not going to include these members as part of the class because I want all data processing
            # to be done before any plot function is called, i.e. no data processing inside a plot method!
            #self.scale_vert = False # decide whether or not to scale the values along the vertical axis
            #self.scale_factor = 1000.0
        except TypeError:
            print("Type Error in plotting.plot_arguments(object) instantiation")

    # return a string the describes the class
    def __str__(self):
        return "Arguments for a plot"
    
class plot_arg_single(plot_arguments):
    # derived class for plots with a single curve
    # base class is plot_arguments
    def __init__(self):
        try: 
            
            plot_arguments.__init__(self) # need to initialise the base class, ensure access to all members

            # axis and plot labels
            self.curve_label = "" # label for a single curve

            # plot markers
            self.marker = 'r*-' # plot marker type

        except TypeError:
            print("Type Error in plotting.plot_arguments(object) instantiation")

class plot_arg_multiple(plot_arguments):
    # derived class for plots with multiple curves
    # base class is plot_arguments
    def __init__(self):
        try: 
            plot_arguments.__init__(self) # need to initialise the base class, ensure access to all members

            # axis and plot labels
            self.crv_lab_list = None # list of labels for multiple curves in a plot
            
            # plot markers
            self.mrk_list = None # list of plot markers to be deployed in a plot

        except TypeError:
            print("Type Error in plotting.plot_arguments(object) instantiation")

def plot_single_curve(h_data, v_data, plt_args):
    # plot a single data set with arguments supplied by plt_args
    # h_data is a list of length N
    # v_data is a list of length N
    # plt_args is an object with multiple data members, see class plot_arguments(object)
    # R. Sheehan 3 - 4 - 2017

    # .png is the default matplotlib format

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

            if plt_args.curve_label != "":
                if plt_args.log_x and plt_args.log_y:
                    ax.loglog(h_data, v_data, plt_args.marker, lw = plt_args.thick, ms = plt_args.msize, label = plt_args.curve_label)
                elif plt_args.log_x and plt_args.log_y == False:
                    ax.semilogx(h_data, v_data, plt_args.marker, lw = plt_args.thick, ms = plt_args.msize, label = plt_args.curve_label)
                elif plt_args.log_x == False and plt_args.log_y:
                    ax.semilogy(h_data, v_data, plt_args.marker, lw = plt_args.thick, ms = plt_args.msize, label = plt_args.curve_label)                
                else:
                    ax.plot(h_data, v_data, plt_args.marker, lw = plt_args.thick, ms = plt_args.msize, label = plt_args.curve_label)
                ax.legend(loc = 'best')
            else:
                if plt_args.log_x and plt_args.log_y:
                    ax.loglog(h_data, v_data, plt_args.marker, lw = plt_args.thick, ms = plt_args.msize)
                elif plt_args.log_x and plt_args.log_y == False:
                    ax.semilogx(h_data, v_data, plt_args.marker, lw = plt_args.thick, ms = plt_args.msize)
                elif plt_args.log_x == False and plt_args.log_y:
                    ax.semilogy(h_data, v_data, plt_args.marker, lw = plt_args.thick, ms = plt_args.msize)
                else:
                    ax.plot(h_data, v_data, plt_args.marker, lw = plt_args.thick, ms = plt_args.msize)
            
            # for more on set_yscale see https://matplotlib.org/api/_as_gen/matplotlib.axes.Axes.set_yscale.html
            # https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.set_xscale.html
            # https://matplotlib.org/stable/gallery/scales/log_demo.html#sphx-glr-gallery-scales-log-demo-py
            #if plt_args.log_y: ax.set_yscale('log')

            plt.xlabel(plt_args.x_label, fontsize = 14)
            plt.ylabel(plt_args.y_label, fontsize = 14)

            #if plt_args.log_y is False: plt.ticklabel_format(useOffset=False) # use this to turn off tick label scaling
            #ax.get_xaxis().get_major_formatter().set_scientific(False)
            # for more info on this see 
            # https://stackoverflow.com/questions/14711655/how-to-prevent-numbers-being-changed-to-exponential-form-in-python-matplotlib-fi

            # for more on yticks see 
            # https://matplotlib.org/api/pyplot_api.html?highlight=matplotlib%20pyplot%20yticks#matplotlib.pyplot.yticks
            if plt_args.y_tck_vals is not None and plt_args.y_tck_labs is not None:
                plt.yticks( plt_args.y_tck_vals, plt_args.y_tck_labs)
            
            if plt_args.plt_title != "": plt.title(plt_args.plt_title)
            if plt_args.plt_range is not None: plt.axis( plt_args.plt_range )

            # plot endmatter
            if plt_args.fig_name != "": plt.savefig(plt_args.fig_name)
            if plt_args.loud: plt.show()
            plt.clf()
            plt.cla()
            plt.close()
        else:
            raise Exception
    except Exception as e:
        print("\nError: Plotting.plot_single_curve()")
        if c1 == False: print("h_data is not defined")
        if c2 == False: print("v_data is not defined")
        if c3 == False: print("h_data has no elements")
        if c4 == False: print("v_data has no elements")
        if c5 == False: print("h_data and v_data have different lengths")
        print(e)

def plot_single_semilogx(h_data, v_data, plt_args):

    # Generate a semilog plot of the data (h_data, y_data)
    # where the x-axis is logarithmic
    # R. Sheehan 3 - 3 - 2022

    try:
        c1 = True if h_data is not None else False
        c2 = True if v_data is not None else False
        c3 = True if len(h_data) > 0 else False
        c4 = True if len(v_data) > 0 else False
        c5 = True if len(h_data) == len(v_data) else False
        c6 = True if c1 and c2 and c3 and c4 and c5 else False

        if c6:
            fig = plt.figure()
            ax = fig.add_subplot(111)

            if plt_args.curve_label != "":
                ax.semilogx(h_data, v_data, plt_args.marker, lw = plt_args.thick, ms = plt_args.msize, label = plt_args.curve_label)
                ax.legend(loc = 'best')
            else:
                ax.semilogx(h_data, v_data, plt_args.marker, lw = plt_args.thick, ms = plt_args.msize)

            plt.xlabel(plt_args.x_label, fontsize = 14)
            plt.ylabel(plt_args.y_label, fontsize = 14)

            # for more on yticks see 
            # https://matplotlib.org/api/pyplot_api.html?highlight=matplotlib%20pyplot%20yticks#matplotlib.pyplot.yticks
            if plt_args.y_tck_vals is not None and plt_args.y_tck_labs is not None:
                plt.yticks( plt_args.y_tck_vals, plt_args.y_tck_labs)
            
            if plt_args.plt_title != "": plt.title(plt_args.plt_title)
            if plt_args.plt_range is not None: plt.axis( plt_args.plt_range )

            # plot endmatter
            if plt_args.fig_name != "": plt.savefig(plt_args.fig_name)
            if plt_args.loud: plt.show()
            plt.clf()
            plt.cla()
            plt.close()
        else:
            raise Exception
    except Exception as e:
        print("\nError: Plotting.plot_single_semilogx()")
        if c1 == False: print("h_data is not defined")
        if c2 == False: print("v_data is not defined")
        if c3 == False: print("h_data has no elements")
        if c4 == False: print("v_data has no elements")
        if c5 == False: print("h_data and v_data have different lengths")
        print(e)

def log_plot_error_bars(data, error):
    # pass data using np.asarray(.)
    # use this function to determine the error bars associated with a log plot
    # matplotlib cannot have negative values on error bar plots with log scale
    # so need to replace any negative error bar values with some minimum value
    # R. Sheehan 13 - 11 - 2017

    try:
        if Common.list_has_negative(data) or Common.list_has_negative(error):
            # data or error contains a negative value and as such cannot be used for a log-plot
            print("Data set has negative values")
            raise Exception
        else:
            min_data_val = 0.5*min(data)
            yerr_low = Common.numpy_1D_array( len(data) ); yerr_high = Common.numpy_1D_array( len(data) ); 
            yerr_low = data - np.maximum(min_data_val, data-0.5*error)
            yerr_high = data + 0.5*error
            return [yerr_low, yerr_high]
    except Exception as e:
        print("Error: Plotting.log_plot_error_bars()")
        print(e)

def plot_single_curve_with_errors(h_data, v_data, error, plt_args):
    # plot a single data set with arguments supplied by plt_args
    # h_data is a list of length N
    # v_data is a list of length N
    # error is the difference between max and min values averaged about v_data, must have length N
    # plt_args is an object with multiple data members, see class plot_arg_single(plot_arguments)

    # matplotlib errorbar plot documentation
    #https://matplotlib.org/api/_as_gen/matplotlib.axes.Axes.errorbar.html

    # examples
    #https://matplotlib.org/1.2.1/examples/pylab_examples/errorbar_demo.html

    # R. Sheehan 9 - 11 - 2017

    # .png is the default matplotlib format

    try:
        c1 = True if h_data is not None else False
        c2 = True if v_data is not None else False
        c3 = True if len(h_data) > 0 else False
        c4 = True if len(v_data) > 0 else False
        c5 = True if len(h_data) == len(v_data) else False
        c7 = True if len(error) > 0 else False
        c8 = True if len(error) == len(v_data) else False
        c6 = True if c1 and c2 and c3 and c4 and c5 and c7 and c8 else False       

        if c6:
            # need to adjust error bars in the case of a log-y plot 
            # must prevent negative error bar values
            
            #if plt_args.log_y == True:
            #    if Common.list_has_negative(v_data):
            #        # data set contains negative values, cannot make log plot
            #        print("Error: Plotting.plot_single_curve_with_errors()")
            #        print("Error: Input data contains negative values => log-plot not possible")
            #        plt_args.log_y = False
            #        yerr = error
            #    else:
            #        yerr = log_plot_error_bars( np.asarray(v_data), np.asarray(error) )
            #else:
            #    yerr = error

            yerr = error

            # make the plot
            fig = plt.figure()
            ax = fig.add_subplot(111)

            if plt_args.log_x and plt_args.log_y:
                ax.set_xscale("log", nonpositive = 'clip')
                ax.set_yscale("log", nonpositive = 'clip')
            elif plt_args.log_x and plt_args.log_y == False:
                ax.set_xscale("log", nonpositive = 'clip')
            elif plt_args.log_x == False and plt_args.log_y:
                ax.set_yscale("log", nonpositive = 'clip')
            else:
                pass

            if plt_args.curve_label != "":
                ax.errorbar(h_data, v_data, yerr, fmt = plt_args.marker, lw = plt_args.thick, ms = plt_args.msize, label = plt_args.curve_label)
                ax.legend(loc = 'best')    
            else:
                ax.errorbar(h_data, v_data, yerr, fmt = plt_args.marker, lw = plt_args.thick, ms = plt_args.msize)
                # to update this code with an error in x value plot
                #ax.errorbar(h_data, v_data, y_error, x_error, fmt = plt_args.marker, lw = plt_args.thick, ms = plt_args.msize)
            
            # for more on set_yscale see https://matplotlib.org/api/_as_gen/matplotlib.axes.Axes.set_yscale.html
            # Error bars with negative values will not be shown when plotted on a logarithmic axis.
            #if plt_args.log_y: ax.set_yscale('log')

            plt.xlabel(plt_args.x_label, fontsize = 14)
            plt.ylabel(plt_args.y_label, fontsize = 14)

            #if plt_args.log_y is False: plt.ticklabel_format(useOffset=False) # use this to turn off tick label scaling
            #ax.get_xaxis().get_major_formatter().set_scientific(False)
            # for more info on this see 
            # https://stackoverflow.com/questions/14711655/how-to-prevent-numbers-being-changed-to-exponential-form-in-python-matplotlib-fi

            # for more on yticks see 
            # https://matplotlib.org/api/pyplot_api.html?highlight=matplotlib%20pyplot%20yticks#matplotlib.pyplot.yticks
            if plt_args.y_tck_vals is not None and plt_args.y_tck_labs is not None:
                plt.yticks( plt_args.y_tck_vals, plt_args.y_tck_labs)
            
            if plt_args.plt_title != "": plt.title(plt_args.plt_title)
            if plt_args.plt_range is not None: plt.axis( plt_args.plt_range )

            # plot endmatter
            if plt_args.fig_name != "": plt.savefig(plt_args.fig_name)
            if plt_args.loud: plt.show()
            plt.clf()
            plt.cla()
            plt.close()
        else:
            raise Exception
    except Exception as e:
        print("\nError: Plotting.plot_single_curve_with_errors()")
        if c1 == False: print("h_data is not defined")
        if c2 == False: print("v_data is not defined")
        if c3 == False: print("h_data has no elements")
        if c4 == False: print("v_data has no elements")
        if c5 == False: print("h_data and v_data have different lengths")
        if c7 == False: print("e_low has no elements")
        if c8 == False: print("error and v_data have different lengths")
        print(e)

def plot_single_linear_fit_curve(h_data, v_data, plt_args):
    # plot a linear fit on the single data set with arguments supplied by plt_args
    # h_data is a list of length N
    # v_data is a list of length N
    # plt_args is an object with multiple data members, see class plot_arguments(object)
    # R. Sheehan 26 - 9 - 2017

    # .png is the default matplotlib format

    try:
        c1 = True if h_data is not None else False
        c2 = True if v_data is not None else False
        c3 = True if len(h_data) > 0 else False
        c4 = True if len(v_data) > 0 else False
        c5 = True if len(h_data) == len(v_data) else False
        c6 = True if c1 and c2 and c3 and c4 and c5 else False   

        if c6:
            # make the linear fit
            h_data, v_data = Common.sort_two_col(np.asarray(h_data), np.asarray(v_data))  
            pars = Common.linear_fit(np.asarray(h_data), np.asarray(v_data), [0, 1])

            if pars is not None:

                # print the fit parameters
                #print("Intercept: ",pars[0],", Slope: ",pars[1]); 

                lin_x = [ h_data[0], h_data[-1] ]
                lin_y = [ pars[0] + pars[1]*h_data[0], pars[0] + pars[1]*h_data[-1] ]

                #lin_x = [ np.asarray(h_data)[0], np.asarray(h_data)[-1] ]
                #lin_y = [ pars[0] + pars[1]*np.asarray(h_data)[0], pars[0] + pars[1]*np.asarray(h_data)[-1] ]

                # make the plot
                fig = plt.figure()
                ax = fig.add_subplot(111)
                
                ax.plot(lin_x, lin_y, 'r-', lw = plt_args.thick)
                ax.plot(h_data, v_data, 'b*', ms = plt_args.msize)
            
                # for more on set_yscale see https://matplotlib.org/api/_as_gen/matplotlib.axes.Axes.set_yscale.html
                if plt_args.log_y: ax.set_yscale('log')

                plt.xlabel(plt_args.x_label, fontsize = 14)
                plt.ylabel(plt_args.y_label, fontsize = 14)

                if plt_args.log_y is False: plt.ticklabel_format(useOffset=False) # use this to turn off tick label scaling
                #ax.get_xaxis().get_major_formatter().set_scientific(False)
                # for more info on this see 
                # https://stackoverflow.com/questions/14711655/how-to-prevent-numbers-being-changed-to-exponential-form-in-python-matplotlib-fi

                # for more on yticks see 
                # https://matplotlib.org/api/pyplot_api.html?highlight=matplotlib%20pyplot%20yticks#matplotlib.pyplot.yticks
                if plt_args.y_tck_vals is not None and plt_args.y_tck_labs is not None:
                    plt.yticks( plt_args.y_tck_vals, plt_args.y_tck_labs)
            
                if plt_args.plt_title != "": plt.title(plt_args.plt_title)
                if plt_args.plt_range is not None: plt.axis( plt_args.plt_range )

                # plot endmatter
                if plt_args.fig_name != "": plt.savefig(plt_args.fig_name)
                if plt_args.loud: plt.show()
                plt.clf()
                plt.cla()
                plt.close()
            else:
                raise Exception
        else:
            raise Exception
    except Exception as e:
        print("\nError: Plotting.plot_single_linear_fit_curve()")
        if c1 == False: print("h_data is not defined")
        if c2 == False: print("v_data is not defined")
        if c3 == False: print("h_data has no elements")
        if c4 == False: print("v_data has no elements")
        if c5 == False: print("h_data and v_data have different lengths")
        print(e)

def plot_single_linear_fit_curve_with_errors(h_data, v_data, error, plt_args):
    # plot a single data set with arguments supplied by plt_args
    # h_data is a list of length N
    # v_data is a list of length N
    # error is the difference between max and min values averaged about v_data, must have length N
    # a linear fit is made to the data set and included in the plot
    # plt_args is an object with multiple data members, see class plot_arg_single(plot_arguments)

    # matplotlib errorbar plot documentation
    #https://matplotlib.org/api/_as_gen/matplotlib.axes.Axes.errorbar.html

    # examples
    #https://matplotlib.org/1.2.1/examples/pylab_examples/errorbar_demo.html

    # R. Sheehan 9 - 11 - 2017

    # .png is the default matplotlib format

    try:
        c1 = True if h_data is not None else False
        c2 = True if v_data is not None else False
        c3 = True if len(h_data) > 0 else False
        c4 = True if len(v_data) > 0 else False
        c5 = True if len(h_data) == len(v_data) else False
        c7 = True if len(error) > 0 else False
        c8 = True if len(error) == len(v_data) else False
        c6 = True if c1 and c2 and c3 and c4 and c5 and c7 and c8 else False       

        if c6:
                       
            #if plt_args.log_y == True:
            #    if Common.list_has_negative(v_data):
            #        # data set contains negative values, cannot make log plot
            #        print("Error: Plotting.plot_single_curve_with_errors()")
            #        print("Error: Input data contains negative values => log-plot not possible")
            #        plt_args.log_y = False
            #        yerr = error
            #    else:
            #        yerr = log_plot_error_bars( np.asarray(v_data), np.asarray(error) )
            #else:
            #    yerr = error

            yerr = error

            # make the linear fit
            h_data, v_data = Common.sort_two_col(np.asarray(h_data), np.asarray(v_data))
            pars = Common.linear_fit(np.asarray(h_data), np.asarray(v_data), [0, 1])

            lin_x = [ h_data[0], h_data[-1] ]
            lin_y = [ pars[0] + pars[1]*h_data[0], pars[0] + pars[1]*h_data[-1] ]

            # make the plot
            fig = plt.figure()
            ax = fig.add_subplot(111)

            if plt_args.curve_label != "":
                ax.errorbar(h_data, v_data, yerr, fmt = 'b*', lw = plt_args.thick, ms = plt_args.msize, label = plt_args.curve_label)
                ax.legend(loc = 'best')    
            else:
                ax.errorbar(h_data, v_data, yerr, fmt = 'b*', lw = plt_args.thick, ms = plt_args.msize)
                # to update this code with an error in x value plot
                #ax.errorbar(h_data, v_data, y_error, x_error, fmt = plt_args.marker, lw = plt_args.thick, ms = plt_args.msize)

            ax.plot(lin_x, lin_y, 'r-', lw = plt_args.thick)
            
            # for more on set_yscale see https://matplotlib.org/api/_as_gen/matplotlib.axes.Axes.set_yscale.html
            # Error bars with negative values will not be shown when plotted on a logarithmic axis.
            #if plt_args.log_y: ax.set_yscale('log')

            plt.xlabel(plt_args.x_label, fontsize = 14)
            plt.ylabel(plt_args.y_label, fontsize = 14)

            #if plt_args.log_y is False: plt.ticklabel_format(useOffset=False) # use this to turn off tick label scaling
            #ax.get_xaxis().get_major_formatter().set_scientific(False)
            # for more info on this see 
            # https://stackoverflow.com/questions/14711655/how-to-prevent-numbers-being-changed-to-exponential-form-in-python-matplotlib-fi

            # for more on yticks see 
            # https://matplotlib.org/api/pyplot_api.html?highlight=matplotlib%20pyplot%20yticks#matplotlib.pyplot.yticks
            if plt_args.y_tck_vals is not None and plt_args.y_tck_labs is not None:
                plt.yticks( plt_args.y_tck_vals, plt_args.y_tck_labs)
            
            if plt_args.plt_title != "": plt.title(plt_args.plt_title)
            if plt_args.plt_range is not None: plt.axis( plt_args.plt_range )

            # plot endmatter
            if plt_args.fig_name != "": plt.savefig(plt_args.fig_name)
            if plt_args.loud: plt.show()
            plt.clf()
            plt.cla()
            plt.close()
        else:
            raise Exception
    except Exception as e:
        print("\nError: Plotting.plot_single_curve_with_errors()")
        if c1 == False: print("h_data is not defined")
        if c2 == False: print("v_data is not defined")
        if c3 == False: print("h_data has no elements")
        if c4 == False: print("v_data has no elements")
        if c5 == False: print("h_data and v_data have different lengths")
        if c7 == False: print("e_low has no elements")
        if c8 == False: print("error and v_data have different lengths")
        print(e)

def plot_histogram(the_data, plt_args):
    # make a histogram plot of the_data
    # no. bins used is computed automatically, no normalisation is applied
    # plt_args is the set of arguments to be used in the plot
    # no data processing is performed inside the method
    # R. Sheehan 29 - 11 - 2021
    
    try:
        c1 = True if the_data is not None else False
        c2 = True if len(the_data) > 0 else False
        c10 = True if c1 and c2 else False   

        if c10:
            plt.hist(the_data)
            plt.xlabel(plt_args.x_label, fontsize = 14)
            plt.ylabel(plt_args.y_label, fontsize = 14)

            if plt_args.plt_title != "": plt.title(plt_args.plt_title)            
            if plt_args.fig_name != "": plt.savefig(plt_args.fig_name)
            if plt_args.loud: plt.show()

            plt.clf()
            plt.cla()
            plt.close()
        else:
            raise Exception
    except Exception as e:
        print("\nError: Plotting.plot_histogram()")
        if c1 == False or c2 == False: print("the_data is not defined")
        print(e)

def plot_two_y_axis(h_data, v_data_1, v_data_2, plt_args):
    
    # Make a plot that includes two y_axes
    # For notes on this type of plot see https://matplotlib.org/gallery/api/two_scales.html
    # R. Sheehan 4 - 10 - 2019
    
    # To make a plot with two x-axes see
    # https://matplotlib.org/stable/gallery/subplots_axes_and_figures/secondary_axis.html
    # R. Sheehan 24 - 1 - 2024

    try:
        c1 = True if h_data is not None else False
        c2 = True if v_data_1 is not None else False
        c3 = True if v_data_2 is not None else False
        c4 = True if len(h_data) > 0 else False
        c5 = True if len(v_data_1) > 0 else False
        c6 = True if len(v_data_2) > 0 else False
        c7 = True if len(h_data) == len(v_data_1) else False
        c8 = True if len(h_data) == len(v_data_2) else False
        c10 = True if c1 and c2 and c3 and c4 and c5 else False

        if c10:
            fig, ax1 = plt.subplots()

            # same x-label for both graphs
            ax1.set_xlabel(plt_args.x_label, fontsize = 14)
            
            # set the colour of the ticks and labels on the 1st y-axis
            color = 'r'
            ax1.set_ylabel(plt_args.y_label, color=color, fontsize = 14)
            ax1.tick_params(axis='y', labelcolor=color)

            # plot the first data set
            ax1.plot(h_data, v_data_1, 'r*', lw = plt_args.thick, ms = plt_args.msize)
            
            ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

            # set the colour of the ticks and labels on the 2nd y-axis
            color = 'b'
            ax2.set_ylabel(plt_args.y_label_2, color=color, fontsize = 14)  # we already handled the x-label with ax1
            ax2.tick_params(axis='y', labelcolor=color)

            # plot the second data set
            ax2.plot(h_data, v_data_2, 'b^', lw = plt_args.thick, ms = plt_args.msize)
            
            fig.tight_layout()  # otherwise the right y-label is slightly clipped

            # add a plot title if required
            if plt_args.plt_title != "": plt.title(plt_args.plt_title)
            
            # just use default plot range
            #if plt_args.plt_range is not None: plt.axis( plt_args.plt_range )

            # plot endmatter
            if plt_args.fig_name != "": plt.savefig(plt_args.fig_name)
            if plt_args.loud: plt.show()
            plt.clf()
            plt.cla()
            plt.close()
        else:
            raise Exception
    except Exception as e:
        print("\nError: Plotting.plot_two_axis()")
        if c1 == False: print("h_data is not defined")
        if c2 == False: print("v_data_1 is not defined")
        if c3 == False: print("v_data_2 is not defined")
        if c4 == False: print("h_data has no elements")
        if c5 == False: print("v_data_1 has no elements")
        if c6 == False: print("v_data_2 has no elements")
        if c7 == False or c8 == False: print("h_data and v_data have different lengths")
        print(e)

def plot_two_x_axis(hv_data, plt_args):

    # generate a plot with two different x-axis scales
    # https://matplotlib.org/stable/gallery/subplots_axes_and_figures/secondary_axis.html
    # this is the standard plot_multiple_curves with a second x-axis added on top of the frame
    # also I've removed the ability to do loglog plots, only plot log along y for simplicity
    # R. Sheehan 25 - 1 - 2024

    # this works as long as the mapping from one scale to another is linear
    # otherwise it does not work as well as you'd like

    # generate plot that contains multiple curves on the same axis
    # It is assumed that each data set shares the same horizontal coordinates
    # hv_data is a 2D array of size M*N
    # data is stored row-wise in => data is accesed by subscript operation on hv_data
    # M is the number of curves to be plotted
    # N is the number of data points in each set
    # plt_args is an object that contains multiple data members, see class plot_arguments(object)
    # It is assumed that plt_args.crv_lab_list and plt_args.mrk_list[k] are not empty

    # .png is the default matplotlib format

    try:
        c1 = True if hv_data is not None else False
        c2 = True if plt_args.crv_lab_list is not None else False        
        c3 = True if plt_args.mrk_list is not None else False
        c4 = True if len(plt_args.crv_lab_list) == len(hv_data) else False
        c5 = True if len(plt_args.mrk_list) == len(hv_data) else False
        c6 = True if c1 and c2 and c3 and c4 and c5 else False

        if c6:
            
            from matplotlib.ticker import AutoMinorLocator
            
            # make the plot
            fig = plt.figure()
            ax = fig.add_subplot(111)

            for k in range(0, len(hv_data), 1):
                if plt_args.log_x == False and plt_args.log_y:
                    ax.semilogy(hv_data[k][0], hv_data[k][1], plt_args.mrk_list[k], lw = plt_args.thick, ms = plt_args.msize, label = plt_args.crv_lab_list[k])
                else:
                    ax.plot(hv_data[k][0], hv_data[k][1], plt_args.mrk_list[k], lw = plt_args.thick, ms = plt_args.msize, label = plt_args.crv_lab_list[k])
                
            if plt_args.show_leg: ax.legend(loc = 'best')
            
            plt.xlabel(plt_args.x_label, fontsize = 14)
            plt.ylabel(plt_args.y_label, fontsize = 14)

            #if plt_args.log_y is False: plt.ticklabel_format(useOffset=False) # use this to turn off tick label scaling
            #ax.get_xaxis().get_major_formatter().set_scientific(False)
            # for more info on this see 
            # https://stackoverflow.com/questions/14711655/how-to-prevent-numbers-being-changed-to-exponential-form-in-python-matplotlib-fi
            
            if plt_args.plt_title != "": plt.title(plt_args.plt_title)
            if plt_args.plt_range is not None: plt.axis( plt_args.plt_range )

            # Code needed to add second axis scale to frame
            #def forward(x):
            #    return np.interp(x, plt_args.xold, plt_args.xnew)

            #def inverse(x):
            #    return np.interp(x, plt_args.xnew, plt_args.xold)

            # have to define functions to map one scale onto another
            def fbeat2dist(x):
                return 0.125*x; # maps fbeat onto looplength for Lf = 10km

            def dist2fbeat(x):
                return 8*x; # maps looplength onto distance for Lf = 10km

            #def fbeat2dist(x):
            #    return 0.625*x; # maps fbeat onto looplength for Lf = 50km

            #def dist2fbeat(x):
            #    return 1.6*x; # maps looplength onto distance for Lf = 50km

            secax = ax.secondary_xaxis('top', functions=(fbeat2dist, dist2fbeat))
            secax.xaxis.set_minor_locator(AutoMinorLocator())
            secax.set_xlabel(plt_args.x_label_2)

            # plot endmatter
            if plt_args.fig_name != "": plt.savefig(plt_args.fig_name)
            if plt_args.loud: plt.show()
            plt.clf()
            plt.cla()
            plt.close()
        else:
            raise Exception
    except Exception as e:
        print("Error: Plotting.plot_multiple_curves()")
        if c1 == False: print("hv_data has not been assigned correctly")
        if c2 == False: print("plt_args.crv_lab_list has not been assigned correctly")
        if c3 == False: print("plt_args.mrk_list has not been assigned correctly")
        if c4 == False: print("hv_data and plt_args.crv_lab_list have differing numbers of elements")
        if c5 == False: print("hv_data and plt_args.mrk_list have differing numbers of elements")
        print(e)

def plot_multiple_curves(hv_data, plt_args):
    # generate plot that contains multiple curves on the same axis
    # It is assumed that each data set shares the same horizontal coordinates
    # hv_data is a 2D array of size M*N
    # data is stored row-wise in => data is accesed by subscript operation on hv_data
    # M is the number of curves to be plotted
    # N is the number of data points in each set
    # plt_args is an object that contains multiple data members, see class plot_arguments(object)
    # It is assumed that plt_args.crv_lab_list and plt_args.mrk_list[k] are not empty

    # I would like a method which could have multiple curves but only want a small number of the curves are to have a legend
    # Assume that the last k < M curves in hv_data are to have a legend label
    # See here for details on how this is implemented
    # https://matplotlib.org/stable/gallery/text_labels_and_annotations/legend_demo.html#sphx-glr-gallery-text-labels-and-annotations-legend-demo-py
    # I don't think I can do this in a generic manner because the legend wants you to save the lines as elements of a tuple
    # Don't know how to do this when you don't know the size of the tuple in advance
    # Updated R. Sheehan 25 - 1 - 2024

    # .png is the default matplotlib format

    try:
        c1 = True if hv_data is not None else False
        c2 = True if plt_args.crv_lab_list is not None else False        
        c3 = True if plt_args.mrk_list is not None else False
        c4 = True if len(plt_args.crv_lab_list) == len(hv_data) else False
        c5 = True if len(plt_args.mrk_list) == len(hv_data) else False
        c6 = True if c1 and c2 and c3 and c4 and c5 else False

        if c6:
            # check that all data for plotting is positive
            #if plt_args.log_y == True:
            #    for k in range(0, len(hv_data), 1):
            #        if Common.list_has_negative(hv_data[k][1]):
            #            plt_args.log_y = False

            # make the plot
            fig = plt.figure()
            ax = fig.add_subplot(111)

            for k in range(0, len(hv_data), 1):
                if plt_args.log_x and plt_args.log_y:
                    ax.loglog(hv_data[k][0], hv_data[k][1], plt_args.mrk_list[k], lw = plt_args.thick, ms = plt_args.msize, label = plt_args.crv_lab_list[k])
                elif plt_args.log_x and plt_args.log_y == False:
                    ax.semilogx(hv_data[k][0], hv_data[k][1], plt_args.mrk_list[k], lw = plt_args.thick, ms = plt_args.msize, label = plt_args.crv_lab_list[k])
                elif plt_args.log_x == False and plt_args.log_y:
                    ax.semilogy(hv_data[k][0], hv_data[k][1], plt_args.mrk_list[k], lw = plt_args.thick, ms = plt_args.msize, label = plt_args.crv_lab_list[k])
                else:
                    ax.plot(hv_data[k][0], hv_data[k][1], plt_args.mrk_list[k], lw = plt_args.thick, ms = plt_args.msize, label = plt_args.crv_lab_list[k])
                
            if plt_args.show_leg: ax.legend(loc = 'best')
            
            #if plt_args.log_y: ax.set_yscale('log') 

            plt.xlabel(plt_args.x_label, fontsize = 14)
            plt.ylabel(plt_args.y_label, fontsize = 14)

            #if plt_args.log_y is False: plt.ticklabel_format(useOffset=False) # use this to turn off tick label scaling
            #ax.get_xaxis().get_major_formatter().set_scientific(False)
            # for more info on this see 
            # https://stackoverflow.com/questions/14711655/how-to-prevent-numbers-being-changed-to-exponential-form-in-python-matplotlib-fi
            
            if plt_args.plt_title != "": plt.title(plt_args.plt_title)
            if plt_args.plt_range is not None: plt.axis( plt_args.plt_range )

            # plot endmatter
            if plt_args.fig_name != "": plt.savefig(plt_args.fig_name)
            if plt_args.loud: plt.show()
            plt.clf()
            plt.cla()
            plt.close()
        else:
            raise Exception
    except Exception as e:
        print("Error: Plotting.plot_multiple_curves()")
        if c1 == False: print("hv_data has not been assigned correctly")
        if c2 == False: print("plt_args.crv_lab_list has not been assigned correctly")
        if c3 == False: print("plt_args.mrk_list has not been assigned correctly")
        if c4 == False: print("hv_data and plt_args.crv_lab_list have differing numbers of elements")
        if c5 == False: print("hv_data and plt_args.mrk_list have differing numbers of elements")
        print(e)

def plot_multiple_curves_with_errors(hv_data, plt_args):
    # generate plot that contains multiple curves on the same axis
    # It is assumed that each data set shares the same horizontal coordinates
    # hv_data is a 2D array of size M*N
    # data is stored row-wise in => data is accesed by subscript operation on hv_data
    # M is the number of curves to be plotted
    # N is the number of data points in each set
    # plt_args is an object that contains multiple data members, see class plot_arguments(object)
    # It is assumed that plt_args.crv_lab_list and plt_args.mrk_list[k] are not empty

    # .png is the default matplotlib format

    try:
        c1 = True if hv_data is not None else False
        c2 = True if plt_args.crv_lab_list is not None else False        
        c3 = True if plt_args.mrk_list is not None else False
        c4 = True if len(plt_args.crv_lab_list) == len(hv_data) else False
        c5 = True if len(plt_args.mrk_list) == len(hv_data) else False
        c6 = True if c1 and c2 and c3 and c4 and c5 else False

        if c6:
            # check that all data for plotting is positive
            if plt_args.log_y == True:
                for k in range(0, len(hv_data), 1):
                    if Common.list_has_negative(hv_data[k][1]):
                        plt_args.log_y = False

            # make the plot
            fig = plt.figure()
            ax = fig.add_subplot(111)

            for k in range(0, len(hv_data), 1):
                ax.errorbar(hv_data[k][0], hv_data[k][1], yerr = hv_data[k][2] if plt_args.log_y == False else log_plot_error_bars( np.asarray(hv_data[k][1]), np.asarray(hv_data[k][2]) ), 
                        fmt = plt_args.mrk_list[k], lw = plt_args.thick, ms = plt_args.msize, 
                        label = plt_args.crv_lab_list[k])
                
            if plt_args.show_leg: ax.legend(loc = 'best')
            
            if plt_args.log_y: ax.set_yscale('log') 

            plt.xlabel(plt_args.x_label, fontsize = 14)
            plt.ylabel(plt_args.y_label, fontsize = 14)

            if plt_args.log_y is False: plt.ticklabel_format(useOffset=False) # use this to turn off tick label scaling
            #ax.get_xaxis().get_major_formatter().set_scientific(False)
            # for more info on this see 
            # https://stackoverflow.com/questions/14711655/how-to-prevent-numbers-being-changed-to-exponential-form-in-python-matplotlib-fi
            
            if plt_args.plt_title != "": plt.title(plt_args.plt_title)
            if plt_args.plt_range is not None: plt.axis( plt_args.plt_range )

            # plot endmatter
            if plt_args.fig_name != "": plt.savefig(plt_args.fig_name)
            if plt_args.loud: plt.show()
            plt.clf()
            plt.cla()
            plt.close()
        else:
            raise Exception
    except Exception as e:
        print("Error: Plotting.plot_multiple_curves()")
        if c1 == False: print("hv_data has not been assigned correctly")
        if c2 == False: print("plt_args.crv_lab_list has not been assigned correctly")
        if c3 == False: print("plt_args.mrk_list has not been assigned correctly")
        if c4 == False: print("hv_data and plt_args.crv_lab_list have differing numbers of elements")
        if c5 == False: print("hv_data and plt_args.mrk_list have differing numbers of elements")
        print(e)

def plot_multiple_linear_fit_curves(hv_data, plt_args):
    # generate plot that contains multiple linear fits to data on the same axis
    # It is assumed that each data set shares the same horizontal coordinates
    # hv_data is a 2D array of size M*N
    # data is stored row-wise in => data is accesed by subscript operation on hv_data
    # M is the number of curves to be plotted
    # N is the number of data points in each set
    # plt_args is an object that contains multiple data members, see class plot_arguments(object)
    # It is assumed that plt_args.crv_lab_list and plt_args.mrk_list[k] are not empty

    # .png is the default matplotlib format

    try:
        c1 = True if hv_data is not None else False
        c2 = True if plt_args.crv_lab_list is not None else False        
        #c3 = True if plt_args.mrk_list is not None else False
        c4 = True if len(plt_args.crv_lab_list) == len(hv_data) else False
        #c5 = True if len(plt_args.mrk_list) == len(hv_data) else False # not using mrk_list in this function
        c6 = True if c1 and c2 and c4 else False

        if c6:
            # make the plot
            fig = plt.figure()
            ax = fig.add_subplot(111)

            count = 0
            for k in range(0, len(hv_data), 1):

                # sort the data set, this doesn't affect the fit in any way
                # it just means that the line in the final plot always hits the endpoints
                # R. Sheehan 9 - 7 - 2021
                hv_data[k][0], hv_data[k][1] = Common.sort_two_col(hv_data[k][0], hv_data[k][1])  

                pars = Common.linear_fit(np.asarray(hv_data[k][0]), np.asarray(hv_data[k][1]), [0, 1]) # perform linear fit to the data set

                if pars is not None:

                    #print(plt_args.crv_lab_list[k]," , ",pars[0]," , ",pars[1])

                    lin_x = [ hv_data[k][0][0], hv_data[k][0][-1] ]
                    lin_y = [ pars[0] + pars[1]*hv_data[k][0][0], pars[0] + pars[1]*hv_data[k][0][-1] ]

                    # line is to be given a solid line
                    # why should this be the case?
                    # labs_line_only, labs_mrk_only
                    ax.plot(lin_x, lin_y, labs_lins[count], lw = plt_args.thick, ms = plt_args.msize, label = plt_args.crv_lab_list[k])
                    #ax.plot(lin_x, lin_y, labs_line_only[count], lw = plt_args.thick, ms = plt_args.msize, label = plt_args.crv_lab_list[k])

                    # points are given marker of same colour
                    ax.plot(hv_data[k][0], hv_data[k][1], labs_pts[count], lw = plt_args.thick, ms = plt_args.msize)
                    #ax.plot(hv_data[k][0], hv_data[k][1], labs_mrk_only[count], lw = plt_args.thick, ms = plt_args.msize)
                else:
                    raise Exception

                count = (count + 1)%len(labs_lins) # best way to step through the plt marker data
                
            if plt_args.show_leg: ax.legend(loc = 'best')

            plt.xlabel(plt_args.x_label, fontsize = 14)
            plt.ylabel(plt_args.y_label, fontsize = 14)

            plt.ticklabel_format(useOffset=False) # use this to turn off tick label scaling
            #ax.get_xaxis().get_major_formatter().set_scientific(False)
            # for more info on this see 
            # https://stackoverflow.com/questions/14711655/how-to-prevent-numbers-being-changed-to-exponential-form-in-python-matplotlib-fi
            
            if plt_args.plt_title != "": plt.title(plt_args.plt_title)
            if plt_args.plt_range is not None: plt.axis( plt_args.plt_range )

            # for more on yticks see 
            # https://matplotlib.org/api/pyplot_api.html?highlight=matplotlib%20pyplot%20yticks#matplotlib.pyplot.yticks
            if plt_args.y_tck_vals is not None and plt_args.y_tck_labs is not None:
                plt.yticks( plt_args.y_tck_vals, plt_args.y_tck_labs)

            # plot endmatter
            if plt_args.fig_name != "": plt.savefig(plt_args.fig_name)
            if plt_args.loud: plt.show()
            plt.clf()
            plt.cla()
            plt.close()
        else:
            raise Exception
    except Exception as e:
        print("Error: Plotting.plot_multiple_linear_fit_curves()")
        if c1 == False: print("hv_data has not been assigned correctly")
        if c2 == False: print("plt_args.crv_lab_list has not been assigned correctly")
        #if c3 == False: print("plt_args.mrk_list has not been assigned correctly")
        if c4 == False: print("hv_data and plt_args.crv_lab_list have differing numbers of elements")
        #if c5 == False: print("hv_data and plt_args.mrk_list have differing numbers of elements")
        print(e)
