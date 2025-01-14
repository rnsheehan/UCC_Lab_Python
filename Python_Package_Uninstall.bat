:: Script for uninstalling multiple useful python packages via command line
:: script assumes python version 3.12.3
:: for older versions of python replace the command py with python
:: R. Sheehan 14 - 1 - 2024

py --version
py -m pip uninstall --yes numpy
py -m pip uninstall --yes scipy
py -m pip uninstall --yes matplotlib
py -m pip uninstall --yes scikit-learn
py -m pip uninstall --yes pandas
py -m pip uninstall --yes serial
py -m pip uninstall --yes pyserial
py -m pip uninstall --yes pyvisa
echo "Package Uninstallation Complete"
