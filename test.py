# -*- coding: utf-8 -*-
"""
Created on Tue Apr 28 22:52:10 2015

@author: Jacob Riedel and Deniz Celik
"""

import numpy as np
import thinkdsp
import pyaudio
from array import array


class vocoder():
    def __init__(self,filename = "flesh_wound.wav", signal_type = "saw", pitch = 440, num_channel = 1024, num_band = 32):
        
        self.num_bands = num_band
        self.num_channels = num_channel
        self.input = thinkdsp.read_wave(filename)
        self.input_spec = self.spectrum_gen(self.input)
        self.framerate = self.input.framerate
        self.duration = self.input.duration
        
        self.signal_type = signal_type
        self.pitch = pitch
        self.channel = self.Sig_generate()  
        self.channel_spec = self.spectrum_gen(self.channel)
        
        input_seg = self.segmentor(self.input)        
        channel_seg = self.segmentor(self.channel)

        voded_wave = self.vocode(input_seg,channel_seg)
        self.output = voded_wave
        self.output_spec = self.spectrum_gen(self.output)

    def set_input(self, new_file):
        self.input = thinkdsp.read_wave(new_file)
        self.framerate = self.input.framerate
        self.duration = self.input.duration
        
    def set_channel(self, new_type, new_pitch):
        self.signal_type = new_type
        self.pitch = new_pitch
        
    def set_num_channel(self, new_num):
        self.num_channels = new_num        
        
    def record_input(self):
        chunk = 1024
        self.framerate = 41000
        self.pya = pyaudio.PyAudio() # initialize pyaudio
        self.stream = self.pya.open(format = pyaudio.paInt16,
           channels = 1,
           rate = self.framerate,
           input = True,
           output = True,
           frames_per_buffer = chunk)
        data = self.get_samples_from_mic(self.framerate,300,chunk)
        self.input = thinkdsp.Wave(data,self.framerate)
        self.stream.close()
        self.pya.terminate()
    
    def segmentor(self, wave):
        'Turns the input wave into segmented parts to vocode properlly'
        Seg = []
        for i in np.arange(0, wave.duration, wave.duration/self.num_channels):
            Seg.append(wave.segment(start=i, duration=wave.duration/self.num_channels))
        return Seg
        
    def spectrum_gen(self, wave):  
        spectrum = wave.make_spectrum()
        return spectrum
    
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
        
        
    def update(self):
        self.channel = self.Sig_generate()        
        self.channel_spec = self.spectrum_gen(self.channel)
        self.input_spec = self.spectrum_gen(self.input)
        
        input_seg = self.segmentor(self.input)        
        channel_seg = self.segmentor(self.channel)

        voded_wave = self.vocode(input_seg,channel_seg)
        self.output = voded_wave
        self.output_spec = self.spectrum_gen(self.output)
        
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
        # return the data_vec samples    
        return x