from .time_unified import Time_transform
from .background_kernel import AirPLS




class Baseline_in_time(object):

	def __init__(self,time,value,hardness = False):
		self.time = time
		self.value = value
		self.t_transform = Time_transform(time,value)
		self.unified_time,self.unified_value = self.t_transform.to_unified_time()
		self.AirPLS = AirPLS(self.unified_value,hardness = hardness)
		self.unified_bs =self. AirPLS.double_airPLS()
		self.bs = self.t_transform.to_actual_time(time,self.unified_bs)
		self.cs = self.value-self.bs

	def get_value(self):
		return self.time,self.cs,self.bs


	def get_bs(self):
		return self.bs

	def get_cs(self):
		return self.cs

	def get_airPLS(self):
		return self.AirPLS

























