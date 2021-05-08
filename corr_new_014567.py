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


def getting_channel(b):
	f=filterbank+'beam%s/'%(b)+pointing+ '_%s'%(b)+'_8bit.fil'
	data=FilReader(f)
	z=data.dedisperse(0)
	return z
	
def splitFil(filterbank, l2):
	for beam in ['00','01','02','03','04','05','06']:
		f1=filterbank+'beam%s/'%(beam)+pointing+ '_%s'%(beam)+'_8bit.fil'
		data=FilReader(f1)
		z1=data.split(0,l2, filename=filterbank+'beam%s/'%(beam)+pointing+ '_%s'%(beam)+'_s8bit.fil')
		
def prep_fil(filterbank, b):
	dat=FilReader(filterbank+'beam%s/'%(b)+pointing+ '_%s'%(b)+'_8bit.fil')
	fil=dat.readPlan(10000, skipback=0, start=0, nsamps=None, verbose=True)
	filar=[]
	for nsamps, ii, data in fil:
		data = data.reshape(nsamps,dat.header.nchans)
		filar.append(data)

	w=np.concatenate(filar,axis=0)
	return w





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
	with open(filterbank1+'beam%s/'%(beam)+'bad_01_all_samps_comb.txt', 'a') as fh:	
		for i in range(0, len(f8), 1):
			fh.write('%d \n'%(f8[i]))

	fh.close()


def four_beam(p, p0, p1, p2, p3, p4, p5 ,p6, s0, s1, s2, s3, s4, s5, s6, n0, n1, n2, n3, n4, n5, n6):
        ch=c0=c1=c2=c3=c4=c5=c6=1
        m0=m1=m2=m3=m4=m5=m6=0
#       if p[0]>=4.16 and p[1]>=4.16 and p[2]>=4.16 and p[3]>=4.16:
        if p0 not in p:
                c0=0
        if p1 not in p:
                c1=0
        if p2 not in p:
                c2=0
        if p3 not in p:
                c3=0
        if p4 not in p:
                c4=0
        if p5 not in p:
                c5=0
        if p6 not in p:
                c6=0

        if c0==1:
                if p0>(n0+(2.3*s0)):
                        m0=1
        if c1==1:
                if p1>(n1+(2.3*s1)):
                        m1=1
        if c2==1:
                if p2>(n2+(2.3*s2)):
                        m2=1
	if c3==1:
                if p3>(n3+(2.3*s3)):
                        m3=1
	if c4==1:
                if p4>(n4+(2.3*s4)):
                        m4=1
	if c5==1:
                if p5>(n5+(2.3*s5)):
                        m5=1
	if c6==1:
                if p6>(n6+(2.3*s6)):
                        m6=1

	m=[m0,m1,m2,m3,m4,m5,m6]
	mo=np.array(m)
	x=np.where(mo==1)[0]
	if len(x)==4:
		ch=1
	else:
		ch=0

	return ch,m0,m1,m2,m3,m4,m5,m6


def five_beam(p, p0, p1, p2, p3, p4, p5 ,p6, s0, s1, s2, s3, s4, s5, s6, n0, n1, n2, n3, n4, n5, n6):
        ch=c0=c1=c2=c3=c4=c5=c6=1
        m0=m1=m2=m3=m4=m5=m6=0
#       if p[0]>=4.16 and p[1]>=4.16 and p[2]>=4.16 and p[3]>=4.16:
        if p0 not in p:
                c0=0
        if p1 not in p:
                c1=0
        if p2 not in p:
                c2=0
        if p3 not in p:
                c3=0
        if p4 not in p:
                c4=0
        if p5 not in p:
                c5=0
        if p6 not in p:
                c6=0

        if c0==1:
                if p0>(n0+(2.05*s0)):
                        m0=1
        if c1==1:
                if p1>(n1+(2.05*s1)):
                        m1=1
        if c2==1:
                if p2>(n2+(2.05*s2)):
                        m2=1
        if c3==1:
                if p3>(n3+(2.05*s3)):
                        m3=1
        if c4==1:
                if p4>(n4+(2.05*s4)):
                        m4=1
        if c5==1:
                if p5>(n5+(2.05*s5)):
                        m5=1
        if c6==1:
                if p6>(n6+(2.05*s6)):
                        m6=1

        m=[m0,m1,m2,m3,m4,m5,m6]
        mo=np.array(m)
        x=np.where(mo==1)[0]
        if len(x)==5:
                ch=1
        else:
                ch=0

        return ch,m0,m1,m2,m3,m4,m5,m6


