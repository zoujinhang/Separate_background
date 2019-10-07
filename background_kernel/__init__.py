'''
创建一个类，
'''
from .WhittakerSmooth import WhittakerSmooth
import numpy as np
from ..time_unified import Time_transform


class Baseline_in_time(object):

	def __init__(self,time,value,hardness = False):
		self.time = time
		self.value = value
		self.t_transform = Time_transform(time,value)
		self.unified_time,self.unified_value = self.t_transform.to_unified_time()
		self.AirPLS = AirPLS(self.unified_value,hardness = hardness)
		self.unified_bs =self. AirPLS.double_airPLS()
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
				print('baseline 采样区间小于总区间的 10%，可能出现过拟合。建议检查拟合情况。')
				break
			cs_mean = cs[w!=0].mean()
			cs_std = cs[w!=0].std()

		return bs





































