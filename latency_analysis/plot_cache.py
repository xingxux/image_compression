import matplotlib
matplotlib.use('Agg')
import os, sys, glob, commands, pickle
import matplotlib.pyplot as plt
from pylab import *
import numpy

# hit ratio improvement for every 5% increment of cache size,
# 50% extra cache increaese 3.6% hit ratio
edge_cache_hr_5 = 0.36

# 50% extra cache increaese 5.5% hit ratio
origin_cache_hr = 0.55

edge_current_hr = 0.58
origin_current_hr = 0.32


def pdf_cdf(b):
	c = []
	pre = 0
	for x in b:
		pre += x
		c.append(pre)
	return c

def get_cache(i):
	global hr, proc, l, x_min, x_max
	x = []
	y = []
	flag = True
	t_ = 0.0
	for a in range(x_min, x_max+1):
		x.append(a + proc[i])
		p = 0.0
		for ii in range(len(l)):
			if a in l[ii]:
				p += hr[i][ii]*l[ii][a]
		y.append(p)
		t_ += p
		if flag and t_>=0.5:
			print i, ":",hr[i],proc[i], p,a+proc[i]
			flag = False


	print t_
	return x, y

#OB_x = [1,3,5,7,10,30,50,70,100,300,500,700,1000,3000,5000,7000,10000,30000,50000,70000,100000,300000]
#OB_y = [0.0198586,0.137056,0.14988,0.16166,0.215622,0.875385,0.949121,0.969343,0.980389,0.991751,0.99376,0.994784,0.995669,0.998924,0.999957,0.999999,1,1,1,1,1,1] 

hr = [[1,0,0], [0,1,0],[0,0,1]]
hr = [[0.1,0.3,0.6],[0.5,0.3,0.2]]
hr = [[0.1,0.3,0.6],[0.1,0.3,0.6]]
# edge cache: 1% higher : 58% -> 59%
# origin cache: 1.8% higher : 31.67% -> 33.47%
hr = [[0.580,0.133,0.287],[0.580,0.133,0.287], [0.590,0.137,0.273]]
proc = [0,19.2,19.2] 

fname = ["edge.obj_pdf","origin.obj_pdf","backend.obj_pdf"]
for x in range(1, len(sys.argv)):
	fname.append(sys.argv[x])

fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_ylabel("CDF")
ax.set_xlabel("Latency (ms)")
ax.grid()
#ax.set_xlim([0,300])
legend = []
l = []
i = 0
x_min = 1000000
x_max = -1 
for f in fname:
	l.append({})
	with open(f.split(".")[0] + ".obj_pdf", 'rb') as f_in:
		x, y = pickle.load(f_in)
		print f, min(x), max(x)
		print x[:10],y[:10]
		x_min = min(x_min, min(x))
		x_max = max(x_max, max(x))
		for j in range(len(x)):
			l[i][int(x[j])] = y[j]
	i += 1
		#legend.append(f.split(".")[0])
	#ax.plot(x, pdf_cdf(y))
x_min = int(x_min)
x_max = int(x_max)
print x_min, x_max
for i in range(len(hr)):
	x, y = get_cache(i)
	ax.plot(x, pdf_cdf(y))
	legend.append(str(hr[i])+" "+ str(proc[i]))

#ax.plot(OB_x, OB_y)
#legend.append("Origin to Backend")
ax.legend(legend, 4)
ax.set_xscale("log")
#ax.set_yscale("log")

savefig("plot_cache.png")
plt.close("all")
