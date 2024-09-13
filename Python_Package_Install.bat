:: Script for installing multiple useful python packages via command line
:: script assumes python version 3.12.3
:: for older versions of python replace the command py with python
:: R. Sheehan 28 - 5 - 2024

py --version
py -m pip install numpy
py -m pip install scipy
py -m pip install matplotlib
py -m pip install scikit-learn
py -m pip install pandas
py -m pip install pyserial
py -m pip install pyvisa
echo "Package Installation Complete"
