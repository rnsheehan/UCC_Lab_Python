import numpy as np
import tkinter as tk
import sys
import time
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import IBM4_Lib

class App:
    """Define the application class."""
    def __init__(self,root):
        self.root = root
        ### The following grid_columnconfigure statemets make all the columns to belong to the same group, will have the
        ### size of the largest widget
        #self.root.grid_columnconfigure(0, weight=1, uniform="fred")
        #self.root.grid_columnconfigure(1, weight=1, uniform="fred")
        #self.root.grid_columnconfigure(2, weight=1, uniform="fred")
        #self.root.grid_columnconfigure(3, weight=1, uniform="fred")
        #self.root.grid_columnconfigure(4, weight=1, uniform="fred")
        #self.root.grid_columnconfigure(5, weight=1, uniform="fred")
        #self.root.grid_columnconfigure(6, weight=1, uniform="fred")

        self.root.title('IBM4 Multimeter Mode')
        self.the_dev = IBM4_Lib.Ser_Iface() # find the first connected IBM4, open in DC mode by default

        self.radio = Radiobutton(self,'ID;Set A0;Set A1;Set PWM;Ground Outputs;Read Inputs;Diff. Measurement', 'print(self.mssg)')
        # Add windows where we are going to write the std output.
        self.console_text = tk.Text(self.root, state='disabled', height=10)
        self.console_text.grid(row=2,column=0,rowspan=10,columnspan=10,sticky='we')

        # We redirect sys.stdout -> TextRedirector
        self.redirect_sysstd()

        # We add a button to test our setup
        self.test_button = tk.Button(self.root, text="Run", command=self.run_mode)
        self.test_button.grid(row=12,column=0)

        self.voutval = tk.StringVar(value='0')
        tk.Label(text='Vout :').grid(row=12,column=1,sticky='e')
        tk.Entry(root, textvariable=self.voutval, width=10).grid(row=12,column=2,sticky='w')

        self.pwmpc = tk.StringVar(value='0')
        tk.Label(text='PWM % :').grid(row=12,column=3,sticky='e')
        tk.Entry(root, textvariable=self.pwmpc, width=10).grid(row=12,column=4,sticky='w')

        self.diffch = tk.StringVar(value='A2,A3')
        tk.Label(text='Diff. Channels (+,-) :').grid(row=12,column=5,sticky='e')
        tk.Entry(root, textvariable=self.diffch, width=10).grid(row=12,column=6,sticky='w')

    def redirect_sysstd(self):
        # We specify that sys.stdout point to TextRedirector
        sys.stdout = TextRedirector(self.console_text, "stdout")
        sys.stderr = TextRedirector(self.console_text, "stderr")

    def run_mode(self):
        print('Now running: '+self.radio.item)
        action = self.radio.val.get()
        ## ADAPTED FROM ROBS MULTIMETER MODE
        if action == 0:
            self.the_dev.IDNPrompt()
        elif action == 1:
            self.the_dev.WriteVoltage('A0', float(self.voutval.get()))
        elif action == 2:
            self.the_dev.WriteVoltage('A1', float(self.voutval.get()))
        elif action == 3:
            self.thedev.WritePWM(float(self.pwmpc.get()))
        elif action == 4:
            self.the_dev.ZeroIBM4()
        elif action == 5:
            ch_vals = self.the_dev.ReadAverageVoltageAllChnnl()
            print('AI voltages: ',ch_vals)
        elif action == 6:
            chns = self.diffch.get().split(',')
            diff_res = self.the_dev.DiffReadMultiple(chns[0], chns[1])
            print('Differential Read Value = %(v1)0.3f +/- %(v2)0.3f (V)'%{"v1":diff_res[0], "v2":diff_res[1]})
        #del the_dev # destructor for the IBM4 object, closes comms


class Radiobutton:
    """Create a list-based Radiobutton object."""

    def __init__(self, App, items='Radiobutton', cmd='', val=0, **kwargs):
        self.items = items.split(';')
        self.cmd = cmd
        self.val = tk.IntVar()
        self.val.set(val)
        self.item = self.items[self.val.get()]
        for i, item in enumerate(self.items):
            r = tk.Radiobutton(App.root, text=item, variable=self.val,
                                value=i, command=self.cb, **kwargs)
            r.grid(row=1,column=i)#,sticky='w')
            #r.pack(side=tk.LEFT)
    def cb(self):
        """Evaluate the cmd string in the Radiobutton context."""
        self.item = self.items[self.val.get()]
        self.mssg = 'Mode '+self.item+' selected'
        exec(self.cmd)

class TextRedirector(object):
    def __init__(self, widget, tag):
        self.widget = widget
        self.tag = tag

    def write(self, text):
        self.widget.configure(state='normal') # Edit mode
        self.widget.insert(tk.END, text, (self.tag,)) # insert new text at the end of the widget
        self.widget.configure(state='disabled') # Static mode
        self.widget.see(tk.END) # Scroll down
        self.widget.update_idletasks() # Update the console

    def flush(self):
        pass

root = tk.Tk()
root.resizable(False, False)
app = App(root)
root.mainloop()
