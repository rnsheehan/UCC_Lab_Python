"""
Methods for testing the operation of the IBM4 Serial Controller Class

0. Basic Find, Open, Close
1. Step through voltages
2. Basic single channel sweep
3. Read all input channels
4. Differential read
5. Multi-reads and timings
6. Multimeter mode
7. Linear single channel sweep

R. Sheehan 12 - 6 - 2024
"""

import time
import numpy
import Sweep_Interval
import IBM4_Lib

MOD_NAME_STR = "Control_Examples"

def Simple_Open_Close():
    """
    See if an IBM4 is connected to the PC, if so, open it and then close it
    """
    
    FUNC_NAME = ".Simple_Open_Close()"
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        # instantiate an object that interfaces with the IBM4
        the_dev = IBM4_Lib.Ser_Iface() # find the first connected IBM4, open in DC mode by default
        
        #the_dev = IBM4_Lib.Ser_Iface(read_mode = 'AC') # find the first connected IBM4, open in DC mode
        
        #the_dev = IBM4_Lib.Ser_Iface(read_mode = 'AC') # find the first connected IBM4, open in AC mode
        
        #the_dev = IBM4_Lib.Ser_Iface('COM3', read_mode='AC') # connect to a named IBM4, open in AC mode

        print("IBM4 IDN string:", the_dev.IdentifyIBM4() )

        del the_dev # destructor for the IBM4 object, closes comms
    except Exception as e:
        print(ERR_STATEMENT)
        print(e)

def Step_Through_Voltages():
    """
    Connect to an IBM4, output voltage from a channel, increase that voltage, make a reading
    """
    
    FUNC_NAME = ".Step_Through_Voltages()"
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        # instantiate an object that interfaces with the IBM4
        the_dev = IBM4_Lib.Ser_Iface() # find the first connected IBM4, open in DC mode by default
        
        output_ch = 'A1' # select the voltage output channel either A0 or A1
        input_ch = 'A2' # select the voltage input channel A2, A3, A4, A5, D2

        print("Analog Output Steps + Averaged Read on Single Channel")
        print("Analog Out:",output_ch)
        print("Analog In:",input_ch)   

        volt_val = 1.0
        the_dev.WriteVoltage(output_ch, volt_val)
        time.sleep(1)

        volt_val = 1.5
        the_dev.WriteVoltage(output_ch, volt_val)
        time.sleep(1)

        volt_val = 2.0
        the_dev.WriteVoltage(output_ch, volt_val)
        time.sleep(1)

        volt_val = 1.7
        the_dev.WriteVoltage(output_ch, volt_val)
        time.sleep(1)

        volt_val = 0.7
        the_dev.WriteVoltage(output_ch, volt_val)
        time.sleep(1)

        avg_val = the_dev.ReadAverageVoltage(input_ch, no_reads = 10, loud = False)
        print("Set voltage value = ",volt_val)
        print("Recorded average voltage = ",avg_val)

        del the_dev # destructor for the IBM4 object, closes comms
    except Exception as e:
        print(ERR_STATEMENT)
        print(e)

def Simple_Sweep():
    """
    Perform simple sweep and read on a single channel
    """
    
    FUNC_NAME = ".Simple_Sweep()"
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        # instantiate an object that interfaces with the IBM4
        the_dev = IBM4_Lib.Ser_Iface() # find the first connected IBM4, open in DC mode by default
        
        output_ch = 'A1' # select the voltage output channel either A0 or A1
        input_ch = 'A2' # select the voltage input channel A2, A3, A4, A5, D2
        Nreads = 11 # no. readinngs at each channel
        volts = numpy.arange(0, 3.1, 1)

        print("Analog Output Sweep + Averaged Read on Single Channel")
        print("Analog Out:",output_ch)
        print("Analog In:",input_ch)
        
        start = time.time()
        for v in volts:
            the_dev.WriteVoltage(output_ch, v)
            reading = the_dev.ReadAverageVoltage(input_ch, Nreads)
            print('Vset:',v,', Vread: ',reading)
        end = time.time()
        deltaT = end-start
        readsTot = len(volts)*Nreads
        measT = deltaT/(float(readsTot))
        SR = 1.0/measT
        print("%(v1)d measurements performed in %(v2)0.3f seconds => SR = %(v3)0.3f Hz"%{"v1":readsTot, "v2":deltaT, "v3":SR})

        del the_dev # destructor for the IBM4 object, closes comms
    except Exception as e:
        print(ERR_STATEMENT)
        print(e)