def six_beam(p, p0, p1, p2, p3, p4, p5 ,p6, s0, s1, s2, s3, s4, s5, s6, n0, n1, n2, n3, n4, n5, n6):
        ch=c0=c1=c2=c3=c4=c5=c6=1
        m0=m1=m2=m3=m4=m5=m6=0
#       if p[0]>=4.16 and p[1]>=4.16 and p[2]>=4.16 and p[3]>=4.16:
        if p0 not in p:
                c0=0
        if p1 not in p:
                c1=0
        if p2 not in p:
                c2=0
        if p3 not in p:
                c3=0
        if p4 not in p:
                c4=0
        if p5 not in p:
                c5=0
        if p6 not in p:
                c6=0

        if c0==1:
                if p0>(n0+(1.64*s0)):
                        m0=1
        if c1==1:
                if p1>(n1+(1.64*s1)):
                        m1=1
        if c2==1:
                if p2>(n2+(1.64*s2)):
                        m2=1
        if c3==1:
                if p3>(n3+(1.64*s3)):
                        m3=1
        if c4==1:
                if p4>(n4+(1.64*s4)):
                        m4=1
        if c5==1:
                if p5>(n5+(1.64*s5)):
                        m5=1
        if c6==1:
                if p6>(n6+(1.64*s6)):
                        m6=1

        m=[m0,m1,m2,m3,m4,m5,m6]
        mo=np.array(m)
        x=np.where(mo==1)[0]
        if len(x)==6:
                ch=1
        else:
                ch=0

        return ch,m0,m1,m2,m3,m4,m5,m6



def seven_beam(p, p0, p1, p2, p3, p4, p5 ,p6, s0, s1, s2, s3, s4, s5, s6, n0, n1, n2, n3, n4, n5, n6):
        ch=c0=c1=c2=c3=c4=c5=c6=1
        m0=m1=m2=m3=m4=m5=m6=0
#       if p[0]>=4.16 and p[1]>=4.16 and p[2]>=4.16 and p[3]>=4.16:
        if p0 not in p:
                c0=0
        if p1 not in p:
                c1=0
        if p2 not in p:
                c2=0
        if p3 not in p:
                c3=0
        if p4 not in p:
                c4=0
        if p5 not in p:
                c5=0
        if p6 not in p:
                c6=0

        if c0==1:
                if p0>(n0+(1.4*s0)):
                        m0=1
        if c1==1:
                if p1>(n1+(1.4*s1)):
                        m1=1
        if c2==1:
                if p2>(n2+(1.4*s2)):
                        m2=1
        if c3==1:
                if p3>(n3+(1.4*s3)):
                        m3=1
        if c4==1:
                if p4>(n4+(1.4*s4)):
                        m4=1
        if c5==1:
                if p5>(n5+(1.4*s5)):
                        m5=1
        if c6==1:
                if p6>(n6+(1.4*s6)):
                        m6=1

        m=[m0,m1,m2,m3,m4,m5,m6]
        mo=np.array(m)
        x=np.where(mo==1)[0]
        if len(x)==7:
                ch=1
        else:
                ch=0

        return ch,m0,m1,m2,m3,m4,m5,m6
























