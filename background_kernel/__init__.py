'''
创建一个类，
'''
from .WhittakerSmooth import WhittakerSmooth
import numpy as np
from ..time_unified import Time_transform


class Baseline_in_time(object):

	def __init__(self,time,value,fitness = 'r',hardness = False):
		self.time = time
		self.value = value
		self.t_transform = Time_transform(time,value)
		self.unified_time,self.unified_value = self.t_transform.to_unified_time()

		self.AirPLS = AirPLS(self.unified_value,hardness = hardness)
		cc = {#'double':self.AirPLS.double_airPLS(),'bottom':self.AirPLS.bottom_airPLS(),
		      'r':TD_baseline(self.unified_time,self.unified_value)}
		self.unified_bs = cc[fitness]
		self.bs = self.t_transform.to_actual_time(self.unified_time,self.unified_bs)[1]
		self.cs = self.value-self.bs

	def get_value(self):
		return self.time,self.cs,self.bs


	def get_bs(self):
		return self.bs

	def get_cs(self):
		return self.cs

	def get_airPLS(self):
		return self.AirPLS




class AirPLS(object):

	def __init__(self,x,hardness = False):
		self.b_index = np.isnan(x)
		self.x = np.array(x)

		self.m = self.x.shape[0]

		self.w = np.ones(self.m)
		if (True in self.b_index):
			print('数据输入存在存在无效值')
			self.x[self.b_index] = 0
			self.w[self.b_index] = 0

		if hardness:
			self.x = WhittakerSmooth(self.x,self.w,4)

	def trag(self,x,arg = 5):
		'''
		激活函数
		:param x:
		:param arg:
		:return:
		'''
		arg = 5/arg
		x = x*arg

		return (np.exp(x)-np.exp(-x))/(np.exp(x)+np.exp(-x))

	def w_pp(self,w,rang = 9,f = 18):
		'''
		对权重进行操作
		该过程合并了权重比较琐碎的区域。
		:param w: 权重
		:param rang:
		:param f:
		:return: 权重
		'''

		num_w = w.size
		ff = 0
		ff1 =  0
		first = True
		rem_index = 0
		rem_index2 = 0
		rem_valu = 0
		for i in range(num_w-1):
			if(w[i] == w[i+1]):
				ff = ff + 1
				#valu = w[i]

			else:

				if first == False:
					if(w[i] == 1):
						F = (self.trag(ff,rang)-self.trag(ff1,rang))*f
					else:
						F = (self.trag(ff,rang)-self.trag(ff1,rang))*f
					change_num = int(F)
					if(change_num > 0):
						if(rem_index-change_num<rem_index2):
							nnn = rem_index2
						else:
							nnn = rem_index-change_num
						change_index = np.arange(nnn,rem_index+1,1)
						w[change_index] = w[i]

					elif(change_num < 0):
						if(rem_index-change_num>=i):
							nnn = i+1
						else:
							nnn = rem_index-change_num+1

						change_index = np.arange(rem_index,nnn,1)
						w[change_index] = rem_valu

				rem_index2 = rem_index
				rem_index = i
				rem_valu = w[i]
				ff1 = ff
				ff = 0
				first = False
		return w

	def double_airPLS(self):

		'''
		airPLS 核心过程。
		:return:
		'''

		w = self.w
		bs = WhittakerSmooth(self.x,w,100)
		cs = self.x - bs
		cs_mean = cs.mean()
		cs_std = cs.std()
		for i in range(40):
			cs_index = np.where((cs>cs_mean+(1+0.0*i)*cs_std)|(cs<cs_mean-(1+0.0*i)*cs_std))
			cs1 = cs
			w[cs_index] = 0
			w = self.w_pp(w,rang = 5,f = 9)
			w = self.w_pp(w,rang = 10,f = 18)#rang = 10,f = 18
			w[self.b_index] = 0	#忽略无效值

			bs = WhittakerSmooth(self.x,w,100)
			cs = self.x - bs
			drti = ((cs1-cs)**2).mean()
			if(drti <0.1):
				break
			if(len(w[w!=0]) < self.m * 0.1):
				#print('baseline 采样区间小于总区间的 10%，可能出现过拟合。建议检查拟合情况。')
				break
			cs_mean = cs[w!=0].mean()
			cs_std = cs[w!=0].std()

		return bs
	def bottom_airPLS(self):

		w = self.w
		bs = WhittakerSmooth(self.x,w,100)
		cs = self.x - bs
		dssn = np.abs(cs[cs < 0].sum())
		for i in range(20):
			if(dssn <0.05*(abs(self.x)).sum() or i == 20-1):
				#print('%%',i)
				break
			w[cs>0] = 0
			w[cs<0] = 1*np.exp(i*np.abs(cs[cs<0])/dssn)
			w[0] = np.exp(i*(cs[cs<0]).max()/dssn)
			w[-1] = w[0]
			bs = WhittakerSmooth(self.x, w, 100)
			cs = self.x - bs

		return bs



