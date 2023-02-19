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
import pygame
import kzbutfun
import scipy.special as sp
gain     = dsp.ExpFilter(np.tile(0.01, config.N_FFT_BINS), alpha_decay=0.001, alpha_rise=0.99)
pix      = config.N_PIXELS 
p        = np.tile(1.0, (3, config.N_PIXELS))
coo      = np.array([1,1,1]).astype(float)

coms     = cmdfun.pygrun()  #keyboard commands

pl = np.linspace(0,pix-1,pix).astype(int)*4

arx         = np.linspace(0,config.ARX-1,config.ARX).astype(int)
ary         = np.linspace(0,config.ARY-1,config.ARY).astype(int)
red_ar      = np.zeros((config.ARX,config.ARY))
gre_ar      = np.zeros((config.ARX,config.ARY))
blu_ar      = np.zeros((config.ARX,config.ARY))
tim=0
k = 2
rtim11 = 0
class bessel1:
    
    def bessel1(y):
            global p, pix, arx, ary, red_ar, gre_ar, blu_ar, pl, tim, k, rtim11
            
            tim+=k
            B = ((sp.jv(1,pl)+.4)/1.4)*255

            ys = 5#5*np.sin(tim/50)+10
            xs = 5# 5*np.sin(tim/50)+15
            for i in arx:
                red_ar[i,ary] = (sp.jv(1,(i-xs)*(ary-ys)/20)+.33)*255
                blu_ar[i,ary] = (sp.jv(1,(i-xs)*(ary-ys)/20)+.33)*255
                gre_ar[i,ary] = (sp.jv(1,(i-xs)*(ary-ys)/20)+.33)*255           



            p[0,:] = viz_mf.flatMatHardMode(red_ar)
            p[1,:] = viz_mf.flatMatHardMode(gre_ar)
            p[2,:] = viz_mf.flatMatHardMode(blu_ar)
            print(p)
            if tim>100 or tim == 0:
                k*=-1
            
            return p


