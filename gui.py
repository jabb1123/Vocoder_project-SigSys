import Tkinter as tk
#import matplotlib
from matplotlib import pyplot as plt
from matplotlib import  style
#import vocoder
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg#, NavigationToolbar2TkAgg


HEADER_FONT = ("Helvetica",24)
#MIN_HEIGHT = 600
#MIN_WIDTH  = 800
style.use('ggplot')
  
def callback(val):
    print val

class gui(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        #Don't allow gui to be resized
        self.resizable(False,False)
        self.title('SigSys Vocoder')
        self.iconbitmap(self, default='Vocoder_logo.ico')
        
        #Create frame for main window
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand="True")
        
        #Configure grid weights
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        #Create interface frame
        self.interface= Interface(container,self)
        self.interface.grid(row=0,column=0,sticky="NEWS",padx = 0)
        
        #Create divider canvas
        #self.divider = tk.Canvas(container,width=10,bg="gray")
        #self.divider.grid(row=0, column=1, rowspan=1)
        
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
        
        inputs = tk.Frame(self, height = 150, width = 150)
        inputs.grid(row=1,pady=5)     

        input_play = tk.BooleanVar()   
        input_play.set(False)
        
        play_input = tk.Button(inputs,height = 2, text="Press to Play")
        play_input.grid(row=0, pady = 15)
        
        record_input = tk.Button(inputs,height = 2, text="Press to Record")
        record_input.grid(row=2, pady = 15)
        
        outputs = tk.Canvas(self, height = 150, width = 150)
        outputs.grid(row=3,pady=10)
        
        output_play = tk.BooleanVar()   
        output_play.set(False)    
        
        volume = tk.IntVar()   
        volume.set(5)
        
        play_output = tk.Button(outputs,height = 2, text="Press to Play")
        play_output.grid(row=0, column=1, pady = 15)
        
        volume_output = tk.Scale(outputs,label = "Volume",variable = volume,
                                 from_ = 10,to=0, 
                                 command = lambda volume: callback(volume))
        volume_output.set(5)
        volume_output.grid(row=0, column=0, pady=15)
        
        #Channel stuff
        channels = tk.Frame(self, height = 450, width = 150)
        channels.grid(row=2, pady=0)
        channel_options = ('Sin', 'Cos', 'Sawtooth',
                           'Square', 'Triangle', 'Parabolic') 
        #Channel 1 Stuff
        ch1 = tk.Canvas(channels,height = 150, width = 150)
        ch1.grid(row=1, pady=55)
        
        ch1_var = tk.BooleanVar()
        ch1_var.set(False)
        
        ch1_freq = tk.IntVar()
        ch1_freq.set(440)
        
        ch1_wave = tk.StringVar()
        ch1_wave.set(channel_options[0])
          
        ch1_dropdown = tk.OptionMenu(ch1,ch1_wave,*channel_options,
                                     command = lambda ch1_wave: callback(ch1_wave))
        ch1_dropdown.grid(row=0, columnspan = 1, sticky = "w")
        
        ch1_label = tk.Label(ch1, text="Pitch")
        ch1_label.grid(row=0, column= 1, pady=5, padx = 0, sticky = "w")
        ch1_pitch = tk.Spinbox(ch1,width = 4,wrap = True, 
                               from_ = 100,to=1000,
                               textvariable = ch1_freq,
                               command = lambda: callback(ch1_freq.get()))
        ch1_pitch.delete(0,tk.END)
        ch1_pitch.insert(0,440)
        ch1_pitch.grid(row=0, column =2, pady=5, sticky = "w")
        
        ch1_toggle = tk.Checkbutton(ch1,    
                                    text="Toggle Channel 1 Modulation",
                                    variable=ch1_var,
                                    command = lambda: callback(ch1_var.get()))
        ch1_toggle.grid(row=1, pady = 5,columnspan = 3, sticky = "w")
        
        #Channel 2 Stuff
        ch2 = tk.Canvas(channels,height = 150, width = 150)
        ch2.grid(row=2, pady=25)
        
        ch2_var = tk.BooleanVar()
        ch2_var.set(False)
        
        ch2_freq = tk.IntVar()
        ch2_var.set(440)
        
        ch2_wave = tk.StringVar()
        ch2_wave.set(channel_options[0])
          
        ch2_dropdown = tk.OptionMenu(ch2,ch2_wave,*channel_options,
                                     command = lambda ch2_wave: callback(ch2_wave))
        ch2_dropdown.grid(row=0, columnspan = 1, sticky = "w")
        
        ch2_label = tk.Label(ch2, text="Pitch")
        ch2_label.grid(row=0, column= 1, pady=5, padx = 0, sticky = "w")
        ch2_pitch = tk.Spinbox(ch2,width = 4,wrap = True, 
                               from_ = 100,to=1000,
                               textvariable = ch2_freq,
                               command = lambda: callback(ch2_freq.get()))
        ch2_pitch.delete(0,tk.END)
        ch2_pitch.insert(0,440)
        ch2_pitch.grid(row=0, column =2, pady=5, sticky = "w")
        
        ch2_toggle = tk.Checkbutton(ch2,    
                                    text="Toggle Channel 2 Modulation",
                                    variable=ch2_var,
                                    command = lambda: callback(ch2_var.get()))
        ch2_toggle.grid(row=1, pady = 5,columnspan = 3, sticky = "w")
        
        #Channel 3 Stuff
        ch3 = tk.Canvas(channels,height = 150, width = 150)
        ch3.grid(row=3, pady=50)
        
        ch3_var = tk.BooleanVar()
        ch3_var.set(False)
        
        ch3_freq = tk.IntVar()
        ch3_var.set(440)
        
        ch3_wave = tk.StringVar()
        ch3_wave.set(channel_options[0])
          
        ch3_dropdown = tk.OptionMenu(ch3,ch3_wave,*channel_options,
                                     command = lambda ch3_wave: callback(ch3_wave))
        ch3_dropdown.grid(row=0, columnspan = 1, sticky = "w")
        
        ch3_label = tk.Label(ch3, text="Pitch")
        ch3_label.grid(row=0, column= 1, pady=5, padx = 0, sticky = "w")
        ch3_pitch = tk.Spinbox(ch3,width = 4,wrap = True, 
                               from_ = 100,to=1000,
                               textvariable = ch3_freq,
                               command = lambda: callback(ch3_freq.get()))
        ch3_pitch.delete(0,tk.END)
        ch3_pitch.insert(0,440)
        ch3_pitch.grid(row=0, column =2, pady=5, sticky = "w")
        
        ch3_toggle = tk.Checkbutton(ch3,    
                                    text="Toggle Channel 3 Modulation",
                                    variable=ch3_var,
                                    command = lambda: callback(ch3_var.get()))
        ch3_toggle.grid(row=1, pady = 5,columnspan = 3, sticky = "w")
        
