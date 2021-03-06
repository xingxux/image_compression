# input X1, X2
# get distribution of X1 + X2*X4
# output as X3
import os, pickle, time, sys
from multiprocessing.pool import ThreadPool

def pdf_cdf(b):
	c = []
	pre = 0
	for x in b:
		pre += x
		c.append(pre)
	return c


def worker(a,b):
	global x1, x2, y1, y2
	x = []
	y = []
	print "start task:",a,b
	#for i in range(a, b+1):
#		x.append(i)
#		y.append(i+0.1)
#	return x,y
	x2_l = min(x2)
	x2_r = max(x2)
	p1 = {}
	p2 = {}
	for i in range(len(x1)):
		p1[x1[i]] = y1[i]
	for i in range(len(x2)):
		p2[x2[i]] = y2[i]


	for i in range(a, b + 1):
		#print i
		if i % 1000 == 0:
			print "task %d %d: "%(a,b), i, int(time.time())
		x.append(i)
		p = 0.0
		for j in range(-1+int(min(x1)), i+1-int(min(x2))):
			#if j-i==-3:
			#	p+=p1[j]
			#else:
			#	continue
			#print j, i-j
			if i-j in p2 and j in p1: #>=x2_l and j-i<=x2_r:
				p += p2[i-j]*p1[j]
				#print j, i-j
			#if j-i in x2:
				#p += y2[x2.index(j-i)]*y1[x1.index(i)]
		y.append(p)
	return x, y

def log_result(result):
	global final_x, final_y
	final_x += result[0]
	final_y += result[1]

def get_close_y(y, y_):
	close_i = 0
	close = 100000000000000000000
	for i in range(len(y)):
		if abs(y[i] - y_) < close:
			close = abs(y[i] - y_)
			close_i = i
	return close_i

f1 = sys.argv[1]
f2 = sys.argv[2]
f3 = sys.argv[3]
f4 = float(sys.argv[4])
with open(f2, 'rb') as f_in:
		x2, y2 = pickle.load(f_in)
for i in range(len(x2)):
	x2[i] = int(round(x2[i]*f4))

x2_ = []
y2_ = []
last = -1
y_ = 0.0
for i in range(len(x2)):
	if x2[i] != last:
		if i > 0:
			x2_.append(last)
			y2_.append(y_)
		y_ = y2[i]
		last = x2[i]
	else:
		y_ += y2[i]

x2 = x2_
y2 = y2_

with open(f1, 'rb') as f_in:
		x1, y1 = pickle.load(f_in)
print min(x1), max(x1), sum(y1)
print min(x2), max(x2), sum(y2)

y1_cdf = pdf_cdf(y1)


final_x_, final_y_ = worker(-1+int(min(x1))+int(min(x2)),1+int(max(x1))+int(max(x2)))

#print final_x
#print final_y
#print max(final_x)

final_x = []
final_y = []
t_ = 0.0
final_y_cdf = pdf_cdf(final_y_)
for i in range(len(final_x_)):
	t_ = final_y_cdf[i]
	ttt = x1[get_close_y(y1_cdf, t_)]
	if final_x_[i] < ttt:
		final_x.append(int(round(ttt)))
	else:
		final_x.append(final_x_[i])
	final_y.append(final_y_[i])

final_x2_ = []
final_y2_ = []
last = -1
y_ = 0.0
for i in range(len(final_x)):
	if final_x[i] != last:
		if i > 0:
			final_x2_.append(last)
			final_y2_.append(y_)
		y_ = final_y[i]
		last = final_x[i]
	else:
		y_ += final_y[i]

final_x = final_x2_
final_y = final_y2_

print max(final_x)
p=0.0
for x in final_y:
	p += x
print "p", p

with open(f3, 'wb') as f_out:
	pickle.dump((final_x,final_y), f_out)
