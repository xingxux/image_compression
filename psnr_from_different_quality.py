# this file is to plot PSNR / rate curve for different quality factor, and by zero-off of using different threshold
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os, sys, glob, commands
import matplotlib.gridspec as gridspec
from pylab import *

def get_threshold_jpg(out_, threshold, block_file, base_file, quality):
	global folder
	c = commands.getstatusoutput("python lossy_zerooff.py %s tmp_out.block %s %s"%(block_file, str(threshold), str(quality)))
	print "(", c[1], 
	c = commands.getstatusoutput("/opt/libjpeg-turbo/bin/jpegtran -inputcoef tmp_out.block %s %s"%(base_file, out_))

reso = "600"
fs = glob.glob("images/raw/*.png")
reso = "1200"
fs = glob.glob("images/TESTIMAGES/RGB/RGB_OR_1200x1200/*.png")
fs = fs[:2]

dest = range(40, 93, 2)
qs = range(60, 91)
qs = [30,40,50,60,70,80,90]
qs = range(60, 96, 6) + [100]
qs = [100,90,86,80,70,60,50]
#print qs, dest

root_folder = "psnr_transcoding"
c = commands.getstatusoutput("rm %s -rf"%(root_folder))
c = commands.getstatusoutput("mkdir " + root_folder)

folder = root_folder

x = {}
y = {}
y2 = {}
s_r = {} # size reduction
for t in qs:
	x[t] = []
	y[t] = []
	y2[t] = []
	s_r[t] = []

ind = 0
for f in fs:
	for q in qs:
		if q != 100:
			c = commands.getstatusoutput("convert -sampling-factor 4:2:0 -quality " + str(q)  + " "  + f + " " + folder + "/" + str(ind) + "_q_" + str(q) +".jpg")
		else:
			c = commands.getstatusoutput("cp " + f + " " + folder + "/" + str(ind) + "_q_100.png")
	ind += 1

for q in qs:
	print q
	for d in dest:
		print "", d
		if d > q:
			continue
		ind = 0
		psnr = 0.0
		ssim = 0.0
		size = 0.0
		ind = 0
		for f in fs:
			if q != 100:
				f_in = folder + "/" + str(ind) + "_q_" + str(q) + ".jpg"
			else:
				f_in = folder + "/" + str(ind) + "_q_100.png"
			f_out = folder + "/temp.jpg"
			if d != q:
				c = commands.getstatusoutput("convert -sampling-factor 4:2:0 -quality " + str(d)  + " "  + f_in + " " + f_out)
				c = commands.getstatusoutput("compare -metric PSNR %s/%d_q_100.png %s tmp_diff.png"%(folder, ind, f_out))
				c1 = commands.getstatusoutput("pyssim %s/%d_q_100.png %s "%(folder, ind, f_out))
				size += os.path.getsize(f_out)
			else:
				c = commands.getstatusoutput("compare -metric PSNR %s/%d_q_100.png %s tmp_diff.png"%(folder, ind, f_in))
				c1 = commands.getstatusoutput("pyssim %s/%d_q_100.png %s "%(folder, ind, f_in))
				size += os.path.getsize(f_in)
			psnr += float(c[1])
			ssim += float(c1[1])
			ind += 1
		psnr /= len(fs)
		ssim /= len(fs)
		size /= len(fs)
		#print q, d, ":", psnr, ssim, size
		x[q].append(size/1000)
		y[q].append(psnr)
		y2[q].append(ssim)

#print x
#print y
#print y2

fig = plt.figure()
ax = fig.add_subplot(111)
leg = []
for t in qs:
	#ax.plot(x[t], y[t], '-x')
	if t != 100:
		ax.plot(x[t], y[t], ':', lw=3)
		leg.append("Changing Quality")
	else:
		ax.plot(x[t], y[t], '-k', lw=1)
		leg.append("Raw Image")
	print "#",t
	for tt in x[t]:
		print tt,",",
	print ""
	for tt in y[t]:
		print tt,",",
	print ""	
ax.set_xlabel("Filesize (KB)", fontsize=24)
ax.grid()
ax.set_ylabel("PSNR (dB)", fontsize=24)
#ax.legend(leg, 4)
ax.legend(leg[:2], 4, fontsize=22, numpoints=1, ncol=1)

#ax2.legend(leg, 4)
tight_layout()
plt.tick_params(axis='both', which='major', labelsize=22)
plt.tick_params(axis='both', which='minor', labelsize=22)
savefig("Q_psnr_transcoding_%s.png"%(reso))
savefig("Q_psnr_transcoding_%s.eps"%(reso))

fig = plt.figure()
ax = fig.add_subplot(111)
leg = []
for t in qs:
	#ax.plot(x[t], y2[t], '-x')
	if t != 100:
		ax.plot(x[t], y2[t], ':', lw=3)
		leg.append("QP="+str(t))
	else:
		ax.plot(x[t], y2[t], '-k', lw=1)
		leg.append("Raw Image")
ax.set_xlabel("Filesize (KB)", fontsize=24)
ax.grid()
ax.set_ylabel("SSIM", fontsize=24)
ax.legend(leg[:2], 4, fontsize=22, numpoints=1, ncol=1)
#ax2.legend(leg, 4)
tight_layout()
plt.tick_params(axis='both', which='major', labelsize=22)
plt.tick_params(axis='both', which='minor', labelsize=22)
savefig("Q_ssim_transcoding_%s.png"%(reso))
savefig("Q_ssim_transcoding_%s.eps"%(reso))
