import numpy as np

def bayesian_rate_edges(t,prior = 2.5):
	t = np.asarray(t)

	t = np.sort(t)

	unq_t,unq_ind,unq_inv = np.unique(t,
				      return_index=True,
				      return_inverse=True)
	if len(unq_t) == len(t):
		x = np.ones_like(t)
	else:
		x = np.bincount(unq_ind)

	t = unq_t

	edges = np.concatenate([t[:1],
                                0.5 * (t[1:] + t[:-1]),
                                t[-1:]])
	block_length = t[-1] - edges
	N = len(t)
	best = np.zeros(N, dtype=float)
	last = np.zeros(N, dtype=int)

	for R in range(N):
		T_k = block_length[:R + 1] - block_length[R + 1]
		N_k = np.cumsum(x[:R + 1][::-1])[::-1]

		fit_vec = N_k * (np.log(N_k) - np.log(T_k))
		A_R = fit_vec - prior
		A_R[1:] += best[:R]
		i_max = np.argmax(A_R)
		last[R] = i_max
		best[R] = A_R[i_max]
	change_points = np.zeros(N, dtype=int)
	i_cp = N
	ind = N
	while True:
		i_cp -= 1
		change_points[i_cp] = ind
		if ind == 0:
			break
		ind = last[ind - 1]
	change_points = change_points[i_cp:]

	return edges[change_points]
def fast_bayesian_rate_edges(t,prior = 2.5):
	t = np.asarray(t)

	t = np.sort(t)

	unq_t, unq_ind, unq_inv = np.unique(t,
					    return_index=True,
					    return_inverse=True)
	if len(unq_t) == len(t):
		x = np.ones_like(t)
	else:
		x = np.bincount(unq_ind)

	t = unq_t

	edges0 = np.concatenate([t[:1],
				0.5 * (t[1:] + t[:-1]),
				t[-1:]])

	N = len(t)

	sum_block = x[0]

	r_edges = [edges0[0]] #最终返回的边界列表
	dt1 = edges0[1]-edges0[0]#计算第一个时间差
	fit_old = x[0] * (np.log(x[0]) - np.log(dt1)) - prior#计算第一个适合度
	#edges_block_old = edges0[1]  # 开始的边界
	fit_sum = 0
	for i in range(N-1):

		sum_block_now = sum_block+x[i+1] #计算当前情况下总个数
		dt2 = edges0[i+2]-edges0[i+1]    #计算要添加的时长
		dt3 = dt1+dt2			 #计算当前情况下总时长
		fit_new = x[i+1] * (np.log(x[i+1]) - np.log(dt2)) - prior            #计算分离的适合度
		fit_1 = fit_old + fit_new                                      #计算分离总适合度
		fit_2 = sum_block_now*(np.log(sum_block_now)-np.log(dt3)) - prior#计算不分离总适合度

		if(fit_1 +fit_sum> fit_2+fit_sum):                     #说明需要分块。
			r_edges.append(edges0[i+1])    #添加分块边界。
			sum_block = x[i+1]	       #更新起始条件
			fit_sum = fit_sum + fit_old
			print(fit_sum)
			fit_old = fit_new       #更新起始条件

			dt1 = dt2		       #更新起始条件
		else:                                  #不分块
			sum_block = sum_block_now      #起始条件生长
			fit_old = fit_2                #起始条件生长
			dt1 = dt3                      #起始条件生长

	r_edges.append(edges0[-1])#添加最后一个边界

	return np.array(r_edges)
