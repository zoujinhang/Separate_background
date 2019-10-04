from .bayesian_rate_edges import *
from ..background_kernel import Baseline_in_time
import numpy as np


class Event_rate_analysis(object):

	def __init__(self,t,ch = None,time_range = None):

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
		return np.interp(self.t,bin_edges,bs)

	def get_GPS(self):
		edges = np.arange(self.time_start,self.time_stop+1,1)
		#edges = bayesian_rate_edges(self.t,prior = 1.5)
		print('bayesian l ',len(edges))
		bin_n,bin_edges = np.histogram(self.t,bins = edges)
		bin_size = bin_edges[1:]-bin_edges[:-1]
		bin_rate = bin_n/bin_size
		bin_c = (bin_edges[1:]+bin_edges[:-1])*0.5

		bin_c = np.concatenate(([self.time_start],bin_c,[self.time_stop]))
		bin_rate = np.concatenate(([bin_rate[0]],bin_rate,[bin_rate[-1]]))

		return np.interp(self.t,bin_c,bin_rate)























