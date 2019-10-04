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
			self.t = t
			self.ch = ch
		else:
			self.time_start = time_range[0]
			self.time_stop = time_range[-1]
			self.t = t[np.where((t>=self.time_start)&(t<=self.time_stop))]
			self.ch = ch[np.where((t>=self.time_start)&(t<=self.time_stop))]
		#self.t = t
		#self.ch = ch
		self.ch_n = ch_n

		s = np.array([])
		b = np.array([])
		s_ch = np.array([])
		b_ch = np.array([])
		for i in self.ch_n:
			print('inite channel ',i)
			S,B = self.separate_background_for_one_ch(i)
			S_ch = np.zeros_like(S) + i
			B_ch = np.zeros_like(B) + i
			s = np.concatenate((s,S))
			s_ch = np.concatenate((s_ch,S_ch))
			b = np.concatenate((b,B))
			b_ch = np.concatenate((b_ch,B_ch))
		s_index = np.argsort(s)
		b_index = np.argsort(b)
		self.s = s[s_index]
		self.s_ch = s_ch[s_index]
		self.b = b[b_index]
		self.b_ch = b_ch[b_index]
		self.check_background()


	def separate_background_for_one_ch(self,ch_n):
		t = self.t[np.where(self.ch == ch_n)]
		Era = Event_rate_analysis(t,time_range=[self.time_start,self.time_stop])
		GPS = Era.get_GPS()
		BPS = Era.get_BPS()
		#print('GPS \n',GPS)
		#print('BPS \n',BPS)
		mc = MC_separate(t,GPS,BPS)
		return mc.S,mc.B
	def check_background(self):

		Bra = Event_rate_analysis(self.b)
		GPS = Bra.get_GPS()
		BPS = Bra.get_BPS()
		mc = MC_separate(self.b,GPS,BPS,ch = self.b_ch)

		c_b,c_b_ch = mc.B
		c_s,c_s_ch = mc.S

		self.b = c_b
		self.b_ch = c_b_ch
		c_s = np.concatenate((c_s,self.s))
		c_s_ch = np.concatenate((c_s_ch,self.s_ch))
		sort_index = np.argsort(c_s)
		self.s = c_s[sort_index]
		self.s_ch = c_s_ch[sort_index]




	def get_S(self):
		return self.s
	def get_B(self):
		return self.b
























