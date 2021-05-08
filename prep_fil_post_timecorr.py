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



def write_fil(finals,f8,t8,filterbank,beam,kl):
        sum1=0
        for x11 in range(0,512,1):
                for y11 in range(0,kl,1):
                        for z11 in range(0,len(f8),1):
                                if y11==t8[z11] and x11==f8[z11]:
                                        #for z12 in range(-5000,5000,1):
#                                                sum1=sum1+finals[y11+z12][x11]
										 #                                       avg=sum1/10000
                                        finals[y11][x11]=np.median(finals[:,x11])


        dat=FilReader(filterbank+'/beam0%s/'%(beam)+pointing+ '_%s'%(b)+'_8bit.fil')
        s11=dat.header.prepOutfile(filterbank+'/beam0%s/new.fil'%(beam),nbits=8)
        s.cwrite(finals.ravel())
        s.close()



def write_samps_bad(f8,filterbank1,beam):
	with open(filterbank1+'beam%s/'%(beam)+'bad_new2_time_samps.txt', 'a') as fh:	
		for i in range(0, len(f8), 1):
			fh.write('%d \n'%(f8[i]))

	fh.close()






















if __name__ == '__main__':
		
	pointing=sys.argv[1]
	beam=sys.argv[2]
	filterbank='/home/psr/hercules/scratch/ssengupt/SHALINI_HTRU_North_lowlat/data_files/Test_poitings/' + pointing + '/filterbank_files/beam%s/' %str(beam) + pointing + '_%s_' %str(beam) +'8bit.fil'
	g='/home/psr/hercules/scratch/ssengupt/SHALINI_HTRU_North_lowlat/data_files/Test_poitings/' + pointing + '/filterbank_files/beam%s/' %str(beam) + pointing + '_%s_' %str(beam) +'8bit_random_noise_all_beam.fil'

	k1='/home/psr/hercules/scratch/ssengupt/SHALINI_HTRU_North_lowlat/data_files/Test_poitings/' + pointing + '/filterbank_files/beam%s/' %str(beam) + pointing + '_%s_' %str(beam) +'8bit_original_obs1.fil'

	cmds='cat /home/psr/hercules/scratch/ssengupt/SHALINI_HTRU_North_lowlat/data_files/Test_poitings/' + pointing + '/filterbank_files/beam%s/bad*.txt > /home/psr/hercules/scratch/ssengupt/SHALINI_HTRU_North_lowlat/data_files/Test_poitings/'%str(beam) + pointing + '/filterbank_files/beam%s/combo_4567.txt' %str(beam)
	log = subprocess.check_output(cmds,shell=True)
	print log

	c='/home/psr/hercules/scratch/ssengupt/SHALINI_HTRU_North_lowlat/data_files/Test_poitings/' + pointing + '/filterbank_files/beam%s/combo_4567.txt' %str(beam)
	l3=np.loadtxt(c,dtype=int)
        l=[]

        for i in range(0, len(l3), 1):
                a=l3[i]
                if a not in l:
                        l.append(a)
	
	cmds= 'mv ' +filterbank +' '+k1
	log = subprocess.check_output(cmds,shell=True)
        print log
	

#	dat=FilReader(filterbank+'beam%s/'%(b)+pointing+ '_%s'%(b)+'_8bit.fil')
	dat=FilReader(k1)
        fil=dat.readPlan(10000, skipback=0, start=0, nsamps=None, verbose=True)
        filar=[]
        for nsamps, ii, data in fil:
                data = data.reshape(nsamps,dat.header.nchans)
                filar.append(data)

        w=np.concatenate(filar,axis=0)
        print np.shape(w)

	print 'no.of unique bad bins is ,',len(l)	

	d=dat.dedisperse(0)
	y1=np.median(d)
	b=np.where((d>(y1-0.4)) & (d<(y1+0.4)))[0]
	#z=np.where(d>(np.median(d)+(3*np.std(d))))[0]
	#print z
	print b[0]	
	y=y1/512
	print 'replacement value is emdian timeseries/512, ',y
	print l[0]	
	
	'''for k in range(0,len(z),1):
                for j in range(0,512,1):
                        w[z[k],j]=w[b[0],j]'''



	for k in range(0,len(l),1):
		for j in range(0,512,1):
			w[l[k],j]=w[b[0],j]
		#	if (w[l[k],j]>y):
		#		w[l[k],j]=y
#	print w[l[0],:]
	s=dat.header.prepOutfile(filterbank,nbits=8)
        s.cwrite(w.ravel())
        s.close()
	
	

# l stores the bad time samps uniquely
	


