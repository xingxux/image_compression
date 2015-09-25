# this file is to plot PSNR / rate curve for different quality factor, and by zero-off of using different threshold
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os, sys, glob, commands
import matplotlib.gridspec as gridspec
from pylab import *

def get_threshold_jpg(in_, out_, threshold, quality):
	global folder
	base_file = "tmp_out_base.block"
	c = commands.getstatusoutput("/opt/libjpeg-turbo-coef/bin/jpegtran -outputcoef tmp.block %s %s"%(in_, base_file))
	c = commands.getstatusoutput("python lossy_zerooff.py tmp.block tmp_out.block %s %s"%(str(threshold), str(quality)))
	c = commands.getstatusoutput("/opt/libjpeg-turbo-coef/bin/jpegtran -inputcoef tmp_out.block %s %s"%(base_file, out_))


root = "generated_lromp"
reso = "1200"
#reso = "1200"
fs = glob.glob("images/TESTIMAGES/RGB/RGB_OR_1200x1200/*.png")
fs = fs[:51]

dest = range(40, 90, 2)
qs = [100,50, 60,70,80,86,90]
#qs = [100,50]
thres1 = range(1, 4)
thres2 = range(1, 11)

for t1 in thres1:
	for t2 in thres2:
		sub = "%s/%d_%d"%(root, thres1, thres2)
		os.system("mkdir " + sub)
		
		for f in fs:
			fname = f[f.rfind("/")+1:f.find(".jpg")] + "_lromp.jpg"
			os.system("/opt/libjpeg-turbo-lromp-only/bin/jpegtran -encode t %f %f %s %s/%s"%(float(t1), float(t2), f, sub,fname)) 


#qs = range(60, 96, 6) + [100]
print qs, dest

root_folder = "better_transcoding"
c = commands.getstatusoutput("rm %s -rf"%(root_folder))
c = commands.getstatusoutput("mkdir " + root_folder)

folder = root_folder

x = {}
y = {}
x2 = {}
y2 = {}
s_r = {} # size reduction
for t in qs:
	x[t] = []
	y[t] = []
	x2[t] = []
	y2[t] = []
	s_r[t] = []

ind = 0
print fs
for f in fs:
	for q in qs:
		if q != 100:
			c = commands.getstatusoutput("convert -sampling-factor 4:2:0 -quality " + str(q)  + " "  + f + " " + folder + "/" + str(ind) + "_q_" + str(q) +".jpg")
		else:
			c = commands.getstatusoutput("cp " + f + " " + folder + "/" + str(ind) + "_q_100.png")
	ind += 1

for q in qs:
	if q==100:
		rr = range(40, max(dest)+5, 2)
	else:
		rr = range(q,q-10,-1)
	for d in rr:
	#for d in dest:
		#if d > q:
		#	continue
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
				#c1 = commands.getstatusoutput("pyssim %s/%d_q_100.png %s "%(folder, ind, f_out))
				size += os.path.getsize(f_out)
			else:
				c = commands.getstatusoutput("compare -metric PSNR %s/%d_q_100.png %s tmp_diff.png"%(folder, ind, f_in))
				#c1 = commands.getstatusoutput("pyssim %s/%d_q_100.png %s "%(folder, ind, f_in))
				size += os.path.getsize(f_in)
			psnr += float(c[1])
			#ssim += float(c1[1])
			ind += 1
		psnr /= len(fs)
		#ssim /= len(fs)
		size /= len(fs)*1000
		#print q, d, ":", psnr, ssim, size
		#print q, d, ":", psnr, size
		x[q].append(size)
		y[q].append(psnr)
		#y2[q].append(ssim)

#c = commands.getstatusoutput("/opt/libjpeg-turbo/bin/jpegtran -outputcoef tmp.block %s %s"%(folder+"/"+str(ind)+".jpg", folder+"/"+str(ind)+"_std.jpg"))
#get_threshold_jpg(folder+"/"+str(ind)+"_%d.jpg"%(t), t, "tmp.block", folder+"/"+str(ind)+"_std.jpg", q)
#def get_threshold_jpg(in_, out_, threshold, quality):
for q in qs:
	print q
	for d in [q]+thre:
		print "\t",d
	#for d in dest:
		#if d > q:
		#	continue
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
				get_threshold_jpg(f_in, f_out, str(d), 75)
				#c = commands.getstatusoutput("convert -sampling-factor 4:2:0 -quality " + str(d)  + " "  + f_in + " " + f_out)
				c = commands.getstatusoutput("compare -metric PSNR %s/%d_q_100.png %s tmp_diff.png"%(folder, ind, f_out))
				#c1 = commands.getstatusoutput("pyssim %s/%d_q_100.png %s "%(folder, ind, f_out))
				size += os.path.getsize(f_out)
			else:
				c = commands.getstatusoutput("compare -metric PSNR %s/%d_q_100.png %s tmp_diff.png"%(folder, ind, f_in))
				#c1 = commands.getstatusoutput("pyssim %s/%d_q_100.png %s "%(folder, ind, f_in))
				size += os.path.getsize(f_in)
			psnr += float(c[1])
			#ssim += float(c1[1])
			ind += 1
		psnr /= len(fs)
		#ssim /= len(fs)
		size /= len(fs)*1000
		#print q, d, ":", psnr, size
		x2[q].append(size)
		y2[q].append(psnr)
		#y2[q].append(ssim)


#print x
#print y
#print x2
#print y2

fig = plt.figure()
ax = fig.add_subplot(111)
leg = []
for t in qs:
	if t == 100:
		ax.plot(x[t], y[t], '-k', lw=1)
		leg.append("Raw Image")
		print "#",t
		for tt in x[t]:
			print tt,",",
		print ""
		for tt in y[t]:
			print tt,",",
		print ""	
	else:
		ax.plot(x[t], y[t], ':r', lw=3)#, ms=15, markevery=3)
		leg.append("Changing Quality")
		print "#",t, "changing quality"
		for tt in x[t]:
			print tt,",",
		print ""
		for tt in y[t]:
			print tt,",",
		print ""			
		ax.plot(x2[t], y2[t], '-b', dashes=[16,4,2,4],lw=3)#, ms=15, markevery=3)
		leg.append("LOSSY")
		print "#",t, "L-ROMP"
		for tt in x2[t]:
			print tt,",",
		print ""
		for tt in y2[t]:
			print tt,",",
		print ""					
ax.set_xlabel("Filesize (KB)", fontsize=24)
ax.grid()
ax.set_ylabel("PSNR (dB)", fontsize=24)
ax.legend(leg[:3], 4, fontsize=22, numpoints=1)
#ax2.legend(leg, 4)
tight_layout()
plt.tick_params(axis='both', which='major', labelsize=22)
plt.tick_params(axis='both', which='minor', labelsize=22)
savefig("better_transcoding_%s.png"%(reso))
savefig("better_transcoding_%s.eps"%(reso))