:: Script for upgrading multiple useful python packages via command line
:: script assumes python version 3.12.3
:: for older versions of python replace the command py with python
:: R. Sheehan 28 - 5 - 2024

py --version
py -m pip install --upgrade numpy
py -m pip install --upgrade scipy
py -m pip install --upgrade matplotlib
py -m pip install --upgrade scikit-learn
py -m pip install --upgrade pandas
py -m pip install --upgrade pyserial
py -m pip install --upgrade pyvisa
echo "Package Upgrade Complete"
