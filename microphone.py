import time
import numpy as np
import pyaudio
import config
import dsp
import pygame
import cmdfun
#import matplotlib.pyplot as plt
#import matplotlib.animation as animation 
from numpy.fft import fft, ifft
pygame.init()
window = pygame.display.set_mode((300,300))
pygame.display.set_caption("Pygame Demonstration")

#X=0
RATE =1000
#prev = 0
#CHUNK = int(RATE)
#fig, ax = plt.subplots(figsize=(14,6))
#x = np.arange(0, 1000, 1)
#ax.set_ylim(0, 1)
#ax.set_xlim(0, 1000) #make sure our x axis matched our chunk size
#line = ax.plot(x, np.random.rand(1000))
#line2, = ax.plot(x, np.random.rand(CHUNK))
def start_stream(callback):
    p = pyaudio.PyAudio()
    frames_per_buffer = int(config.MIC_RATE / config.FPS)#config.FPS
    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=config.MIC_RATE,
                    input=True,
                    frames_per_buffer=frames_per_buffer)
    overflows = 0
    prev_ovf_time = time.time()
    prev = 0
    while True:
        try:
            y = np.fromstring(stream.read(frames_per_buffer, exception_on_overflow=False), dtype=np.int16)
            y = y.astype(np.float32)
            callback(y)
            
        except IOError:
            overflows += 1
            if time.time() > prev_ovf_time + 1:
                prev_ovf_time = time.time()
                print('Audio buffer has overflowed {} times'.format(overflows))
    stream.stop_stream()
    stream.close()
    p.terminate()
