"""
Script for running the Methods from Plotting_Examples.py
Uncomment the method you would like to test

R. Sheehan 19 - 9 - 2024
"""

import os
import Plotting_Examples

# Where are you? 
pwd = os.getcwd()

print(pwd)

# 0. Method for Generating Synthetic Data
#Plotting_Examples.Generate_Synthetic_Data(5, True, True)

# 1. Plot showing single data set
#Plotting_Examples.Single_Data_Set()

# 2. Plot showing single data set with error bars
#Plotting_Examples.Single_Data_Set_With_Errors()

# 3. Plot showing linear fit to single data set
#Plotting_Examples.Single_Data_Set_Linear_Fit()

# 4. Plot showing linear fit to single data set including error bars
#Plotting_Examples.Single_Data_Set_Linear_Fit_With_Errors()

# 5. Plot showing multiple data sets
#Plotting_Examples.Multiple_Data_Set()

# 6. Plot showing multiple data sets with error bars
#Plotting_Examples.Multiple_Data_Set_With_Errors()

# 7. Plot showing linear fit to multiple data sets
Plotting_Examples.Multiple_Data_Set_Linear_Fit()

# 8. Plot showing multiple data sets with imported data
#Plotting_Examples.Multiple_Data_Set_Imported()