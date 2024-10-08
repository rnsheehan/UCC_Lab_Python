"""
Script for running the Methods from Control_Examples.py
Uncomment the method you would like to test

R. Sheehan 19 - 9 - 2024
"""

import os
import Control_Examples

# Where are you? 
pwd = os.getcwd()

print(pwd)

# 0. Basic Find, Open, Close
#Control_Examples.Simple_Open_Close()

# 1. Step through voltages
#Control_Examples.Step_Through_Voltages()

# 2. Basic single channel sweep
#Control_Examples.Simple_Sweep()

# 3. Read all input channels
#Control_Examples.Simple_Sweep_Read_All()

# 4. Differential read
#Control_Examples.Differential_Readings()

# 5. Multi-reads and timings
#Control_Examples.Multiple_Readings()

# 6. Multimeter mode
Control_Examples.Multimeter_Mode()

# 7. Linear single channel sweep
#Control_Examples.Linear_Sweep_V1()
#Control_Examples.Linear_Sweep_V2()