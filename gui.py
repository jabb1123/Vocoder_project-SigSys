# -*- coding: utf-8 -*-
"""
Created on Wed Apr 22 22:52:10 2015

@author: Deniz Celik and Jacob Riedel
"""

import Tkinter as tk
#import matplotlib
from matplotlib import pyplot as plt
from matplotlib import  style
import Vocoder as vc
#import thinkdsp
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg#, NavigationToolbar2TkAgg
import winsound


HEADER_FONT = ("Helvetica",24)
#MIN_HEIGHT = 600
#MIN_WIDTH  = 800
style.use('ggplot')
  
def callback(val):
    print val
  
def play_audio(wave):
    wave.write('temp.wav')
    winsound.PlaySound('temp.wav', winsound.SND_FILENAME)
    return 'temp.wav'

class gui(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        #Don't allow gui to be resized
        self.resizable(False,False)
        self.title('SigSys Vocoder')
        self.iconbitmap(self, default='Vocoder_logo.ico')
        self.vocoder = vc.vocoder()#filename = 'temp.wav')

        
        #Create frame for main window
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand="True")
        
        #Configure grid weights
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        #Create interface frame
        self.interface= Interface(container,self)
        self.interface.grid(row=0,column=0,sticky="NEWS",padx = 0)
    
        #Create waves frame
        self.waves = Waves(container,self)
        self.waves.grid(row=0,column=1,sticky="NEWS",padx = 0) 
        
        #Create the MenuBar
        menu = tk.Menu(container)
        tk.Tk.config(self, menu=menu)
    
        #Add file dropdown menu
        filemenu = tk.Menu(menu,tearoff=0)
        menu.add_cascade(label="File", menu=filemenu)
        
        #Add options to file menu
        filemenu.add_command(label="About", command=quit)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=quit)
                
        
class Interface(tk.Frame):
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent, highlightthickness=0)
        label = tk.Label(self, text="Interface",font=HEADER_FONT)
        label.grid(row=0)
        self.gui = controller
        
        #INPUT STUFF
        inputs = tk.Frame(self, height = 150, width = 150)
        inputs.grid(row=1,pady=50)     

        input_play = tk.BooleanVar()   
        input_play.set(False)
        
        play_input = tk.Button(inputs,height = 2, text="Press to Play",
                               command = lambda: play_audio(self.gui.vocoder.input))
        play_input.grid(row=0, pady = 15)
        
        record_input = tk.Button(inputs,height = 2, text="Press to Record",
                                 command = lambda: self.record_audio(rec_time.get()))
        record_input.grid(row=2, pady = 15)
        
        rec_time = tk.IntVar()
        rec_time.set(6)        
        
        input_label = tk.Label(inputs, text="Rec Time:")
        input_label.grid(row=1, column= 0, pady=5, sticky = "w")
        rec_timer = tk.Spinbox(inputs,width = 2,wrap = True, 
                               from_ = 1,to=10,
                               textvariable = rec_time,
                               command = lambda: callback(rec_time.get()))
        rec_timer.delete(0,tk.END)
        rec_timer.insert(0,6)
        rec_timer.grid(row=1,column = 1, pady=5, sticky = "w")
        
        #OUTPUT STUFF
        outputs = tk.Canvas(self, height = 150, width = 150)
        outputs.grid(row=3,pady=70)
        
        output_play = tk.BooleanVar()   
        output_play.set(False)    
        
        volume = tk.IntVar()   
        volume.set(5)
        
        play_output = tk.Button(outputs,height = 2, text="Press to Play",
                                command = lambda: play_audio(self.gui.vocoder.output))
        play_output.grid(row=1, column=0, pady = 15)
        
        vocode = tk.Button(outputs,height = 2, text="Press to Vocode",
                                command = lambda: self.vocodestuff())
        vocode.grid(row=0, column=0, pady = 15)
        
#        volume_output = tk.Scale(outputs,label = "Happiness Factor",variable = volume,
#                                 from_ = 10,to=0, 
#                                 command = lambda volume: callback(volume))
#        volume_output.set(5)
#        volume_output.grid(row=0, column=0, pady=15)
        
        #Channel stuff
        channels = tk.Frame(self, height = 450, width = 150)
        channels.grid(row=2, pady=0)
        channel_options = ('Sawtooth', 'Sin', 'Cos',
                           'Square', 'Triangle', 'Parabolic') 
        #Channel 1 Stuff
        ch1 = tk.Canvas(channels,height = 150, width = 150)
        ch1.grid(row=1, pady=55)