if __name__ == '__main__':
		
	pointing=sys.argv[1]
	filterbank='/home/psr/hercules/scratch/ssengupt/SHALINI_HTRU_North_lowlat/data_files/Test_poitings/' + pointing + '/filterbank_files/'
	beam=['00','01','02','03','04','05','06']
	c=np.loadtxt('/home/psr/hercules/scratch/ssengupt/SHALINI_HTRU_North_lowlat/data_files/Test_poitings/' + pointing + '/' +  pointing+'_corr.txt',dtype=int)
	l3=np.loadtxt('/home/psr/hercules/scratch/ssengupt/SHALINI_HTRU_North_lowlat/data_files/Test_poitings/' + pointing + '/' +  pointing+'_min_len.txt',dtype=int)
	l=int(l3)

	t0=[]
	t1=[]
	t2=[]
	t3=[]
	t4=[]
	t5=[]
	t6=[]
	bf0=[]
	bf1=[]
	bf2=[]
	bf3=[]
	bf4=[]
	bf5=[]
	bf6=[]
	
	hel=max(c[:,0])
	print (hel)	
#	for i in range(0,2,1):
	final0=getting_channel('00')		
	final1=getting_channel('01')
	final2=getting_channel('02')
	final3=getting_channel('03')
	final4=getting_channel('04')
	final5=getting_channel('05')
	final6=getting_channel('06')
	cor=[]
	for z1 in range(0,21,1):
        	q=c[z1]
                if c[z1][2]==0 and c[z1][3]==1:
                	cor.append(c[z1])
		if c[z1][2]==1 and c[z1][3]==2:
                        cor.append(c[z1])
		if c[z1][2]==1 and c[z1][3]==3:
                        cor.append(c[z1])
		if c[z1][2]==1 and c[z1][3]==4:
                        cor.append(c[z1])
		if c[z1][2]==1 and c[z1][3]==5:
                        cor.append(c[z1])
		if c[z1][2]==1 and c[z1][3]==6:
                        cor.append(c[z1])

	print cor		


	corr=[]                                        
	if cor[0][1]==1: 
		corr.append(cor[0][0]*(-1))
	elif cor[0][1]==2:
		corr.append(cor[0][0])
	else:
		corr.append(0)   #b0
	
	if cor[1][1]==1:
                corr.append(cor[1][0])
        elif cor[1][1]==2:
                corr.append(cor[1][0]*(-1))
        else:
                corr.append(0)   #b2

	if cor[2][1]==1:
                corr.append(cor[2][0])
        elif cor[2][1]==2:
                corr.append(cor[2][0]*(-1))
        else:
                corr.append(0)   #b3

	if cor[3][1]==1:
                corr.append(cor[3][0])
        elif cor[3][1]==2:
                corr.append(cor[3][0]*(-1))
        else:
                corr.append(0)   #b4

	if cor[4][1]==1:
                corr.append(cor[4][0])
        elif cor[4][1]==2:
                corr.append(cor[4][0]*(-1))
        else:
                corr.append(0)    #b5

	if cor[5][1]==1:
                corr.append(cor[5][0])
        elif cor[5][1]==2:
                corr.append(cor[5][0]*(-1))
        else:
                corr.append(0)    #b6

	print corr	
	
	ff0=[]
	ff1=[]
	ff2=[]
	ff3=[]
	ff4=[]
	ff5=[]
	ff6=[]


	for f in range(hel, l-hel, 1):
		ff0.append(final0[f-corr[0]])
		ff2.append(final2[f-corr[1]])
		ff3.append(final3[f-corr[2]])
		ff4.append(final4[f-corr[3]])
		ff5.append(final5[f-corr[4]])
		ff6.append(final6[f-corr[5]])

	fin0=np.array(ff0)
	fin1=np.array(final1[hel:l-hel])
	fin2=np.array(ff2)
	fin3=np.array(ff3)
	fin4=np.array(ff4)
	fin5=np.array(ff5)
	fin6=np.array(ff6)

	d1=np.add(fin0,fin1)
	d2=np.add(d1,fin2)
	d3=np.add(d2,fin3)
	d4=np.add(d3,fin4)
	d5=np.add(d4,fin5)
	d=np.add(d5,fin6)
	

	sm=np.median(d)
	sd=np.std(d)
	
	
	bins=np.where(d>(sm+(1.5*sd)))[0]
	#bins=bins+hel #to get the real bin value from the start

	
	sd0=np.std(final0)                                                #taking the standard deviation for each channel for comparison of time samples
        sd1=np.std(final1)
        sd2=np.std(final2)
        sd3=np.std(final3)
        sd4=np.std(final4)
        sd5=np.std(final5)
        sd6=np.std(final6)
	md0=np.median(final0)
	md1=np.median(final1)
	md2=np.median(final2)
	md3=np.median(final3)
	md4=np.median(final4)
	md5=np.median(final5)
	md6=np.median(final6)



	for i in range(0,len(bins),1):
		j=bins[i]
		counter=0
		counter0=0
		counter1=0
		counter2=0
		counter3=0
		counter4=0
		counter5=0
		counter6=0
		a=[fin0[j], fin1[j],fin2[j],fin3[j],fin4[j],fin5[j],fin6[j]]
		b=list(itertools.combinations(a, 4))
		for mm in range(0, len(b), 1):
			r, r0, r1, r2, r3, r4, r5, r6=four_beam(b[mm], fin0[j], fin1[j], fin2[j], fin3[j], fin4[j], fin5[j], fin6[j], sd0,sd1,sd2,sd3,sd4,sd5,sd6,md0,md1,md2,md3,md4,md5,md6)

			counter=counter+r
                        counter0=counter0+r0
                        counter1=counter1+r1
                        counter2=counter2+r2
                        counter3=counter3+r3
                        counter4=counter4+r4
                        counter5=counter5+r5
                        counter6=counter6+r6

		ddd=1

                if counter==0:
                        ddd=0
                else:
                        
                        if counter0>0:
                                bf0.append(j+hel-corr[0])
                        if counter1>0:
                                bf1.append(j+hel)
                        if counter2>0:
                                bf2.append(j+hel-corr[1])
                        if counter3>0:
                                bf3.append(j+hel-corr[2])
                        if counter4>0:
                                bf4.append(j+hel-corr[3])
                        if counter5>0:
                                bf5.append(j+hel-corr[4])
                        if counter6>0:
                                bf6.append(j+hel-corr[5])