def Simple_Sweep_Read_All():
    """
    Perform simple sweep and read on all input channel
    """
    
    FUNC_NAME = ".Simple_Sweep_Read_All()"
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        # instantiate an object that interfaces with the IBM4
        the_dev = IBM4_Lib.Ser_Iface() # find the first connected IBM4, open in DC mode by default
        
        output_ch = 'A1' # select the voltage output channel either A0 or A1
        Nreads = 11 # no. readinngs at each channel
        NAI = 5 # no. analog input channels
        volts = numpy.arange(0, 3.1, 0.5)

        print("Analog Output Sweep + Averaged Read on All Channels")
        print("Analog Out:",output_ch)

        start = time.time()
        for v in volts:
            the_dev.WriteVoltage(output_ch, v)
            readings = the_dev.ReadAverageVoltageAllChnnl(Nreads)
            print('Vset:',v,', Vread: ',readings)
        end = time.time()
        deltaT = end-start
        readsTot = len(volts)*Nreads*NAI
        measT = deltaT/(float(readsTot))
        SR = 1.0/measT
        print("%(v1)d measurements performed in %(v2)0.3f seconds => SR = %(v3)0.3f Hz"%{"v1":readsTot, "v2":deltaT, "v3":SR})

        del the_dev # destructor for the IBM4 object, closes comms
    except Exception as e:
        print(ERR_STATEMENT)
        print(e)

def Differential_Readings():
    """
    Perform differential reads between different pairs of channels
    use the overloaded DifferentialRead Method to obtain an averaged reading

    the user must be careful when using overloaded methods
    python allows for different return types and different numbers of returned elements
    what is not forbidden is permitted and exploited
    """
    
    FUNC_NAME = ".Differential_Readings()"
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        # instantiate an object that interfaces with the IBM4
        the_dev = IBM4_Lib.Ser_Iface() # find the first connected IBM4, open in DC mode by default
        
        # this assumes that you are reading the voltage across a resistor and diode in series
        # A2 set to Vin, A3 between the resistor and the diode, A4 at GND
        Nreads = 237
        Rval = 10.0 / 1000.0 # sense resistance in kOhm
        Vset = 2.25
        output_ch = 'A0' # select the voltage output channel either A0 or A1

        print("Differential Reads on Different Analog Inputs")
        print("Analog Out: ",output_ch)
        
        the_dev.WriteVoltage(output_ch, Vset)
        the_dev.ResetBuffer()
        time.sleep(1) # give it some time to settle

        vals = the_dev.DifferentialRead('A2', 'A4', 'Multiple Voltage', Nreads)
        print("Vhi: A2, Vlo: A4")
        print("Set Voltage: %(v1)0.3f +/- %(v2)0.3f (V)"%{"v1":vals[0],"v2":vals[1]})

        vals = the_dev.DifferentialRead('A2', 'A3', 'Multiple Voltage', Nreads)
        print("Vhi: A2, Vlo: A3")
        print("Sense Voltage: %(v1)0.3f +/- %(v2)0.3f (V)"%{"v1":vals[0],"v2":vals[1]})
        print("Sense Current: %(v1)0.1f +/- %(v2)0.1f (mA)"%{"v1":vals[0]/Rval,"v2":vals[1]/Rval})
        
        vals = the_dev.DifferentialRead('A3', 'A4', 'Multiple Voltage', Nreads)
        print("Vhi: A3, Vlo: A4")
        print("Diode Voltage: %(v1)0.3f +/- %(v2)0.3f (V)"%{"v1":vals[0],"v2":vals[1]})
        
        del the_dev # destructor for the IBM4 object, closes comms
    except Exception as e:
        print(ERR_STATEMENT)
        print(e)

