# -*- coding: utf-8 -*-
"""
This code will vocode an audio input with a generated signal.  
In doing so, the orignial sound will be distorted to sound like the generated signal.
"""

import numpy as np
import thinkdsp
import pyaudio
from array import array
import winsound, sys

class vocoder():
    def __init__(self,filename = "flesh_wound.wav", signal_type = "saw", pitch = 240, num_channel = 1024, num_band = 32):
        
        self.num_bands = num_band
        self.num_channels = num_channel

        if filename == 'record':
            chunk = 1024
            self.framerate = 41000
            self.pya = pyaudio.PyAudio() # initialize pyaudio
            self.stream = self.pya.open(format = pyaudio.paInt16,
               channels = 1,
               rate = self.framerate,
               input = True,
               output = True,
               frames_per_buffer = chunk)
            data = get_samples_from_mic(self.framerate,300,chunk)
            self.voice_wave = thinkdsp.Wave(data,self.framerate)
            self.stream.close()
            self.pya.terminate()
        else:
            self.voice_wave = thinkdsp.read_wave(filename) # read in recording
            self.framerate= self.voice_wave.framerate # determine framerate
            self.duration = self.voice_wave.duration # determine duration
        self.voice_wave.normalize
        self.signal_type = signal_type # list of the type of signals to generate
        self.pitch = pitch # list of fundementals for the generated waves        
        
        seg_voi = self.segmentor(self.voice_wave)        
        
        self.sig_wave = self.Sig_generate()
        seg_sig = self.segmentor(self.sig_wave)
        
        voded_wave = self.vocode(seg_voi,seg_sig)
        
        self.vocoded_wave = voded_wave
    
    def segmentor(self, wave):
        'Turns the input wave into segmented parts to vocode properlly'
        Seg = []
        for i in np.arange(0, wave.duration, wave.duration/self.num_channels):
            Seg.append(wave.segment(start=i, duration=wave.duration/self.num_channels))
        return Seg
        
    def spectrum_gen(self, wave):  
        spectrum = wave.make_spectrum()
        return spectrum
    #    v_spectrum.plot()
    
    def Sig_generate(self):
        'Chooses what generated signal to use, and at what pitch.'
        if self.signal_type == 'saw':
            sig = thinkdsp.SawtoothSignal(freq=self.pitch, amp=1, offset=0)
        elif self.signal_type == 'sin':
            sig = thinkdsp.SinSignal(freq=self.pitch, amp=1, offset=0)
        elif self.signal_type == 'cos':
            sig = thinkdsp.CosSignal(freq=self.pitch, amp=1, offset=0)
        elif self.signal_type == 'tri':
            sig = thinkdsp.TriangleSignal(freq=self.pitch, amp=1, offset=0)
        elif self.signal_type == 'sqr':
            sig = thinkdsp.SquareSignal(freq=self.pitch, amp=1, offset=0)
        elif self.signal_type == 'par':
            sig = thinkdsp.ParabolicSignal(freq=self.pitch, amp=1, offset=0)
        wav=sig.make_wave(framerate = self.framerate, duration = self.duration)
        wav.normalize            
        return wav
    
    def get_wave(self):
        return self.vocoded_wave

    def make_file(self, wave):
        wave.normalize
        wave.write('temp.wav')

    def vocode(self, segment_voice, segment_gen):
        """This is the vocoder.  It multiplies the amplitudes of two seperate signals
        to produce a singular response""" 
        temp_final = []
        for j in range(self.num_channels):
            saw_spec = segment_gen[j].make_spectrum()
            input_spec = segment_voice[j].make_spectrum()
        
            input_hs = input_spec.hs
            saw_hs = saw_spec.hs
        
            saw_bands = np.array_split(saw_hs, self.num_bands)
            input_bands = np.array_split(input_hs, self.num_bands)
        
            final_bands = np.empty_like(saw_bands)
            for i in range(self.num_bands):
                amp_multi = np.abs(saw_bands[i])*np.abs(input_bands[i])
                phase_multi = np.angle(saw_bands[i])
                final_bands[i] = amp_multi*(np.cos(phase_multi)+(np.sin(phase_multi)*1j))
                
            temp_final.append(np.ma.concatenate(final_bands).data)
        final_wave = []
        for i in range(len(temp_final)):
            final_wave.append(thinkdsp.Spectrum(hs=temp_final[i], framerate = self.framerate).make_wave())
        output = final_wave[0]
        for i in range(1,len(final_wave)):
            output |= final_wave[i]
        return output
        
        
    
                
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
            
def combine(wav):
    if type(wav) is list:
        wave = wav[0]
        if len(wav) > 1:
            for i in range(1,len(wav)):
                wave +=wav[i]
    else:
        wave = wav
    return wave


def get_samples_from_mic(sample_rate = 8000, threshold = 1000, chunk_size = 1000):
    # initialize pyaudio object
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=sample_rate,
            input=True, output=True,
            frames_per_buffer=chunk_size)

    
    def is_silent(snd_data, th):
    #"Returns 'True' if below the 'silent' threshold"
        return max(snd_data) < th


# initialize an array to store the data
    data_vec = array('h')
    
# wait until we hear something
    while 1:
        # read a chunk of samples from the mic
        data = stream.read(chunk_size)
        # convert the data into an array of int16s
        snd_data = array('h', data)
        # if no longer silent break out of detection loop
        if not is_silent(snd_data, threshold):
            break

# append the sound data from the previous chunk into the array             
    data_vec.extend(snd_data)
    
# collect samples until we get a silent block
    while 1:
        # read a chunk of data
        data = stream.read(chunk_size)
        snd_data = array('h', data)
        # stick the chunk of samples at the end of the vector that stores
        # the samples
        data_vec.extend(snd_data)     
        # if silent break out of loop
        if is_silent(snd_data, threshold):
            break
            
# convert to a numpy array   
# we don't use a numpy array directly because it's slower than
# array 
    x = np.frombuffer(data_vec, dtype= np.dtype('int16'))    
    
# close the pyaudio stream     
    stream.stop_stream()
    stream.close()
    p.terminate()

# return the data samples    
    return x  

        
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
        
def play_audio(wave):
    wave.normalize
    wave.write('temp.wav')
    winsound.PlaySound('temp.wav', winsound.SND_FILENAME)
    return 'temp.wav'

def make_file(wave):
    wave.normalize
    wave.write('temp.wav')
    return 'temp.wav'


if __name__ == "__main__":
    wav = []
    wav = vocoder().get_wave()
    name = make_file(wav)
    wav = vocoder(filename=name, signal_type='saw',pitch=440).get_wave()
    name = make_file(wav)
    wav = vocoder(filename=name, signal_type='saw',pitch=535).get_wave()
    wave = combine(wav)
    play_audio(wave)