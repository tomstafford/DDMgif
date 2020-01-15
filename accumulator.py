#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Same as ddm_gif.py but modified to make the figure for the paper resubmission

Uses python 3 and runs on linux

Conda environment saved in munge.yml
"""

import matplotlib.pyplot as plt #plotting
import numpy as np #number functions

nrange=100 #points on x axis

#change these parameters to get different traces
noise_scale=0.35 #how much noise on our underlying evidence accumulation curves
seedn=31267124
y1drift=0.05
y2drift=0.02
np.random.seed(seedn) 

#change these parameters to change the animation
flashn=3
waitn=4
endhold=8

#figure parameters
t1=2 #threshold 1
t2=6 #threshold 2
imgh=460 #assumption about figure size in pixels
imgw=640#assumption about figure size in pixels
lw=2 #linewidth for accumulation
tw=1 #linewidth for thresholds


#generate random accumulation paths
x= range(nrange)

#initialise empty array
y1=np.array([0.0]*nrange)    
y2=np.array([0.0]*nrange)

#generate the random paths
for i in range(1,nrange):
    y1[i] = y1[i-1]+np.random.randn()*noise_scale+y1drift
    y2[i] = y2[i-1]+np.random.randn()*noise_scale+y2drift

#make the plot
fig, ax = plt.subplots()
plt.xlabel('Time')
plt.ylabel('Cumulative weight of evidence')
plt.xticks([]) #hide tick labels
plt.yticks([]) #hide tick labels
plt.ylim([-8,8])


#upper threshold
plt.plot([0,nrange],[t2,t2],'--',color='k',lw=tw)
ann1 = plt.annotate('Decide A',xy=(0, t2+0.5),xycoords='data')

#lower threshold
plt.plot([0,nrange],[-t2,-t2],'--',color='k',lw=tw)
ann2 = plt.annotate('Decide B',xy=(0, -t2-0.8),xycoords='data')
    
#make axes invisible    
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)


i=np.argmax(abs(y1)>t2)+1
plt.plot(x[:i],y1[:i],'blue',ls='-',lw=lw)

##path 2 in red
#m=np.argmax(abs(y2)>t2)+1
#plt.plot(x[:m],y2[:m],'red',ls='-',lw=lw)

#name for saving gif
name='accumulator_'+str(seedn)+'_'+str(noise_scale).replace('.','p')+'.png'
name='accumulator.png'

#fig, ax = plt.subplots(figsize=(10, 5))
plt.savefig(name,bbox_inches='tight')