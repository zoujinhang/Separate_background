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
		self.get_background()
		self.check_background()


	def separate_background_for_one_ch(self,t,ch,ch_n):
		t = t[np.where(ch == ch_n)]
		if len(t) == 0:
			return np.array([]),np.array([])
		Era = Event_rate_analysis(t,time_range=[self.time_start,self.time_stop])
		GPS = Era.get_wt_GPS()
		#GPS = Era.get_GPS()
		BPS = Era.get_BPS()
		#print('GPS \n',GPS)
		#print('BPS \n',BPS)
		mc = MC_separate(t,GPS,BPS)
		return mc.S,mc.B

	def get_background(self):

		s = np.array([])
		b = np.array([])
		s_ch = np.array([])
		b_ch = np.array([])
		for i in self.ch_n:
			print('inite channel ', i)
			S, B = self.separate_background_for_one_ch(self.t, self.ch, i)
			S_ch = np.zeros_like(S) + i
			B_ch = np.zeros_like(B) + i
			s = np.concatenate((s, S))
			s_ch = np.concatenate((s_ch, S_ch))
			b = np.concatenate((b, B))
			b_ch = np.concatenate((b_ch, B_ch))
		s_index = np.argsort(s)
		b_index = np.argsort(b)
		self.s = s[s_index]
		self.s_ch = s_ch[s_index]
		self.b = b[b_index]
		self.b_ch = b_ch[b_index]

	def check_background(self):
		'''
		背景检查，首先逐能道检查背景，然后检查总背景，以防背景过扣。
		:return:
		'''
		#-------------------------------------------------------------------------------------------------------
		b_s = np.array([])                                                          #逐能道检测背景部分
		b_b = np.array([])
		b_s_ch = np.array([])
		b_b_ch = np.array([])
		for i in self.ch_n:
			print('check channel ', i,end = '\r')
			b_S, b_B = self.separate_background_for_one_ch(self.b, self.b_ch, i)
			S_ch = np.zeros_like(b_S) + i
			B_ch = np.zeros_like(b_B) + i
			b_s = np.concatenate((b_s, b_S))
			b_s_ch = np.concatenate((b_s_ch, S_ch))
			b_b = np.concatenate((b_b, b_B))
			b_b_ch = np.concatenate((b_b_ch, B_ch))
		b_s_index = np.argsort(b_s)
		b_b_index = np.argsort(b_b)
		c_s = b_s[b_s_index]
		c_s_ch = b_s_ch[b_s_index]

		c_b = b_b[b_b_index]
		c_b_ch = b_b_ch[b_b_index]
		self.b = c_b
		self.b_ch = c_b_ch
		c_s = np.concatenate((c_s, self.s))
		c_s_ch = np.concatenate((c_s_ch, self.s_ch))
		sort_index = np.argsort(c_s)
		self.s = c_s[sort_index]
		self.s_ch = c_s_ch[sort_index]
		#-------------------------------------------------------------------------------------------------------
		'''
		print('check gross \r')
		Bra = Event_rate_analysis(self.b)                                   #背景的总体检测部分
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
		print('check over!')
		'''
		#-------------------------------------------------------------------------------------------------------

	def get_S(self):
		return self.s
	def get_B(self):
		return self.b
