def Multiple_Readings():
    """
    Perform multiple readsings by different methods
    use the overloaded ReadVoltage Method to obtain an averaged reading

    the user must be careful when using overloaded methods
    python allows for different return types and different numbers of returned elements
    what is not forbidden is permitted and exploited
    """
    
    FUNC_NAME = ".Multiple_Readings()"
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        # instantiate an object that interfaces with the IBM4
        the_dev = IBM4_Lib.Ser_Iface() # find the first connected IBM4, open in DC mode by default
        
        # can compare the timing of each of the different measurement types
        # https://stackoverflow.com/questions/7370801/how-do-i-measure-elapsed-time-in-python
        # ReadAverageVoltage is slightly faster than ReadAverageVoltageMultiple
        # which is weird considering that ReadAverageVoltage has to do extra processing on chip
        # Sample Rate for IBM4 is variable, as we know and find annoying
        # Can see that nothing wrong with timing of ReadAverageVoltageAllChnnl
        # Execution of ReadAverageVoltageAllChnnl takes ~ 5 ReadAverageVoltage which makes sense really
        # since ReadAverageVoltageAllChnnl consists of 5 calls to ReadAverageVoltage
        # R. Sheehan 9 - 7 - 2024

        Nreads = 501
        Vset = 1.5
        output_ch = 'A0'
        the_dev.WriteVoltage(output_ch,Vset)
        the_dev.ResetBuffer()
        time.sleep(1)

        print("Multiple Reads by Different Methods - Test the Overloaded ReadVoltage method")
        print("Analog Out:",output_ch)
        print("Vset =",Vset,"(V)")

        # time the measurement
        start = time.time()
        #avg, err, vals = the_dev.ReadMultipleVoltage('A3', Nreads)
        avg, err, vals = the_dev.ReadVoltage('A3', 'Multiple Voltage', Nreads)
        end = time.time()
        deltaT = end-start
        measT = deltaT/(float(Nreads))
        SR = 1.0/measT
        print("Analog Input: A3, Read Method: Multiple Voltage => ReadMultipleVoltage")
        print("%(v1)d measurements performed in %(v2)0.3f seconds"%{"v1":Nreads, "v2":deltaT})
        print("%(v1)0.4f secs / measurement"%{"v1":measT})
        print("Sample Rate: %(v1)0.2f Hz"%{"v1":SR })
        print("Measured Voltage: %(v1)0.3f +/- %(v2)0.3f (V)"%{"v1":avg,"v2":err})

        start = time.time()
        #val = the_dev.ReadAverageVoltage('A3',Nreads)
        val = the_dev.ReadVoltage('A3','Average Voltage', Nreads)
        end = time.time()
        deltaT = end-start
        measT = deltaT/(float(Nreads))
        SR = 1.0/measT
        print("Analog Input: A3, Read Method: Average Voltage => ReadAverageVoltage")
        print("\n%(v1)d measurements performed in %(v2)0.3f seconds"%{"v1":Nreads, "v2":deltaT})
        print("%(v1)0.4f secs / measurement"%{"v1":measT})
        print("Sample Rate: %(v1)0.2f Hz"%{"v1":SR })
        print("Measured Voltage: %(v1)0.3f (V)"%{"v1":val})

        start = time.time()
        val = the_dev.ReadAverageVoltageAllChnnl(Nreads)
        end = time.time()
        deltaT = end-start
        measT = deltaT/(float(Nreads*5))
        SR = 1.0/measT
        print("Analog Input: All, Read Method: ReadAverageVoltageAllChnnl")
        print("\n%(v1)d measurements performed in %(v2)0.3f seconds"%{"v1":Nreads*5, "v2":deltaT})
        print("%(v1)0.4f secs / measurement"%{"v1":measT})
        print("Sample Rate: %(v1)0.2f Hz"%{"v1":SR})
        print("Measured Voltages: ", val)
        print("\nSR from each Read method are comparable")

        del the_dev # destructor for the IBM4 object, closes comms
    except Exception as e:
        print(ERR_STATEMENT)
        print(e)

def Multimeter_Mode():
    """
    Run the IBM4 in multimeter mode
    """
    
    FUNC_NAME = ".Multimeter_Mode()"
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        # instantiate an object that interfaces with the IBM4
        the_dev = IBM4_Lib.Ser_Iface() # find the first connected IBM4, open in DC mode by default

        the_dev.MultimeterMode() # I rock
       
        del the_dev # destructor for the IBM4 object, closes comms
    except Exception as e:
        print(ERR_STATEMENT)
        print(e)

def Linear_Sweep_V1():
    """
    Perform a linear sweep on chosen channels
    """
    
    FUNC_NAME = ".Linear_Sweep_V1()"
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        # instantiate an object that interfaces with the IBM4
        the_dev = IBM4_Lib.Ser_Iface() # find the first connected IBM4, open in DC mode by default

        # instantiate an object to keep track of the sweep space parameters
        no_steps = 10
        v_start = 0.0
        v_end = 3.3
        v_fixed = 1.0

        # A1 will sweep while A0 will be kept constant at v_fixed
        # I wonder what that could be used for? 
        sweep_data = the_dev.SingleChannelSweepA('A1', v_start, v_end, no_steps, v_fixed) # use channel A1 to sweep over the voltage interval

        print('Measured data')
        print(sweep_data)
       
        del the_dev # destructor for the IBM4 object, closes comms
    except Exception as e:
        print(ERR_STATEMENT)
        print(e)

def Linear_Sweep_V2():
    """
    Perform a linear sweep on chosen channels
    """
    
    FUNC_NAME = ".Linear_Sweep_V2()"
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        # instantiate an object that interfaces with the IBM4
        the_dev = IBM4_Lib.Ser_Iface() # find the first connected IBM4, open in DC mode by default

        # instantiate an object to keep track of the sweep space parameters
        no_steps = 10
        v_start = 0.0
        v_end = 3.3
        the_interval = Sweep_Interval.SweepSpace(no_steps, v_start, v_end)

        # A0 will sweep while A1 will be kept constant at v_fixed
        # I wonder what that could be used for? 
        sweep_data = the_dev.SingleChannelSweepB('A0', the_interval, v_fixed = 0.0) # use channel A1 to sweep over the voltage interval

        print('Measured data')
        print(sweep_data)
       
        del the_dev # destructor for the IBM4 object, closes comms
    except Exception as e:
        print(ERR_STATEMENT)
        print(e)

