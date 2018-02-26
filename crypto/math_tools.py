
# calculates a discrete derivative
# via: (f(t + 1) - f(t - 1))
# where t is an index in the list f
# returns None on error
def disc_diff(f, t):
	ret = None
	domain_size = len(f)

	if t < domain_size-1 and t >= 1:
		if f[t + 1] is not None and f[t - 1] is not None:
			ret = (f[t + 1] - f[t - 1])
	elif t < domain_size-1 and t == 0:
		if f[t + 1] is not None and f[t] is not None:
			ret = (f[t + 1] - f[t])
	elif t == domain_size-1 and t >= 1:
		if f[t] is not None and f[t - 1] is not None:
			ret = (f[t] - f[t - 1])
	
	return ret

# return the average rate of change of the entire buffer passed in
def get_buffer_derivative(buff):
	deriv = 0.0
	points = 0
	for t in range(0, len(buff)):
		ret = disc_diff(buff, t)
		if ret is not None:
			deriv += ret
			points += 1

	if points != 0:
		return deriv / points
	else:
		return None
