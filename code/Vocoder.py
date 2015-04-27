# -*- coding: utf-8 -*-
"""
This code will vocode an audio input with a generated signal.  
In doing so, the orignial sound will be distorted to sound like the generated signal.
"""

import numpy as np
import thinkdsp
import pyaudio

class vocoder():
    def __init__(self,filename = "flesh_wound.wav", signal_type = ["saw"], pitch = [440], segment_rate = 1.0/200, ):
    
        self.voice_wave = thinkdsp.read_wave(filename) # read in recording
        self.voice_wave.normalize
        self.framerate= self.voice_wave.framerate # determine framerate
        self.duration = self.voice_wave.duration # determine duration
        self.pya = pyaudio.PyAudio() # initialize pyaudio
        self.stream = self.pya.open(format = pyaudio.paInt16,channels=1, rate=self.framerate, output=True)
        self.signal_types = signal_type # list of the type of signals to generate
        self.pitches = pitch # list of fundementals for the generated waves
        self.segment_rate = segment_rate # Number of segments per second
        
        if len(self.pitches) != len(self.signal_types):
            print('The number of signals does not match the number of frequencies chosen')
            return
        
        seg_voi = self.segmentor(self.voice_wave)        
        
        self.sig_wave = self.Sig_generate()
        seg_sig = self.segmentor(self.sig_wave)
        
        voded_wave = self.vocode(seg_voi,seg_sig)
        
        self.play_audio(voded_wave)
        
        self.stream.close()
        self.pya.terminate()
    
    def segmentor(self, wave):
        'Turns the input wave into segmented parts to vocode properlly'
        if type(wave) is list:
            segmented_list = []
            for i in wave:
                seg = self.segmentor(i)
                segmented_list.append(seg)
            return segmented_list
        else:
            Seg = []
            for s in np.arange(0,self.duration,self.segment_rate):
                Seg.append(wave.segment(s,self.segment_rate))
            return Seg
        
    def spectrum_gen(self, wave):  
        spectrum = wave.make_spectrum()
        return spectrum
    #    v_spectrum.plot()
    
    def Sig_generate(self):
        'Chooses what generated signal to use, and at what pitch.'
        wave = []
        for i in range(len(self.signal_types)):
            if self.signal_types[i] == 'saw':
                sig = thinkdsp.SawtoothSignal(freq=self.pitches[i], amp=1, offset=0)
            elif self.signal_types[i] == 'sin':
                sig = thinkdsp.SinSignal(freq=self.pitches[i], amp=1, offset=0)
            elif self.signal_types[i] == 'cos':
                sig = thinkdsp.CosSignal(freq=self.pitches[i], amp=1, offset=0)
            elif self.signal_types[i] == 'tri':
                sig = thinkdsp.TriangleSignal(freq=self.pitches[i], amp=1, offset=0)
            elif self.signal_types[i] == 'sqr':
                sig = thinkdsp.SquareSignal(freq=self.pitches[i], amp=1, offset=0)
            elif self.signal_types[i] == 'par':
                sig = thinkdsp.ParabolicSignal(freq=self.pitches[i], amp=1, offset=0)
            wav=sig.make_wave(framerate = self.framerate, duration = self.duration)
            wav.normalize
            wave.append(wav)
            
        return wave
            
        #wave.normalize()
    #    wave.apodize()
    #    wave.plot()
    #    for ys in wave:
    #        print ys    

    def vocode(self, segment_voice, segment_gen):
        """This is the vocoder.  It multiplies the amplitudes of two seperate signals
        to produce a singular response""" 
        vocoder_wave = 0
        if type(segment_gen[0]) is list:
            for x in segment_gen:
                vcw = self.vocode(segment_voice, x)
                vocoder_wave = vcw
        else:
            for i in range(len(segment_voice)):
                vocoder_spec=thinkdsp.Spectrum(hs = segment_voice[i].make_spectrum().amps*segment_gen[i].make_spectrum().amps,framerate = self.framerate)
                if i == 0:
                    vocoder_wave =vocoder_spec.make_wave()
                else:
                     vocoder_wave |= vocoder_spec.make_wave()
        return vocoder_wave
    #    vocoder_wave.plot()
        
    #    vocoder_wave.make_spectrum().plot()
        
        
    def play_audio(self,wave):
        wave.normalize
        self.stream.write((wave.ys).astype(np.int16).tostring())
        self.stream.stop_stream()
                
    def plot_fig(self, fig, str_ident):
        if(str_ident=="input"):
            fig.plot([1],[2])#put plot stuff here 
        elif(str_ident=="ch1"):
            fig.plot([1],[2])#put plot stuff here
        elif(str_ident=="ch2"):
            fig.plot([1],[2])#put plot stuff here
        elif(str_ident=="ch3"):
            fig.plot([1],[2])#put plot stuff here
        elif(str_ident=="output"):
            fig.plot([1],[2])


        
def plot_fig(fig, str_ident):
    if(str_ident=="input"):
        fig.plot([1],[2])#put plot stuff here 
    elif(str_ident=="ch1"):
        fig.plot([1],[2])#put plot stuff here
    elif(str_ident=="ch2"):
        fig.plot([1],[2])#put plot stuff here
    elif(str_ident=="ch3"):
        fig.plot([1],[2])#put plot stuff here
    elif(str_ident=="output"):
        fig.plot([1],[2])#put plot stuff here


if __name__ == "__main__":
    vocoder()