class Waves(tk.Frame):
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent, highlightthickness=0)
        label = tk.Label(self, text="Waves",font=HEADER_FONT)
        label.grid(row=0)
        
        input_fig = plt.figure(figsize=(5,1.5), dpi=100)
        input_fig.subplots_adjust(left=0.07, right=0.95, bottom=0.2)
        fig_input = input_fig.add_subplot(111)
        plot_fig(fig_input, "input")
        
        input_plot = FigureCanvasTkAgg(input_fig, master=self)
        input_plot._tkcanvas.config(highlightthickness=0)
        input_plot.show()
        input_plot.get_tk_widget().grid(row=1)
        
        #input_toolbar = NavigationToolbar2TkAgg(input_plot,self)
        #input_toolbar.update()
        #input_toolbar.grid(row=2,sticky='W')                
                
        #CHANNEL STUFF
        channel_fig = plt.figure(figsize=(5,4.5), dpi=100)
        channel_fig.subplots_adjust(left=0.07, bottom=0.07,
                                    right=0.95, top=0.95, hspace=0.3)
        
        
        fig_ch1 = channel_fig.add_subplot(311)
        plot_fig(fig_ch1, "ch1")
        
        fig_ch2 = channel_fig.add_subplot(312)
        plot_fig(fig_ch2, "ch2")
        
        fig_ch3 = channel_fig.add_subplot(313)
        plot_fig(fig_ch3, "ch3")
        
        mod_plot = FigureCanvasTkAgg(channel_fig, master=self)
        mod_plot._tkcanvas.config(highlightthickness=0)
        mod_plot.show()
        mod_plot.get_tk_widget().grid(row=3)
        
        output_fig = plt.figure(figsize=(5,1.5), dpi=100)
        output_fig.subplots_adjust(left=0.07, right=0.95, bottom=0.2)        
        
        fig_output = output_fig.add_subplot(111)
        plot_fig(fig_output, "output")
        
        output_plot = FigureCanvasTkAgg(output_fig, master=self)
        output_plot._tkcanvas.config(highlightthickness=0)
        output_plot.show()
        output_plot.get_tk_widget().grid(row=4)
        
        #toolbar = NavigationToolbar2TkAgg( mod_plot, self )
        #toolbar.update()
        #toolbar.grid(row=5,sticky='W')

def plot_fig(fig, str_ident):
    if(str_ident=="input"):
        fig.plot([1,2,3,4,5,6,7,8],[5,6,1,3,8,9,3,5])#put plot stuff here 
    elif(str_ident=="ch1"):
        fig.plot([1,2,3,4,5,6,7],[5,6,1,3,8,9,3])#put plot stuff here
    elif(str_ident=="ch2"):
        fig.plot([1,2,3,4,5,6],[5,6,1,3,8,9])#put plot stuff here
    elif(str_ident=="ch3"):
        fig.plot([1,2,3,4,5],[5,6,1,3,8])#put plot stuff here
    elif(str_ident=="output"):
        fig.plot([1,2,3,4],[5,6,1,3])#put plot stuff here
  
if __name__ == "__main__":
    #mod = C.Model()
    #con = C.Controller(mod)
    app = gui()
    
    app.mainloop()