import numpy as np

class MC_separate(object):
	'''
	马尔科夫分离法，将随机事件分离开。
	'''

	def __init__(self,t,GPS,BPS,ch = None):
		'''

		:param t:  array or list 需要进行分离的样本
		:param GPS: array or list 总的概率标准
		:param BPS: array or list 背景概率标准
		:param ch: array or list 与t参数等长度，是t参数的伴随量
		'''
		#data = np.asarray(data,dtype=float)
		#GPS = np.asarray(GPS)
		#BPS = np.asarray(BPS)
		self.size = len(t)
		self.t = np.array(t)
		self.GPS = np.array(GPS)
		self.BPS = np.array(BPS)
		self.ch = ch
		if self.ch is not None:
			self.ch = np.array(self.ch)
			if self.ch.size != self.t.size:
				print('ch 与 t 参数长度不相同！不返回ch')
				self.ch = None
		self.S_index,self.B_index = self.MC_kernel()

		if self.ch is not None:
			self.S = self.t[self.S_index],self.ch[self.S_index]
			self.B = self.t[self.B_index],self.ch[self.B_index]
		else:
			self.S = self.t[self.S_index]
			self.B = self.t[self.B_index]


	def MC_kernel(self):
		'''
		这里可以通过一个多次迭代的马尔科夫方法分离样本。不过结果可能变化不大。
		:return:
		'''
		S_index = []#来自源的光子集
		B_index = []#来自背景的光子集

		MC_rand = np.random.rand(self.size)*self.GPS
		for index,value in enumerate(MC_rand):

			if value > self.BPS[index]:#当光子的随机数大于背景标准时，该光子为源光子
				S_index.append(index)
			else:
				B_index.append(index)
		return np.array(S_index,dtype=int),np.array(B_index,dtype=int)

	def get_B(self):
		return self.B
	def get_S(self):
		return self.S





















