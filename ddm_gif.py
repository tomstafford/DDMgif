#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Make animated gif of evidence accumulation

Uses python 3 and runs on linux

Conda environment saved in munge.yml
"""

import matplotlib.pyplot as plt #plotting
import numpy as np #number functions
import os

#assumes there is a subdirectory /frames
os.system('rm frames/*.png') #clear saved frames

nrange=100 #points on x axis

#change these parameters to get different traces
noise_scale=0.8 #how much noise on our underlying evidence accumulation curves
seedn=7
y1drift=0.1 
y2drift=-0.067
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
plt.xlabel('Time (arbitrary units)')
plt.ylabel('Cumulative subjective value (arbitrary units)')
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

#generate frames for gif and save them in /frames


#path 1 in blue
i=0
uncrossed=True
while uncrossed:
    plt.plot(x[:i],y1[:i],'blue',ls='-',lw=lw)
    plt.savefig('frames/'+str(i).zfill(3)+'.png',bbox_inches='tight')
    if (i>1) & (y1[i-1]>t2):
        uncrossed=False
        Aend=i
    i+=1

#flash threshold when it is crossed

for j in range(flashn):
    plt.plot([0,nrange],[t2,t2],'--',color='white',lw=tw)
    ann1.remove()
    for k in range(waitn):
        plt.savefig('frames/'+str(i).zfill(3)+'.png',bbox_inches='tight');i+=1

    plt.plot([0,nrange],[t2,t2],'--',color='k',lw=tw)
    ann1=plt.annotate('Decide A',xy=(0, t2+0.5),color='k',xycoords='data')
    for k in range(waitn):
        plt.savefig('frames/'+str(i).zfill(3)+'.png',bbox_inches='tight');i+=1

plt.plot(x[:Aend],y1[:Aend],'white',ls='-',lw=lw)


#path 2 in red
m=0
uncrossed=True
while uncrossed:
    plt.plot(x[:m],y2[:m],'red',ls='-',lw=lw)
    plt.savefig('frames/'+str(i).zfill(3)+'.png',bbox_inches='tight')
    if (m>1) & (y2[m-1]<-t2):
        uncrossed=False
    i+=1;m+=1

#flash threshold
for j in range(flashn):
    plt.plot([0,nrange],[-t2,-t2],'--',color='white',lw=tw)
    ann2.remove()
    for k in range(waitn):
        plt.savefig('frames/'+str(i).zfill(3)+'.png',bbox_inches='tight');i+=1

    plt.plot([0,nrange],[-t2,-t2],'--',color='k',lw=tw)
    ann2=plt.annotate('Decide B',xy=(0, -t2-0.8),color='k',xycoords='data')
    for k in range(waitn):
        plt.savefig('frames/'+str(i).zfill(3)+'.png',bbox_inches='tight');i+=1


#hold the final picture for a few frames
for j in range(endhold):
    plt.savefig('frames/'+str(i).zfill(3)+'.png',bbox_inches='tight');i+=1


#name for saving gif
name='ddm_'+str(seedn)+'_'+str(noise_scale).replace('.','p')+'.gif'

#assumes you have ffmpeg installed 
os.system('convert -delay 9 frames/*.png ' + name)
#fig, ax = plt.subplots(figsize=(10, 5))
