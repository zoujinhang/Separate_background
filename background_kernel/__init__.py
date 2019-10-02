'''
创建一个类，
'''
from .WhittakerSmooth import WhittakerSmooth
import numpy as np

class AirPLS(object):

	def __init__(self,x,hardness = False):
		self.x = np.array(x)
		self.m = self.x.shape[0]

		self.w = np.ones(self.m)

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
				valu = w[i]

			else:

				if first == False:
					if(valu == 1):
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
						w[change_index] = valu

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
			w = self.w_pp(w,rang = 20,f = 30)
			bs = WhittakerSmooth(self.x,w,100)
			cs = self.x - bs
			drti = ((cs1-cs)**2).mean()
			if(drti <0.01):
				break
			cs_mean = cs[w!=0].mean()
			cs_std = cs[w!=0].std()

		return bs





































