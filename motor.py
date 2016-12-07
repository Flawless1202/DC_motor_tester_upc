# -*- coding: utf-8 -*- 
import numpy as np

# 存储与处理SD卡读到的数据
class data(object):
	# def __init__(self, filenames = []):
		# self.init_data = np.array([[]])
		# for filename in filenames:
		# 	self.loadtxt(filename)
	def __init__(self, filename):
		self.loadtxt(filename)
		self.data_preprocess()
		self.set_group_num()	# 默认值为10
		self.data_process()

	def loadtxt(self, filename):
		self.init_data = np.loadtxt(filename)

	def data_join(self, con_cat):
		self.init_data = np.concatenate((self.init_data, con_cat), axis=0)
		end_time = self.init_data[-1,0]
		num = int(con_cat.shape[0])
		for i in range(0,num):
			con_cat[i,0] = con_cat[i,0] + end_time
		self.init_data = np.concatenate((self.init_data, con_cat), axis=0)
		self.data_preprocess()
		self.data_process()

	# 数据预处理：将时间相同的数据删除一组
	def data_preprocess(self):
		i = 1
		while (int(self.init_data.shape[0])-i>0):
			if (self.init_data[i,0]-self.init_data[i-1,0])<1:
				self.init_data = np.delete(self.init_data, i, axis = 0)
				i=i-1
			i = i+1


	# 数据处理：
	def data_process(self):
		# 将直接测量量转换成实际物理量
		self.data_num = int(self.init_data.shape[0]) # 数据个数
		self.data_time = (self.init_data[:,0]/10000.0).reshape(self.data_num,1) # 时间
		self.data_voltage = (self.init_data[:,1]/1000.0).reshape(self.data_num,1) # 电压
		self.data_current = (self.init_data[:,2]/1000.0).reshape(self.data_num,1) # 电流
		data_angle = (self.init_data[:,3]/10.0).reshape(self.data_num,1) # 转过总角度
		self.data_roll_rate = self.diff(data_angle) # 角速度
		self.data_delta_I_t = self.diff(self.data_current) # dI/dt 电流对时间的微分
		
		self.data = np.column_stack((self.data_time, self.data_voltage, self.data_current, self.data_roll_rate)) # 由时间、电压、电流和角速度组成的数据矩阵
		self.solve('easy')  # solve_data_easy，不考虑摩擦转矩的结果,调用方法self.solve_data_easy['R_m']，下同
		self.solve('hard')	# solve_data_hard,考虑摩擦转矩的结果
		self.check('easy')	# check_data_easy,分组计算的结果，不考虑摩擦转矩
		self.check('hard')	# check_data_hard,分组计算的结果，考虑摩擦转矩
							# check_easy_mean check_hard_mean，分组计算结果的平均数
							# check_easy_var check_hard_var，分组计算结果的方差	


	# 得到各种初始数据
	def get_num(self):
		return self.data_num

	def get_time(self):
		return self.data_time

	def get_voltage(self):
		return self.data_voltage

	def get_current(self):
		return self.data_current

	def get_roll_rate(self):
		return self.data_roll_rate

	def get_data(self):
		return self.data

	def get_data_mean(self):
		return {'voltage':self.data_mean(self.data_voltage),'current':self.data_mean(self.data_current),
			'roll_rate':self.data_mean(self.data_roll_rate)}

	def get_data_var(self):
		return {'voltage':self.data_var(self.data_voltage),'current':self.data_var(self.data_current),
			'roll_rate':self.data_var(self.data_roll_rate)}

	def get_init_data(self):
		return self.init_data

	def get_group_num(self):
		return self.group_num


	# 得到拟合的结果
	# mode'easy'返回不考虑摩擦转矩的结果，'hard'返回考虑摩擦转矩的结果，下同
	# 调用形式为get_solve('模式')['参数代号']，例如：motordata.get_solve('easy')['R_m']
	def get_solve(self, mode = 'easy'):
		if mode == 'easy':
			return self.solve_data_easy
		elif mode == 'hard':
			return self.solve_data_hard
		else:
			return False


	# 得到数据分组拟合的结果
	# 分组个数由set_group_num函数确定，默认值为10
	def get_check(self, mode = 'easy'):
		if mode == 'easy':
			return self.check_data_easy
		elif mode == 'hard':
			return self.check_data_hard
		else:
			return False

	# 得到数据可靠性分析的结果
	# 调用方法同get_solve
	def get_check_mean(self, mode = 'easy'):
		if mode == 'easy':
			return self.check_easy_mean
		elif mode == 'hard':
			return self.check_hard_mean

	def get_check_var(self, mode = 'easy'):
		if mode == 'easy':
			return self.check_easy_var
		elif mode == 'hard':
			return self.check_hard_var


	# 求微分函数
	def diff(self,init_num):
		delta_data = np.zeros((self.data_num,1))
		for i in range(0,self.data_num):
			if i == 0:
				delta_data[i,0] = 0
			else:
				delta_data[i,0] = (init_num[i,0]-init_num[i-1,0])/(self.data_time[i,0]-self.data_time[i-1,0])
		return delta_data

	
	# 求数据的平均值（需输入列向量）
	def data_mean(self, data):
		return np.double(data.mean(axis = 0, dtype = np.double))

	# 求数据的方差（需输入列向量）	
	def data_var(self, data):
		return np.double(data.var(axis = 0, dtype = np.double))

	# 计算R_m, L_m, k_E, f_m
	# 数据为所有数据
	def solve(self, mode = 'easy'):
		if mode == 'easy':
			solve_G = np.mat(np.column_stack((self.data_current*self.data_current, 
											self.data_current*self.data_delta_I_t, 
											self.data_current*self.data_roll_rate)))
		elif mode == 'hard':
			solve_G = np.mat(np.column_stack((self.data_current*self.data_current, 
											self.data_current*self.data_delta_I_t, 
											self.data_current*self.data_roll_rate,
											self.data_roll_rate*self.data_roll_rate)))
		else:
			return False
		solve_G_T = solve_G.transpose()
		solve_b = np.mat(self.data_voltage*self.data_current)
		solve = (np.dot(solve_G_T, solve_G)).I.dot(solve_G_T).dot(solve_b)
		if mode == 'easy':
			self.solve_data_easy = {'R_m':solve[0,0],'L_m':solve[1,0],'k_E':solve[2,0]}	
		elif mode == 'hard':	
			self.solve_data_hard = {'R_m':solve[0,0],'L_m':solve[1,0],'k_E':solve[2,0], 'f_m':solve[3,0]}
		else:
			return False

	# 计算R_m, L_m, k_E, f_m,'easy'模式不考虑摩擦转矩，'hard'模式考虑摩擦转矩
	# 数据为给定数据数据 
	def data_solve(self, mode, data_voltage, data_current, data_delta_I_t, data_roll_rate):
		if mode == 'easy':
			solve_G = np.mat(np.column_stack((data_current*data_current, 
											data_current*data_delta_I_t, 
											data_current*data_roll_rate)))
		elif mode == 'hard':
			solve_G = np.mat(np.column_stack((data_current*data_current, 
											data_current*data_delta_I_t, 
											data_current*data_roll_rate,
											data_roll_rate*data_roll_rate)))
		else:
			return False
		solve_G_T = solve_G.transpose()
		solve_b = np.mat(data_voltage*data_current)
		solve = (np.dot(solve_G_T, solve_G)).I.dot(solve_G_T).dot(solve_b)
		if mode == 'easy':
			solve_data_easy = {'R_m':solve[0,0],'L_m':solve[1,0],'k_E':solve[2,0]}
			return solve_data_easy		
		elif mode == 'hard':	
			solve_data_hard = {'R_m':solve[0,0],'L_m':solve[1,0],'k_E':solve[2,0], 'f_m':solve[3,0]}
			return solve_data_hard
		else:
			return False

	# 设置检验时分组的个数
	def set_group_num(self, group_num = 10):
		self.group_num = group_num
	
	# 拟合结果的统计特征
	def check(self, mode = 'easy'):
		group_num = self.group_num
		per_group_num = self.data_num/int(group_num)
		if mode == 'easy':
			data_check = np.zeros((int(group_num),3))
		elif mode == 'hard':
			data_check = np.zeros((int(group_num),4))
		else:
			return False
		for i in range(0, group_num):
			solve = self.data_solve(mode,self.data_voltage[per_group_num*i:per_group_num*(i+1),0].reshape(-1,1),
									self.data_current[per_group_num*i:per_group_num*(i+1),0].reshape(-1,1),
									self.data_delta_I_t[per_group_num*i:per_group_num*(i+1),0].reshape(-1,1),
									self.data_roll_rate[per_group_num*i:per_group_num*(i+1),0].reshape(-1,1))
			data_check[i,0] = solve['R_m']
			data_check[i,1] = solve['L_m']
			data_check[i,2] = solve['k_E']
			if mode == 'hard':
				data_check[i,3] = solve['f_m']
			else:
				pass
		# end_num = per_group_num*(group_num-1)
		# solve = self.data_solve(mode,self.data_voltage[end_num:self.data_num,0].reshape(-1,1),
		# 							self.data_current[end_num:self.data_num,0].reshape(-1,1),
		# 							self.data_delta_I_t[end_num:self.data_num,0].reshape(-1,1),
		# 							self.data_roll_rate[end_num:self.data_num,0].reshape(-1,1))
		# data_check[group_num-1,0] = solve['R_m']
		# data_check[group_num-1,1] = solve['L_m']
		# data_check[group_num-1,2] = solve['k_E']
		# if mode == 'hard':
		# 	data_check[i,3] = solve['f_m']
		# else:
		# 	pass
		if mode == 'easy':
			self.check_data_easy = {'R_m':data_check[:,0].reshape(-1,1),'L_m':data_check[:,1].reshape(-1,1),
							'k_E':data_check[:,2].reshape(-1,1)}
			self.check_easy_mean = {'R_m':self.data_mean(self.check_data_easy['R_m']),
							'L_m':self.data_mean(self.check_data_easy['L_m']),
							'k_E':self.data_mean(self.check_data_easy['k_E'])}
			self.check_easy_var = {'R_m':self.data_var(self.check_data_easy['R_m']),
							'L_m':self.data_var(self.check_data_easy['L_m']),
							'k_E':self.data_var(self.check_data_easy['k_E'])}
		elif mode == 'hard':
			self.check_data_hard = {'R_m':data_check[:,0].reshape(-1,1),'L_m':data_check[:,1].reshape(-1,1),
							'k_E':data_check[:,2].reshape(-1,1), 'f_m':data_check[:,3].reshape(-1,1)}
			self.check_hard_mean = {'R_m':self.data_mean(self.check_data_hard['R_m']),
							'L_m':self.data_mean(self.check_data_hard['L_m']),
							'k_E':self.data_mean(self.check_data_hard['k_E']),
							'f_m':self.data_mean(self.check_data_hard['f_m'])}
			self.check_hard_var = {'R_m':self.data_var(self.check_data_hard['R_m']),
							'L_m':self.data_var(self.check_data_hard['L_m']),
							'k_E':self.data_var(self.check_data_hard['k_E']),
							'f_m':self.data_var(self.check_data_hard['f_m'])}
			# self.check_data = {{}}
			# self.check_mean = {{}}
			# self.check_var = {{}}
			# keys = ['R_m', 'L_m', 'k_E']
			# if mode == 'hard':
			# 	keys.append('f_m')
			# for i in range(keys):
			# 	key = keys[i]
			# 	self.check_data[mode][key] = data_check[:,i].reshape(-1,1)
			# 	self.check_mean[mode][key] = self.data_mean(self.check_data[key])
			# 	self.check_var[mode][key] = self.data_var(self.check_data[key])


	# # 不考虑摩擦转矩时计算R_m, L_m, k_E
	# def solve_easy(self):
	# 	solve_G = np.mat(np.column_stack((self.data_current, self.data_delta_I_t, self.data_roll_rate)))
	# 	solve_G_T = solve_G.transpose()
	# 	solve_b = np.mat(self.data_voltage)
	# 	solve = (np.dot(solve_G_T, solve_G)).I.dot(solve_G_T).dot(solve_b)
	# 	solve_easy = {'R_m':solve[0,0],'L_m':solve[1,0],'k_E':solve[2,0]}
	# 	return solve_easy