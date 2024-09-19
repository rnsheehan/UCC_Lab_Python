"""
Definition of a class that describes the bounds of a parameter sweep space
e.g. sweep from start-value to stop-value in steps of delta

R. Sheehan 1 - 3 - 2019
"""

class SweepSpace(object):
    """
    Class that describes the bounds of a parameter sweep space
    """

    def __init__(self, no_points, start_value, stop_value):
        """
        Constructor for the SweepSpace object
        
        no_points (type:int) is number of distinct points within the sweep space
        start_value (type:float) is start of sweep space
        stop_value (type:float) is end of sweep space
        """   

        try:
            self.MOD_NAME_STR = "Sweep_Interval"
            self.FUNC_NAME = ".__init__()" # use this in exception handling messages
            self.ERR_STATEMENT = "Error: " + self.MOD_NAME_STR + self.FUNC_NAME
            
            # assign default values to the class members
            self.Nsteps = 0
            self.start = 0.0
            self.stop = 0.0
            self.delta = 0.0
            self.delta_min = 0.01
            self.defined = False

            self.SetVals(no_points, start_value, stop_value) # assign values to the class members
            
        except Exception as e:
            print(self.ERR_STATEMENT)
            print(e)
            
    def SetVals(self, no_points, start_value, stop_value):
        """
        Define the values for the sweep interval
        
        no_points (type:int) is number of distinct points within the sweep space
        start_value (type:float) is start of sweep space
        stop_value (type:float) is end of sweep space
        """
        
        self.FUNC_NAME = ".SetVals()" # use this in exception handling messages
        self.ERR_STATEMENT = "Error: " + self.MOD_NAME_STR + self.FUNC_NAME
        
        try:
            c1 = True if no_points > 3 else False
            c2 = True if abs(stop_value - start_value) > 0 else False
            c10 = c1 and c2

            if c10:
                self.Nsteps = no_points # no steps inside the interval
                self.start = min(start_value, stop_value)
                self.stop = max(stop_value, start_value)
                self.delta = max( (self.stop - self.start) / float(self.Nsteps - 1), self.delta_min) # Determine the sweep voltage increment, this is bounded below by delta_v_min
                self.defined = True
            else:
                if not c1:
                    self.ERR_STATEMENT = self.ERR_STATEMENT + '\nno_points in interval is too small'
                if not c2:
                    self.ERR_STATEMENT = self.ERR_STATEMENT + '\nlength of interval is not defined'
                raise Exception
        except Exception as e:
            print(self.ERR_STATEMENT)
            print(e)
        



