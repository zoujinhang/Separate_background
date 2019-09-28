'''
WhittakerSmooth平滑器
作为评估背景的内核


'''
from scipy.sparse import csc_matrix,eye,diags
from scipy.sparse.linalg import spsolve
import numpy as np



def WhittakerSmooth(x,w,lambda_):
	'''

	:param x: array 输入数值，数组
	:param w: array 与数值对应的权重数组
	:param lambda_: 平滑参数
	:return: array 平滑结果
	'''
	X=np.matrix(x)#这里将数组转化为矩阵。矩阵之后就不可以用索引进行引用了。
	m=X.size
	#i=np.arange(0,m)
	E=eye(m,format='csc')
	D=E[1:]-E[:-1] # numpy.diff() does not work with sparse matrix. This is a workaround.
	W=diags(w,0,shape=(m,m))
	A=csc_matrix(W+(lambda_*D.T*D))
	B=csc_matrix(W*X.T)
	background=spsolve(A,B)   #求解矩阵方程

	return np.array(background)