#                        bad_freq.append(j+hel)



# ============================================================================== 5 beam comaprison =======================================================================================================




		count=0
		count0=0
		count1=0
		count2=0
		count3=0
		count4=0
		count5=0
		count6=0
		a=[fin0[j], fin1[j],fin2[j],fin3[j],fin4[j],fin5[j],fin6[j]]
		bb=list(itertools.combinations(a, 5))
		for mm0 in range(0, len(bb), 1):
			rr, rr0, rr1, rr2, rr3, rr4, rr5, rr6=five_beam(bb[mm0], fin0[j], fin1[j], fin2[j], fin3[j], fin4[j], fin5[j], fin6[j], sd0,sd1,sd2,sd3,sd4,sd5,sd6,md0,md1,md2,md3,md4,md5,md6)

			count=count+rr
                        count0=count0+rr0
                        count1=count1+rr1
                        count2=count2+rr2
                        count3=count3+rr3
                        count4=count4+rr4
                        count5=count5+rr5
                        count6=count6+rr6

		dd0=1

                if count==0:
                        dd0=0
                else:
                        


                        if count0>0:
                                bf0.append(j+hel-corr[0])
                        if count1>0:
                                bf1.append(j+hel)
                        if count2>0:
                                bf2.append(j+hel-corr[1])
                        if count3>0:
                                bf3.append(j+hel-corr[2])
                        if count4>0:
                                bf4.append(j+hel-corr[3])
                        if count5>0:
                                bf5.append(j+hel-corr[4])
                        if count6>0:
                                bf6.append(j+hel-corr[5]) 
		



