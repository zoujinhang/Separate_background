'''

'''
import numpy as np
from ..background_kernel.WhittakerSmooth import WhittakerSmooth


class WT_kernel(object):

	def __init__(self,t):


		self.t = np.array(t)
		self.wt = self.work_WT()
		rate = 1.0/self.wt
		w = np.ones(rate.size)
		self.rate = WhittakerSmooth(rate,w,2)


	def get_wt(self):
		return self.wt

	def get_rate(self):
		return self.rate

	def weight(self,x,x0,sigma):
		return np.exp(-(x-x0)**2/(2*sigma**2))

	def work_WT(self):
		#这里的卷积有些慢。
		dt = self.t[1:]-self.t[:-1]
		wt = []
		for index,value in enumerate(self.t):
			ww = self.weight(self.t,value,1.024)  #长度为t的长度。
			dti = np.insert(dt,index,0)
			ww_sum = ww.sum()-1
			wti = (dti*ww).sum()/ww_sum
			wt.append(wti)
		wt = np.array(wt)
		'''
		n = len(self.t)
		nn = np.arange(0,n,1)
		x = np.arange(-100, 101, 1)
		#---------------------------------------------------------------------------------------------------------------
		ww = self.weight(x, 0, 6)    #产生高斯形状的权重，高斯形状的sigma为5，该数值有平滑效果，为尽力保存原始数据结构，该数值不易过大。
		ww = ww[ww > 0.01]           #为提升计算速度，这里只选用了有效的权重值
		#---------------------------------------------------------------------------------------------------------------
		w_index = np.arange(0, len(ww), 1)         #产生索引值，用于从原始数据中提取响应的数据。
		w_c = int(w_index.mean())		   #索引的中心值，在后面用作提取数据长度中心
		#w_n = int((len(ww) - 1) / 2)
		#--------------------------------------------------------------------------------------------------------------
		for index,value in enumerate(nn):
			if index < n-1:
				dti = np.insert(dt,index,values = [0])
			else:
				dti = np.concatenate((dt,[0]))
			#--------------------------------------------------------------------------------------------------
			i_index = w_index - w_c + index                                  #移动索引值，提取不同时段的数据
			v_index = np.where((i_index >= 0) & (i_index < n))[0]		 #限制索引范围，
			i_index = i_index[v_index]					 #使提取数据与权重数值一一对应。
			weit_ar = ww[v_index]
			#--------------------------------------------------------------------------------------------------
			#weit_ar = self.weight(nn,value,4)
			#index_w = np.where(weit_ar > 0.01)[0]
			weit_sum = weit_ar.sum()-1
			wti = (dti[i_index]*weit_ar).sum()/weit_sum
			wt.append(wti)
		'''
		return wt













