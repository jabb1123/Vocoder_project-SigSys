# -*- coding: utf-8 -*-
"""
This code will vocode an audio input with a generated signal.  
In doing so, the orignial sound will be distorted to sound like the generated signal.
"""

import numpy as np
import thinkdsp
import pyaudio

def vocoder(filename = "flesh_wound.wav", signal_type = "saw", pitch = 220, sample = 1.0/100, ):

    voice_wave = thinkdsp.read_wave(filename)
    frames= voice_wave.framerate
    print(voice_wave.duration)
    print(voice_wave.framerate)
    #wave.normalize()
    p = pyaudio.PyAudio()
    stream = p.open(format = pyaudio.paInt16,channels=1, rate=frames, input=False, output=True)     
    print(voice_wave.ys.astype(np.int16))
    stream.write(voice_wave.ys.astype(np.int16).tostring())
#    stream.stop_stream()
    
    'Turns the input wave into segmented parts to vocode properlly'
    voice_seg = []
    for s in np.arange(0,voice_wave.duration,sample):
        voice_seg.append(voice_wave.segment(s,sample))
    
    v_spectrum = voice_wave.make_spectrum()
#    v_spectrum.plot()
    
    'Chooses what generated signal to use, and at what pitch.'
    if signal_type == 'saw':
        sig = thinkdsp.SawtoothSignal(freq=pitch, amp=1000, offset=0)
    elif signal_type == 'sin':
        sig = thinkdsp.SinSignal(freq=pitch, amp=1, offset=0)
    elif signal_type == 'cos':
        sig = thinkdsp.CosSignal(freq=pitch, amp=1, offset=0)
    elif signal_type == 'tri':
        sig = thinkdsp.TriangleSignal(freq=pitch, amp=1, offset=0)
    elif signal_type == 'sqr':
        sig = thinkdsp.SquareSignal(freq=pitch, amp=1, offset=0)
    elif signal_type == 'par':
        sig = thinkdsp.ParabolicSignal(freq=pitch, amp=1, offset=0)
    wave=sig.make_wave(framerate = voice_wave.framerate, duration = voice_wave.duration)
    #wave.normalize()
#    wave.apodize()
#    wave.plot()
#    stream.write(wave.ys.astype(np.int16).tostring())
    print wave.ys
#    for ys in wave:
#        print ys    
    'Seperated the generated signal into equal segments as the voice wave.'
    Seg = []
    for s in np.arange(0,wave.duration,sample):
        Seg.append(wave.segment(s,sample))
    
    """This is the vocoder.  It multiplies the amplitudes of two seperate signals
    to produce a singular response"""    
    
    for i in range(len(voice_seg)):
        vocoder_spec=thinkdsp.Spectrum(hs = voice_seg[i].make_spectrum().amps*Seg[i].make_spectrum().amps,framerate = frames)
        if i == 0:
            vocoder_wave =vocoder_spec.make_wave()
        else:
             vocoder_wave |= vocoder_spec.make_wave()
#    vocoder_wave.plot()
    
#    vocoder_wave.make_spectrum().plot()
    
    vocoder_wave.normalize()
    stream = p.open(format = pyaudio.paInt16,channels=1, rate=frames, input=False, output=True)
    print (vocoder_wave.ys*2**13).astype(np.int16)
    stream.write((vocoder_wave.ys*2**13).astype(np.int16).tostring())
    stream.stop_stream()
    stream.close()
    p.terminate() 
    print "done"
    
    return (vocoder_wave)

if __name__ == "__main__":
    vocoder()