def TD_baseline(time,rate,lam = None,hwi = None,it = None,inti = None):
	dt = time[1]-time[0]

	if(lam is None):
		lam = 100/dt
	if(hwi is None):
		hwi = int(20/dt)
	if(it is None):
		it = 5
	if(inti is None):

		fillpeak_int = int(len(rate)/10)

	else:
		fillpeak_int =inti
	if(lam < 1):
		lam = 1
	bs = baseline(rate,lambda_=lam,hwi=hwi,it = it,int_ = fillpeak_int)
	return bs


def get_smooth(spectra,lambda_):
	spectra = np.array(spectra)
	m = spectra.shape[0]
	w = np.ones(m)
	smooth = WhittakerSmooth(spectra,w,lambda_)
	cs = spectra-smooth
	cs_mean = cs.mean()
	cs_std = cs.std()
	for i in range(3):
		cs_index = np.where((cs>cs_mean+(1+1*i)*cs_std)|(cs<cs_mean-(1+1*i)*cs_std))
		w[cs_index] = 0
		smooth = WhittakerSmooth(spectra,w,lambda_)
		cs = spectra-smooth
		cs_mean = cs[w!=0].mean()
		cs_std = cs[w!=0].std()
	return smooth


def baseline(spectra,lambda_,hwi,it,int_):
	spectra = np.array(spectra)
	spectra = get_smooth(spectra,lambda_)

	if it != 1 :
		d1 = np.log10(hwi)
		d2 = 0
		w = np.ceil(np.concatenate((10**(d1+np.arange(0,it-1,1)*(d2-d1)/(np.floor(it)-1)),[d2])))
		w = np.array(w,dtype = int)
	else:
		w = np.array([hwi],dtype = int)
	#print(w)

	lims = np.linspace(0,spectra.size -1,int_+1)
	lefts = np.array(np.ceil(lims[:-1]),dtype = int)#这里指的是索引值
	rights = np.array(np.floor(lims[1:]),dtype = int)#同上
	minip = (lefts+rights)*0.5#索引
	xx = np.zeros(int_)
	for i in range(int_):#这里是一个rebin的过程,这里可以提速
		xx[i] = spectra[lefts[i]:rights[i]+1].mean()

	for i in range(it):
		# Current window width
		w0 = w[i]
		# Point-wise iteration to the right
		for j in range(1,int_-1):
			# Interval cut-off close to edges
			v = min([j,w0,int_-j-1])
			# Baseline suppression
			a = xx[j-v:j+v+1].mean()
			xx[j] = min([a,xx[j]])
		for j in range(1,int_-1):
			k = int_-j-1
			v = min([j,w0,int_-j-1])
			a = xx[k-v:k+v+1].mean()
			xx[k] = min([a,xx[k]])

	minip = np.concatenate(([0],minip,[spectra.size-1]))
	xx = np.concatenate((xx[:1],xx,xx[-1:]))
	index = np.arange(0,spectra.size,1)
	xxx = np.interp(index,minip,xx)
	return xxx
































