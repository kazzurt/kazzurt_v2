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

gain     = dsp.ExpFilter(np.tile(0.01, config.N_FFT_BINS), alpha_decay=0.001, alpha_rise=0.99)
p        = np.tile(1.0, (3, config.N_PIXELS))

arx      = np.linspace(0,len(p[0,:])//50,15).astype(int)
ary      = np.linspace(0,49,50).astype(int)


rtim  = 0

rtim4 = 0


coo  = np.array([1,1,1]).astype(float) #initialize color array, r, g, b
xdiv = 14
ydiv = 49
abc  = 0
dcr  = 0
kz   = 0

arby = np.zeros((config.N_PIXELS//50,50))
rr = rn.randint(2,13)
ry = rn.randint(2,47)

xxs = np.linspace(0,config.N_PIXELS//50-1,config.N_PIXELS//50).astype(int)
yys = np.zeros((1,config.N_PIXELS//50)).astype(int)
yys2 = np.zeros((1,config.N_PIXELS//50)).astype(int)+49
yys3 = np.zeros((1,config.N_PIXELS//50)).astype(int)+24
SS = config.N_PIXELS-1
coll2 = np.linspace(0,SS-100,rn.randint(50,150)).astype(int)
jit = 0
fwd = 1
sl = 0
ccn = 0
fwd2 = 1
qq2 = 0
qq = 0
hg = 0
ffi = 0.3
thresh7 = 3
trip_reset = True
arby_loc = np.zeros((40,25))
oods = np.linspace(1,config.N_PIXELS-1,config.N_PIXELS//2).astype(int)

new_x = [20]
new_y = [40]

x_old = [20]
y_old = [40]
class pongy:
    def pong(y):
        global p, rtim, arx, ary, rtim4, coo, xdiv, ydiv, arby, abc, dcr, xxs, yys, yys2, yys3, oods
        y = y**2
        gain.update(y)
        y /= gain.value
        y *= 255.0
        abc+=1
        rtim+=1
        
        if np.mean(y[2*len(y)//3::])>2 and abc>2 or abc>20: #on at 5 
            abc=0
            
            if dcr == 0:
                arby[xxs,yys] = 0
                arby[xxs,yys2] = 0
                arby[xxs,yys3] = 0
                #xxs += 1
                yys += 1
                yys2-=1
                yys3-=1
            elif dcr == 1:
                arby[xxs,yys] = 0
                arby[xxs,yys2] = 0
                arby[xxs,yys3] = 0
                #xxs -= 1
                yys -= 1
                yys2+=1
                yys3+=1
            if np.max(yys)>=49: #np.max(xxs)>= 12 or 
                dcr = 1
            elif np.min(yys)<=0: #np.min(xxs)<= 2 or 
                dcr = 0
                rtim4+=1
            arby[xxs,yys] = 255
            arby[xxs,yys2] = 255
            arby[xxs,yys3] = 255

        coo[0] = (.5*np.sin(rtim/30)+.5)**.5
        coo[1] = (.5*np.sin(rtim/30+30/3)+.5)**.5
        coo[2] = (.5*np.sin(rtim/30+2*30/3)+.5)**.5
        
        p[0,:] = coo[0]*arby.flatten()
        p[1,:] = coo[1]*arby.flatten()
        p[2,:] = coo[2]*arby.flatten()
        if rtim4>2:
            p[0,oods] = p[1,oods]
            p[1,oods] = p[2,oods]
            p[2,oods] = p[0,oods]
        if rtim4>4:
            rtim4 = 0
        
        p[0,:] = gaussian_filter1d(p[0,:], sigma=1)**1.5
        p[1,:] = gaussian_filter1d(p[1,:], sigma=1)**1.5
        p[2,:] = gaussian_filter1d(p[2,:], sigma=1)**1.5
        
        return p
    def slide(y):
        global p, slide, coll2, jit, fwd, sl, ccn, fwd2, coll3, hg, qq, qq2, ffi, thresh7, SS
        y2 = y**2
        gain.update(y2)
        y2 /= gain.value
        y2 *= 255.0
        m2 = np.mean(y2[28:])
        
        y = np.copy(y)
        gain.update(y)
        y /= gain.value
        sl+=1
        ccn+=1
        
        arq = int(.5*(np.sin(qq/50)+1)*255)
        ty = np.mean(y[:len(y)//2])/np.max(y[:len(y)//2])
        qq2+=1
        qq+=1
        
        if m2>thresh7 or qq>30:
            if qq>5:
                if qq<10:
                    thresh7=1.1*thresh7
                    print("Threshold Change, slide")
                    print(thresh7)
                elif qq>25:
                    thresh7*=.9
                    print("Threshold Change, slide")
                    print(thresh7)
                
                if np.max(coll2) > len(p[0,:])-2:
                    fwd = 0
                if np.min(coll2) < 2:
                    fwd = 1
                
                if fwd == 1:
                    p[:,:] = 0
                    coll2 += 1
                elif fwd == 0:
                    p[:,:] = 0
                    coll2 -= 1
                qq = 0
        if m2>2*thresh7 and qq>15 or qq>60:
            p[:,:] = 0
            coll2 = np.linspace(3,SS-1,rn.randint(50,150)).astype(int)
            ffi = rn.randint(3, 5)/10
        
        p[0,coll2] = int(.5*(np.sin(sl/25+0)+1)*255)
        p[1,coll2] = int(.5*(np.sin(sl/25+25/3)+1)*255)
        p[2,coll2] = int(.5*(np.sin(sl/25+2*25/3)+1)*255)
        
        p[0, :] = gaussian_filter1d(p[0, :], sigma=ffi)
        p[1, :] = gaussian_filter1d(p[1, :], sigma=ffi)
        p[2, :] = gaussian_filter1d(p[2, :], sigma=ffi)
        
        #Reorder colors for half the net
        p2 = 0*p
        p2[0,:] = p[1,:]
        p2[1,:] = p[2,:]
        p2[2,:] = p[0,:]
        
        p[0,:len(p[0,:])//4] = p2[0,3*len(p[1,:])//4::]
        p[1,:len(p[0,:])//4] = p2[1,3*len(p[2,:])//4::]
        p[2,:len(p[0,:])//4] = p2[2,3*len(p[0,:])//4::]
        
        p[0,3*len(p[0,:])//4::] = p2[1,:len(p[1,:])//4]
        p[1,3*len(p[0,:])//4::] = p2[0,:len(p[1,:])//4]
        p[2,3*len(p[0,:])//4::] = p2[2,:len(p[1,:])//4]
        
        return p #typical symmetry about origin
    def rainfall(y):
        global p, rtim, arx, ary, rtim4, coo, xdiv, ydiv, arby2, abc, dcr, xxs, yys, yys2, yys3, oods, trip_reset, arby_loc, x_old, new_x, y_old, new_y
        
        y = y**2
        gain.update(y)
        y /= gain.value
        y *= 255.0
        abc+=1
        rtim+=1
        
        n_points = 60
        time.sleep(.03)
        
        if trip_reset:
            arby_loc = np.zeros((40,25))
            init_x = [np.random.randint(40) for i in range(n_points)]

            init_y = [24 for i in range(n_points)]

            new_x = init_x
            new_y = init_y

            x_old = new_x
            y_old = new_y

            y_zero_check = [100]
            trip_reset = False
        
        arby_loc[x_old,y_old] = 0
        arby_loc[new_x,new_y] = 255
        x_old = new_x
        y_old = new_y
        
        new_x = [x for x in new_x]
        new_y = [max(y-np.random.randint(1,5),0) for y in new_y]
        print(new_y)
        y_zero_check = [y>0 for y in new_y]
        
        if sum(y_zero_check) == 0: 
            trip_reset = True

        coo[0] = (.5*np.sin(rtim/30)+.5)**.5
        coo[1] = (.5*np.sin(rtim/30+30/3)+.5)**.5
        coo[2] = (.5*np.sin(rtim/30+2*30/3)+.5)**.5
        
        p[0,:] = coo[0]*viz_mf.flatMatHardMode(arby_loc)#.flatten()
        p[1,:] = coo[1]*viz_mf.flatMatHardMode(arby_loc)#.flatten()
        p[2,:] = coo[2]*viz_mf.flatMatHardMode(arby_loc)#.flatten()
        print(np.max(arby_loc))
        if rtim4>2:
            p[0,oods] = p[1,oods]
            p[1,oods] = p[2,oods]
            p[2,oods] = p[0,oods]
        if rtim4>4:
            rtim4 = 0
        sig = np.sin(rtim/10)+2 
#         p[0,:] = gaussian_filter1d(p[0,:], sigma=sig)**1.5
#         p[1,:] = gaussian_filter1d(p[1,:], sigma=sig)**1.5
#         p[2,:] = gaussian_filter1d(p[2,:], sigma=sig)**1.5
        
        return p
