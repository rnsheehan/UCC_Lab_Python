# UCC_Lab_Python
 Repository for UCC UG Lab Data Analysis and Hardware Automation


## Using UCC_Lab_Python via WSL
WSL (Windows subroutine for Linux) is capable of interfacing with the IBM4 but requires a change to the set up. In the first instance it is __recommended__ that you do **not** run your IBM4 through WSL and instead revert to the windows installation however if you wish there are work arounds.

  1. Install packages documented in ``Python_Package_Install.bat`` through **WSL**. 
  2. Install the python package com2tty to the **windows** partition via:
  ``py -m install com2tty``
  3. Plug in the IBM4 and run ``py -m com2tty`` through powershell / command prompt.
  4. Attach the IBM4 COM port

You will need to clone this repository not the original as there is some changes to the ``IBM4_Lib.py`` file 