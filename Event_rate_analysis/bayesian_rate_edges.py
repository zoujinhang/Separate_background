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
