from __future__ import print_function
from __future__ import division
import time
import numpy as np
from scipy.ndimage.filters import gaussian_filter1d
import config
import microphone
import dsp
import led
import sys
import numpy as np
from numpy import random as rn
import config
from color_pal import pallette
import viz_mf
import cmdfun
import kzbutfun

gain     = dsp.ExpFilter(np.tile(0.01, config.N_FFT_BINS), alpha_decay=0.001, alpha_rise=0.99)
p_filt   = dsp.ExpFilter(np.tile(1, (3, config.N_PIXELS)), alpha_decay=0.1, alpha_rise=0.99)

pix      = config.N_PIXELS // 2 - 1
co2      = pallette.pal(0)
p        = np.tile(1.0, (3, config.N_PIXELS))
coo      = np.array([1,1,1]).astype(float)
oods     = np.linspace(1,config.N_PIXELS-1,config.N_PIXELS//2).astype(int)
evs      = np.linspace(0,config.N_PIXELS-2,(config.N_PIXELS-1)//2).astype(int)

rtim   = 0
rtim3  = 0
cnt3   = 0
cy     = 0
ard    = 1
cyc    = 0
bthe   = 0
thresh_bthe = 0.5

coo2 = coo

timeCount = 1
countUp   = True
arx       = np.linspace(0,config.N_PIXELS//50-1,config.N_PIXELS//50).astype(int)
ary       = np.linspace(0,49,50).astype(int)
coo3      = np.ones((config.N_PIXELS//50,50))
coo4      = np.ones((config.N_PIXELS//50,50))
coo5      = np.ones((config.N_PIXELS//50,50))
coo6      = np.ones((config.N_PIXELS//50,50))
coo7      = np.ones((config.N_PIXELS//50,50))
coo8      = np.ones((config.N_PIXELS//50,50))
ar_wave0  = np.ones((config.N_PIXELS//50,50))
ar_wave1  = np.ones((config.N_PIXELS//50,50))
ar_wave2  = np.ones((config.N_PIXELS//50,50))
bdir      = 1
nuu       = 50 #defines speed for kuwave2 (higher is slower)
mat_map   = 1
xn        = 14
yn        = 49
upcnt     = 0

class breathe:
        
    def breathe(y):
        global p, p_filt, rtim, pix, arx, ary, ar_wave, phw, rtim3, coo, xdiv, ydiv, cy, oods, evs, xn, yn, upcnt
        y = y**2
        gain.update(y)
        y /= gain.value
        y *= 255.0
        bs = np.mean(y[::len(y)//2])
       
        rtim +=1
        rtim3+=1
        
           
        for x in arx:
            ar_wave0[x,ary] = ((np.sin(ary*np.pi/(49))/2 + np.sin(x*np.pi/(14))/4))*(.5*np.sin(rtim/10+2*x+ary+(bs**.4)/(15-cy))+.5)*255 
            
        if rtim3 >25:
            rtim3 = 0
            cy+=1
        coo[0] = (.5*np.sin(rtim/20)+.5)**.5
        coo[1] = (.5*np.sin(rtim/20+30/3)+.5)**.5
        coo[2] = (.5*np.sin(rtim/20+2*30/3)+.5)**.5
        
        p[0,:] = coo[0]*ar_wave0.flatten()
        p[1,:] = coo[1]*ar_wave0.flatten()
        p[2,:] = coo[2]*ar_wave0.flatten()
        ppm    = np.mean(p[:,:])
        if cy>1:
            p[0,oods] = p[1,oods]
            p[1,oods] = p[2,oods]
            if cy>3:
                p[1,evs] = p[2,evs]
                p[2,evs] = p[0,evs]
                if cy>7:
                    p[1,evs] = p[2,evs]
                    p[2,oods] = p[1,oods]
                    if cy>10:
                        cy = 0
        p = gaussian_filter1d(p, sigma=.2)
#         if lpad[1,56] == 1:
#             upcnt+=1
#             if upcnt>=20:
#                 lpad[1,56] = 0
#                 upcnt      = 0
#             p*= 1.5 * (.5*np.sin(upcnt/20*(np.pi/4) + np.pi/4)+.5)
#         elif lpad[1,54] == 1:
#             lpad[1,54]   = 0
#             p           *=.75
        return p

    