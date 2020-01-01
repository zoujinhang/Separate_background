from .bayesian_rate_edges import *
from ..background_kernel import Baseline_in_time
import numpy as np
from .WT_kernel import WT_kernel

class Event_rate_analysis(object):

	def __init__(self,t,time_range = None):

		#self.ch = ch
		if time_range is None:
			self.time_start = t[0]
			self.time_stop = t[-1]
			self.t = t
		else:
			self.time_start = time_range[0]
			self.time_stop = time_range[-1]
			self.t = t[np.where((t>=self.time_start)&(t<=self.time_stop))]


	def get_BPS(self):

		edges = np.arange(self.time_start,self.time_stop+1,1)
		bin_n,bin_edges = np.histogram(self.t,bins = edges)
		bin_n = np.concatenate(([bin_n[0]],bin_n))

		bs = Baseline_in_time(bin_edges,bin_n).get_bs()
		#print(self.t)
		#print(bin_edges)
		#print(bs)
		BPS = np.interp(self.t,bin_edges,bs)
		#rand = np.random.normal(BPS.size)*np.sqrt(BPS)

		return BPS #+ rand

	def get_GPS(self,binsize = 1):
		'''
		等时切片，分析GPS，这样分析的结果存在切片精度的问题。
		:param binsize:
		:return:
		'''
		edges = np.arange(self.time_start,self.time_stop+binsize,binsize)
		#edges = bayesian_rate_edges(self.t,prior = 1.)
		#print('bayesian l ',len(edges))
		bin_n,bin_edges = np.histogram(self.t,bins = edges)
		bin_size = bin_edges[1:]-bin_edges[:-1]
		bin_rate = bin_n/bin_size
		bin_c = (bin_edges[1:]+bin_edges[:-1])*0.5

		bin_c = np.concatenate(([self.time_start],bin_c,[self.time_stop]))
		bin_rate = np.concatenate(([bin_rate[0]],bin_rate,[bin_rate[-1]]))

		return np.interp(self.t,bin_c,bin_rate)

	def get_wt_GPS(self,prior = 1.1):
		'''
		使用WT分析GPS，计算量会大一些。分析结果不存在切片精度问题。
		:return:

		#edges = np.arange(self.time_start, self.time_stop + binsize, binsize)
		edges = fast_bayesian_rate_edges(self.t,prior =prior)
		# print('bayesian l ',len(edges))
		bin_n, bin_edges = np.histogram(self.t, bins=edges)
		bin_size = bin_edges[1:] - bin_edges[:-1]
		bin_rate = bin_n / bin_size
		bin_c = (bin_edges[1:] + bin_edges[:-1]) * 0.5

		bin_c = np.concatenate(([self.time_start], bin_c, [self.time_stop]))
		bin_rate = np.concatenate(([bin_rate[0]], bin_rate, [bin_rate[-1]]))

		return np.interp(self.t, bin_c, bin_rate)

		'''
		return WT_kernel(self.t).rate

	def get_bayesian_GPS(self,prior = 1.5):
		#edges = np.arange(self.time_start, self.time_stop + binsize, binsize)
		edges = bayesian_rate_edges(self.t,prior = prior)
		# print('bayesian l ',len(edges))
		bin_n, bin_edges = np.histogram(self.t, bins=edges)
		bin_size = bin_edges[1:] - bin_edges[:-1]
		bin_rate = bin_n / bin_size
		bin_c = (bin_edges[1:] + bin_edges[:-1]) * 0.5

		bin_c = np.concatenate(([self.time_start], bin_c, [self.time_stop]))
		bin_rate = np.concatenate(([bin_rate[0]], bin_rate, [bin_rate[-1]]))

		return np.interp(self.t, bin_c, bin_rate)

















