import os, sys, glob, commands, pickle, operator

def get_pixels(f):
	c = commands.getstatusoutput("identify %s"%(f))
	s = c[1].split(" ")
	ss = s[2].split("x")
	return int(ss[0])*int(ss[1])

def get_threshold_jpg(out_, threshold, block_file, base_file):
	global folder
	c = commands.getstatusoutput("python ../../lossy_zerooff_ssim.py %s tmp_out.block___ %s %s"%(block_file, str(threshold), str(75)))
	c = commands.getstatusoutput("/opt/libjpeg-turbo-coef/bin/jpegtran -inputcoef tmp_out.block___ %s temp5.jpg"%(base_file))
	c = commands.getstatusoutput("jpegtran -optimize temp5.jpg %s"%(out_))

dest_bpp = [0.25, 0.5, 0.75, 1, 1.25, 1.5]
thre = [0.001,0.002,0.003,0.004,0.005,0.006,0.007,0.008,0.009,0.01,0.011,0.012]
thre = [50,100,200,300,500,2000]

fs = glob.glob("./*.bmp")

#os.system("mkdir all_qp")
#for f in fs:
#	fname = f[f.find("/")+1:f.find("bmp") - 1]
#	for q in range(99, 0, -1):
#		os.system("convert -sampling-factor 4:2:0 -quality " + str(q)  + " "  + f + " all_qp/" + fname+"_q"+str(q)+".jpg")
#		c = commands.getstatusoutput("/opt/libjpeg-turbo/bin/jpegtran -outputcoef all_qp/" + fname+"_q"+str(q)+".block " + " all_qp/" + fname+"_q"+str(q)+".jpg " + " all_qp/" + fname+"_q"+str(q)+".base ")

if os.path.isfile("range_ssim.pcs"):
	ran = pickle.load(open("range_ssim.pcs"))
	print ran
else:
	ran = {}
	for d in dest_bpp:
		print d
		ran[d] = {}
		for f in fs:
			print "\t", f
			ran[d][f] = {}
			fname = f[f.find("/")+1:f.find("bmp") - 1]
			ps = get_pixels(f)
			desired_size = ps*d/8
			min_ = -1
			max_ = -1
			flag = False
			done = False
			for q in range(1, 100):
				if done:
					break
				f_current = "all_qp/" + fname + "_q"+str(q)+".block"
				f_base = "all_qp/" + fname + "_q"+str(q)+".base"
				get_threshold_jpg("temp6.jpg", thre[len(thre)-1], f_current, f_base)
				fz = os.path.getsize("temp6.jpg")
				if not flag and fz > desired_size:
					print "\t\t", q, fz, desired_size
					min_ = q
					flag = True
				if flag:
					get_threshold_jpg("temp6.jpg", thre[0], f_current, f_base)
					fz = os.path.getsize("temp6.jpg")
					if fz > desired_size:
						done = True
						print "\t\t", q, fz, desired_size
					else:
						max_ = q
			ran[d][f][0] = min_
			ran[d][f][1] = max_
	print ran
	pickle.dump(ran, open("range_ssim.pcs", "wb"))

for b in dest_bpp:
	print b
	os.system("rm %s -rf"%("lromp_bpp_ssim_"+str(b)))
	os.system("mkdir %s"%("lromp_bpp_ssim_"+str(b)))
	for f in fs:
		print "\t", f, ran[b][f][0], ran[b][f][1]
		fname = f[f.find("/")+1:f.find("bmp") - 1]
		ps = get_pixels(f)
		desired_size = ps*b/8
		res = {}
		for q in range(ran[b][f][0], ran[b][f][1] + 1):
			f_current = "all_qp/" + fname + "_q"+str(q)+".block"
			f_base = "all_qp/" + fname + "_q"+str(q)+".base"
			for t in thre:
				get_threshold_jpg("temp6.jpg", t, f_current, f_base)
				fz = os.path.getsize("temp6.jpg")
				if fz < desired_size:
					#psnr = float(commands.getstatusoutput("compare -metric PSNR %s temp6.jpg temp6_diff.png"%(f))[1])
					psnr = float(commands.getstatusoutput("pyssim "  + f + " temp6.jpg")[1])
					res[str(q)+"_"+str(t)] = psnr
		sorted_x = sorted(res.items(), key=operator.itemgetter(1), reverse=True)
		print sorted_x
		t = sorted_x[0][0]
		t__ = t.split("_")
		q_ = int(t__[0])
		#t_ = float(t__[1])
		t_ = int(t__[1])
		f_current = "all_qp/" + fname + "_q"+str(q_)+".block"
		f_base = "all_qp/" + fname + "_q"+str(q_)+".base"
		get_threshold_jpg("%s/%s.jpg"%("lromp_bpp_ssim_"+str(b), fname + "_q" + str(q_)+"_t"+str(t_)+".jpg" ), t_, f_current, f_base)
		print "\t\t", fname, q_, t_, desired_size, sorted_x[0][1]
