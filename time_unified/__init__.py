
import numpy as np

class Time_transform(object):
	def __init__(self,time,value):

		self.time = time
		self.value = value
		self.time_range = self.time[-1]-self.time[0]
		self.bin_numb = self.time.size

		mreg_n = self.bin_numb/self.time_range
		if mreg_n >= 1:
			self.unif_time,self.unif_value = self.rebin(mreg_n)
		else:
			self.unif_time,self.unif_value = self.supplement_bin()

	def rebin(self,mreg_n):

		mreg_n = int(mreg_n)
		x = np.array(self.time)
		y = np.array(self.value)
		cutoff = int(x.size/mreg_n)*mreg_n
		x_a = x[:cutoff]
		y_a = y[:cutoff]
		reshape_x = x_a.reshape(-1,mreg_n)
		reshape_x = reshape_x.mean(axis=1)
		reshape_y = y_a.reshape(-1,mreg_n)
		reshape_y = reshape_y.mean(axis=1)
		if(x.size % mreg_n != 0):
			x_b = x[cutoff:]
			y_b = y[cutoff:]
			reshape_x = np.concatenate((reshape_x,[x_b.mean()]))
			reshape_y = np.concatenate((reshape_y,[y_b.mean()]))

		return reshape_x,reshape_y

	def supplement_bin(self):

		re_x = np.arange(self.time[0],self.time[-1]+1,1)
		re_y = np.interp(re_x,self.time,self.value)

		return re_x,re_y

	def to_unified_time(self):
		return self.unif_time,self.unif_value


	def to_actual_time(self,time,value):

		try:
			if(time[0] != self.time[0]):
				time = np.concatenate(([self.time[0]],time))
				value = np.concatenate(([value[0]],value))
			if(time[-1] != self.time[-1]):
				time = np.concatenate((time, [self.time[-1]]))
				value = np.concatenate((value,[value[0]] ))

			actual_value = np.interp(self.time,time,value)
			return self.time,actual_value
		except:
			print('输入时间不匹配！')