#        
#        ch1_var = tk.BooleanVar()
#        ch1_var.set(False)
        
        ch1_freq = tk.IntVar()
        ch1_freq.set(440)
        
        ch1_wave = tk.StringVar()
        ch1_wave.set(channel_options[0])
          
        ch1_dropdown = tk.OptionMenu(ch1,ch1_wave,*channel_options,
                                     command = lambda ch1_wave: self.update_modulator(ch1_wave, ch1_freq.get()))
        ch1_dropdown.grid(row=0, columnspan = 1, sticky = "w")
        
        ch1_label = tk.Label(ch1, text="Pitch:")
        ch1_label.grid(row=0, column= 1, pady=20, sticky = "w")
        ch1_pitch = tk.Spinbox(ch1,width = 4,wrap = True, 
                               from_ = 100,to=1000,
                               textvariable = ch1_freq,
                               command = lambda: self.update_modulator(ch1_wave.get(), ch1_freq.get()))
        ch1_pitch.delete(0,tk.END)
        ch1_pitch.insert(0,440)
        ch1_pitch.grid(row=0, column =2, pady=5, sticky = "w")
        
#        ch1_toggle = tk.Checkbutton(ch1,    
#                                    text="Toggle Channel 1 Modulation",
#                                    variable=ch1_var,
#                                    command = lambda: callback(ch1_var.get()))
#        ch1_toggle.grid(row=1, pady = 5,columnspan = 3, sticky = "w")
        
    def record_audio(self, time):
        self.gui.vocoder.record_input(recordtime = time)
        self.gui.vocoder.update("record")
        self.gui.waves.update()
    
    def update_modulator(self, sig, pitch):
        self.gui.vocoder.set_channel(sig,pitch)
        self.gui.vocoder.update("update")
        self.gui.waves.update()
        
    def vocodestuff(self):
        self.gui.vocoder.update("v")
        self.gui.waves.update()
        
class Waves(tk.Frame):
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent, highlightthickness=0)
        label = tk.Label(self, text="Waves",font=HEADER_FONT)
        label.grid(row=0)
        self.gui = controller
        
        #INPUT STUFF
        input_fig = plt.figure(figsize=(6.5,2.5), dpi=100)
        input_fig.subplots_adjust(left=0.11, right=0.96,
                                   top=0.95, bottom=0.11,
                                   wspace = 0.2, hspace = 0.43)
        
        self.input_wave = input_fig.add_subplot(211)        
        self.input_spec = input_fig.add_subplot(212)
        
        self.input_plot = FigureCanvasTkAgg(input_fig, master=self)
        self.input_plot._tkcanvas.config(highlightthickness=0)
        self.input_plot.show()
        self.input_plot.get_tk_widget().grid(row=1)           
                
        #CHANNEL STUFF
        channel_fig = plt.figure(figsize=(6.5,2.5), dpi=100)
        channel_fig.subplots_adjust(left=0.11, right=0.96,
                                   top=0.95, bottom=0.11,
                                   wspace = 0.2, hspace = 0.43)
        
        self.channel_wave = channel_fig.add_subplot(211)
        self.channel_spec = channel_fig.add_subplot(212)
        
        self.channel_plot = FigureCanvasTkAgg(channel_fig, master=self)
        self.channel_plot._tkcanvas.config(highlightthickness=0)
        self.channel_plot.show()
        self.channel_plot.get_tk_widget().grid(row=2)
        
        #OUTPUT STUFF
        output_fig = plt.figure(figsize=(6.5,2.5), dpi=100)
        output_fig.subplots_adjust(left=0.11, right=0.96,
                                   top=0.95, bottom=0.11,
                                   wspace = 0.2, hspace = 0.43)        
        
        self.output_wave = output_fig.add_subplot(211)
        self.output_spec = output_fig.add_subplot(212)
        
        self.output_plot = FigureCanvasTkAgg(output_fig, master=self)
        self.output_plot._tkcanvas.config(highlightthickness=0)
        self.output_plot.show()
        self.output_plot.get_tk_widget().grid(row=3)
        
        self.update()
#        toolbar = NavigationToolbar2TkAgg( input_plot, self )
#        toolbar.update()
#        toolbar.grid(row=5,sticky='W')
    
    def update(self):
        self.input_wave.clear()
        self.input_spec.clear()
        self.input_wave.plot(self.gui.vocoder.input.ts,self.gui.vocoder.input.ys)
        self.input_spec.plot(self.gui.vocoder.input_spec.fs,self.gui.vocoder.input_spec.amps)
        self.input_plot.show()
        
        self.channel_wave.clear()
        self.channel_spec.clear()
        channel_wave_seg = self.gui.vocoder.channel.segment(duration=(1.0/self.gui.vocoder.pitch)*5)
        self.channel_wave.plot(channel_wave_seg.ts,channel_wave_seg.ys)
        self.channel_spec.plot(self.gui.vocoder.channel_spec.fs,self.gui.vocoder.channel_spec.amps)   
        self.channel_plot.show()
        
        self.output_wave.clear()
        self.output_spec.clear()
        self.output_wave.plot(self.gui.vocoder.output.ts,self.gui.vocoder.output.ys)
        self.output_spec.plot(self.gui.vocoder.output_spec.fs,self.gui.vocoder.output_spec.amps)
        self.output_plot.show()
        
if __name__ == "__main__":
    #mod = C.Model()
    #con = C.Controller(mod)
    app = gui()
    
    app.mainloop()