# ============================================================================== 6 beam comparison ======================================================================================================


		coun=0
		coun0=0
		coun1=0
		coun2=0
		coun3=0
		coun4=0
		coun5=0
		coun6=0
		a=[fin0[j], fin1[j],fin2[j],fin3[j],fin4[j],fin5[j],fin6[j]]
		bb1=list(itertools.combinations(a, 6))
		for mm1 in range(0, len(bb1), 1):
			ss, ss0, ss1, ss2, ss3, ss4, ss5, ss6=six_beam(bb1[mm1], fin0[j], fin1[j], fin2[j], fin3[j], fin4[j], fin5[j], fin6[j], sd0,sd1,sd2,sd3,sd4,sd5,sd6,md0,md1,md2,md3,md4,md5,md6)

			coun=coun+ss
                        coun0=coun0+ss0
                        coun1=coun1+ss1
                        coun2=coun2+ss2
                        coun3=coun3+ss3
                        coun4=coun4+ss4
                        coun5=coun5+ss5
                        coun6=coun6+ss6

		dd1=1

                if coun==0:
                        dd1=0
                else:
                        
                        if coun0>0:
                                bf0.append(j+hel-corr[0])
                        if coun1>0:
                                bf1.append(j+hel)
                        if coun2>0:
                                bf2.append(j+hel-corr[1])
                        if coun3>0:
                                bf3.append(j+hel-corr[2])
                        if coun4>0:
                                bf4.append(j+hel-corr[3])
                        if coun5>0:
                                bf5.append(j+hel-corr[4])
                        if coun6>0:
                                bf6.append(j+hel-corr[5])
		

# ========================================================================== 7 beam comparison =============================================================================================================

		cou=0
		cou0=0
		cou1=0
		cou2=0
		cou3=0
		cou4=0
		cou5=0
		cou6=0
		a=[fin0[j], fin1[j],fin2[j],fin3[j],fin4[j],fin5[j],fin6[j]]
		bb2=list(itertools.combinations(a, 7))
		for mm2 in range(0, len(bb2), 1):
			tt, tt0, tt1, tt2, tt3, tt4, tt5, tt6=seven_beam(bb2[mm2], fin0[j], fin1[j], fin2[j], fin3[j], fin4[j], fin5[j], fin6[j], sd0,sd1,sd2,sd3,sd4,sd5,sd6,md0,md1,md2,md3,md4,md5,md6)

			cou=cou+tt
                        cou0=cou0+tt0
                        cou1=cou1+tt1
                        cou2=cou2+tt2
                        cou3=cou3+tt3
                        cou4=cou4+tt4
                        cou5=cou5+tt5
                        cou6=cou6+tt6

		dd2=1

                if cou==0:
                        dd2=0
                else:
                        
                        if cou0>0:
                                bf0.append(j+hel-corr[0])
                        if cou1>0:
                                bf1.append(j+hel)
                        if cou2>0:
                                bf2.append(j+hel-corr[1])
                        if cou3>0:
                                bf3.append(j+hel-corr[2])
                        if cou4>0:
                                bf4.append(j+hel-corr[3])
                        if cou5>0:
                                bf5.append(j+hel-corr[4])
                        if cou6>0:
                                bf6.append(j+hel-corr[5])
		
















#final step outputting the modified filterbank files


	write_samps_bad(bf0,filterbank,'00')
	write_samps_bad(bf1,filterbank,'01')
	write_samps_bad(bf2,filterbank,'02')
	write_samps_bad(bf3,filterbank,'03')
	write_samps_bad(bf4,filterbank,'04')
	write_samps_bad(bf5,filterbank,'05')
	write_samps_bad(bf6,filterbank,'06')


	print ('for 0 beam:freq, time ',len(bf0),  (len(bf0)/33554432)*100)
        print ('for 1 beam:freq, time ',len(bf1), (len(bf1)/33554432)*100)
	print ('for 2 beam:freq, time ',len(bf2), (len(bf2)/33554432)*100)
	print ('for 3 beam:freq, time ',len(bf3), (len(bf3)/33554432)*100)
	print ('for 4 beam:freq, time ',len(bf4), (len(bf4)/33554432)*100)
	print ('for 5 beam:freq, time ',len(bf5), (len(bf5)/33554432)*100)
	print ('for 6 beam:freq, time ',len(bf6),  (len(bf6)/33554432)*100)

