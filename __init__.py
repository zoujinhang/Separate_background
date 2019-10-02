'''

进行背景光子事件的分离。
'''

from .time_unified import *
from .background_kernel import *
from .MC_separate import *
from .Event_rate_analysis import *
import numpy as np





class Separate_background(object):
	'''

	'''

	def __init__(self,t,ch,ch_n,
		     time_range = None
		     ):

		if time_range is None:
			self.time_start = t[0]
			self.time_stop = t[-1]
		else:
			self.time_start = time_range[0]
			self.time_stop = time_range[-1]

		self.t = t
		self.ch = ch
		self.ch_n = ch_n

		s = np.array([])
		b = np.array([])

		for i in self.ch_n:
			S,B = self.separate_background_for_one_ch(i)
			s = np.concatenate((s,S))
			b = np.concatenate((b,B))
		self.s = s
		self.b = b



	def separate_background_for_one_ch(self,ch_n):
		t = self.t[np.where(self.ch == ch_n)]
		Era = Evet_rate_analysis(t,time_range=[self.time_start,self.time_stop])
		GPS = Era.get_GPS()
		BPS = Era.get_BPS()
		return MC_separate(t,GPS,BPS)

	def get_S(self):
		return self.s
	def get_B(self):
		return self.b
























