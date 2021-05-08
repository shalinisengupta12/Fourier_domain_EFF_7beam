from __future__ import division
import os, glob
import errno
import sys
import subprocess
import numpy as np
import time
import pandas as pd
import re
sys.path.append('/home/psr/software/sigpyproc')
import sigpyproc
from sigpyproc.Readers import readTim, readDat, FilReader
from joblib import Parallel, delayed
from sigpyproc.Readers import readDat, readTim, FilReader
import itertools
from itertools import combinations



def correlation(x1,x2):
        a1=x1[200:5499800]
        c=np.correlate(a1,x2,mode='valid')
        g=c.argmax()
        a2=x2[200:5499800]
        c1=np.correlate(a2,x1,mode='valid')
        g1=c1.argmax()
        k=0
        m=np.absolute(g-200)
        if m==0:
                #g=g1
                #no delay
                k=0
        else:
                if g>g1:
                #x1 leads x2
                        k=1
                else: #g>g1:
                        k=2
        return m,k

def dedisperse(a,b):
        f=filterbank+'beam%s/'%(b)+pointing+ '_%s'%(b)+'_8bit.fil'
        data=FilReader(f)
        z=data.dedisperse(0)
        return z


if __name__ == '__main__':

        pointing=sys.argv[1]
        filterbank='/home/psr/hercules/scratch/ssengupt/SHALINI_HTRU_North_lowlat/data_files/Test_poitings/' + pointing + '/filterbank_files/'
        beam=['00','01','02','03','04','05','06']
        d0=dedisperse(filterbank, '00')
        d1=dedisperse(filterbank, '01')
        d2=dedisperse(filterbank, '02')
        d3=dedisperse(filterbank, '03')
        d4=dedisperse(filterbank, '04')
        d5=dedisperse(filterbank, '05')
        d6=dedisperse(filterbank, '06')


        z0=d0[0:5500000]
        z1=d1[0:5500000]
        z2=d2[0:5500000]
        z3=d3[0:5500000]
        z4=d4[0:5500000]
        z5=d5[0:5500000]
        z6=d6[0:5500000]

#       val = Parallel(n_jobs = 21)(delayed(correlation)(current_filterbank, number_samples8, mask_file, dm) for dm in np.arange(1808.136, 3002, 7.063))
        t01, k01= correlation(z0,z1)
        t02, k02= correlation(z0,z2)
        t03, k03= correlation(z0,z3)
        t04, k04= correlation(z0,z4)
        t05, k05= correlation(z0,z5)
        t06, k06= correlation(z0,z6)
        t12, k12= correlation(z1,z2)
        t13, k13= correlation(z1,z3)
        t14, k14= correlation(z1,z4)
        t15, k15= correlation(z1,z5)
        t16, k16= correlation(z1,z6)
        t23, k23= correlation(z2,z3)
        t24, k24= correlation(z2,z4)
        t25, k25= correlation(z2,z5)
        t26, k26= correlation(z2,z6)
        t34, k34= correlation(z3,z4)
        t35, k35= correlation(z3,z5)
        t36, k36= correlation(z3,z6)
        t45, k45= correlation(z4,z5)
        t46, k46= correlation(z4,z6)
        t56, k56= correlation(z5,z6)

	c=[[t01,k01,0,1],[t02,k02,0,2],[t03,k03,0,3],[t04,k04,0,4],[t05,k05,0,5],[t06,k06,0,6],[t12,k12,1,2],[t13,k13,1,3],[t14,k14,1,4],[t15,k15,1,5],[t16,k16,1,6],[t23,k23,2,3],[t24,k24,2,4],[t25,k25,2,5],[t26,k26,2,6],[t34,k34,3,4],[t35,k35,3,5],[t36,k36,3,6],[t45,k45,4,5],[t46,k46,4,6],[t56,k56,5,6]]


	a=np.array([len(d0), len(d1), len(d2), len(d3), len(d4), len(d5), len(d6)])
        l=min(a)


        l1=a.argmin()              
	s='/home/psr/hercules/scratch/ssengupt/SHALINI_HTRU_North_lowlat/data_files/Test_poitings/' + pointing+'/%s_corr.txt'%(pointing)
	with open(s,'w') as fh:
		fh.write('%d %d %d %d \n'%(t01,k01,0,1))
		fh.write('%d %d %d %d \n'%(t02,k02,0,2))
		fh.write('%d %d %d %d \n'%(t03,k03,0,3))
		fh.write('%d %d %d %d \n'%(t04,k04,0,4))
		fh.write('%d %d %d %d \n'%(t05,k05,0,5))     
		fh.write('%d %d %d %d \n'%(t06,k06,0,6))
		fh.write('%d %d %d %d \n'%(t12,k12,1,2))
		fh.write('%d %d %d %d \n'%(t13,k13,1,3))
		fh.write('%d %d %d %d \n'%(t14,k14,1,4))
		fh.write('%d %d %d %d \n'%(t15,k15,1,5))
		fh.write('%d %d %d %d \n'%(t16,k16,1,6))
		fh.write('%d %d %d %d \n'%(t23,k23,2,3))
		fh.write('%d %d %d %d \n'%(t24,k24,2,4))
		fh.write('%d %d %d %d \n'%(t25,k25,2,5))
		fh.write('%d %d %d %d \n'%(t26,k26,2,6))
		fh.write('%d %d %d %d \n'%(t34,k34,3,4))
		fh.write('%d %d %d %d \n'%(t35,k35,3,5))
		fh.write('%d %d %d %d \n'%(t36,k36,3,6))
		fh.write('%d %d %d %d \n'%(t45,k45,4,5))
		fh.write('%d %d %d %d \n'%(t46,k46,4,6))
		fh.write('%d %d %d %d \n'%(t56,k56,5,6))

	s1='/home/psr/hercules/scratch/ssengupt/SHALINI_HTRU_North_lowlat/data_files/Test_poitings/' + pointing+'/%s_min_len.txt'%(pointing)
	with open(s1,'w') as fh1:
		fh1.write('%d'%(l))

	fh.close()
	fh1.close()	                                                                                                                                                                                                                                                           
