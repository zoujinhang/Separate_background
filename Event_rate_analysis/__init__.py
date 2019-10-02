from .bayesian_rate_edges import *
from ..background_kernel import Baseline_in_time
import numpy as np


class Evet_rate_analysis(object):

	def __init__(self,t,time_range = None):
		self.t = t

		if time_range is None:
			self.time_start = t[0]
			self.time_stop = t[-1]
		else:
			self.time_start = time_range[0]
			self.time_stop = time_range[-1]

	def get_BPS(self):

		edges = np.arange(self.time_start,self.time_stop+1,1)
		bin_n,bin_edges = np.histogram(self.t,bins = edges)
		bin_n = np.concatenate(([bin_n[0]],bin_n))

		bs = Baseline_in_time(bin_edges,bin_n).get_bs()

		return np.interp(self.t,bin_edges,bs)

	def get_GPS(self):

		edges = bayesian_rate_edges(self.t,prior = 1.5)

		bin_n,bin_edges = np.histogram(self.t,bins = edges)
		bin_size = bin_edges[1:]-bin_edges[:-1]
		bin_rate = bin_n/bin_size
		bin_c = (bin_edges[1:]+bin_edges[:-1])*0.5

		bin_c = np.concatenate(([self.time_start],bin_c,[self.time_start]))
		bin_rate = np.concatenate(([bin_rate[0]],bin_rate,[bin_rate[-1]]))

		return np.interp(self.t,bin_c,bin_rate)























