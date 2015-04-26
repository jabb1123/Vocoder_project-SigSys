import Tkinter as tk
#import matplotlib
from matplotlib import pyplot as plt
from matplotlib import style
#import vocoder as vc
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg


HEADER_FONT = ("Helvetica",24)
#MIN_HEIGHT = 600
#MIN_WIDTH  = 800
style.use('ggplot')

class gui(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        #Don't allow gui to be resized
        self.resizable(False,False)
        self.title('SigSys Vocoder')
       # self.iconbitmap(self, default='Vocoder_logo.ico')
        
        #Create frame for main window
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand="True")
        
        #Configure grid weights
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        #Create interface frame
        self.interface= Interface(container,self)
        self.interface.grid(row=0,column=0,sticky="NEWS",padx = 20)
        
        #Create divider canvas
        #self.divider = tk.Canvas(container,width=10,bg="gray")
        #self.divider.grid(row=0, column=1, rowspan=1)
        
        #Create waves frame
        self.waves = Waves(container,self)
        self.waves.grid(row=0,column=1,sticky="NEWS",padx = 20) 
        
        #Create the MenuBar
        menu = tk.Menu(container)
        tk.Tk.config(self, menu=menu)
    
        #Add file dropdown menu
        filemenu = tk.Menu(menu,tearoff=0)
        menu.add_cascade(label="File", menu=filemenu)
        
        #Add options to file menu
        filemenu.add_command(label="About", command=quit)
        filemenu.add_command(label="Number of Modulators",command=quit)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=quit)
        
        

class Interface(tk.Frame):
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text="Interface",font=HEADER_FONT)
        label.grid(row=0)
        
        f = plt.figure(figsize=(5,5), dpi=100)
        channel_num = 3
        
        a = f.add_subplot(channel_num*100+(11))
        a.plot([1,2,3,4,5,6,7,8],[5,6,1,3,8,9,3,5])
        
        a1 = f.add_subplot(channel_num*100+(12))
        a1.plot([1,2,3,4,5,6,7,8],[5,6,1,3,8,9,3,5])
        
        a2 = f.add_subplot(channel_num*100+(13))
        a2.plot([1,2,3,4,5,6,7,8],[5,6,1,3,8,9,3,5])
        
        canvas = FigureCanvasTkAgg(f, master=self)
        canvas.show()
        canvas.get_tk_widget().grid(row=1)
        
        toolbar = NavigationToolbar2TkAgg( canvas, self )
        toolbar.update()
        toolbar.grid(row=2,sticky='W')
        
class Waves(tk.Frame):
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text="Waves",font=HEADER_FONT)
        label.grid(row=0)
        
        f = plt.figure(figsize=(5,5), dpi=100)
        channel_num = 3
        
        a = f.add_subplot(channel_num*100+(11))
        a.plot([1,2,3,4,5,6,7,8],[5,6,1,3,8,9,3,5])
        
        a1 = f.add_subplot(channel_num*100+(12))
        a1.plot([1,2,3,4,5,6,7,8],[5,6,1,3,8,9,3,5])
        
        a2 = f.add_subplot(channel_num*100+(13))
        a2.plot([1,2,3,4,5,6,7,8],[5,6,1,3,8,9,3,5])
        
        canvas = FigureCanvasTkAgg(f, master=self)
        canvas.show()
        canvas.get_tk_widget().grid(row=1)
        
        toolbar = NavigationToolbar2TkAgg( canvas, self )
        toolbar.update()
        toolbar.grid(row=2,sticky='W')
  
  
if __name__ == "__main__":
    #mod = C.Model()
    #con = C.Controller(mod)
    app = gui()
    
    app.mainloop()