import numpy as np

def MC_separate(data,GPS,BPS):
	'''
	马尔科夫分离法，将随机事件分离开。
	:param data: array or list 需要进行分离的样本
	:param GPS: array or list 总的概率标准
	:param BPS: array or list 背景概率标准
	:return: 2 array 信号源事件，背景事件
	'''
	data = np.asarray(data,dtype=float)
	GPS = np.asarray(GPS)
	BPS = np.asarray(BPS)

	data = np.array(data)
	size = data.size
	GPS = np.array(GPS)
	BPS = np.array(BPS)

	S = []
	B = []

	MC_rand = np.random.rand(size)*GPS

	for index,value in enumerate(MC_rand):

		if value >= BPS[index]:
			S.append(data[index])
		else:
			B.append(data[index])

	return np.array(S),np.array(B)
















