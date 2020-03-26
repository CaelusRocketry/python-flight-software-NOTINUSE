class Kalman:

	def __init__(self, process_variance, measurement_variance, kalman_value):
		self.process_variance = process_variance ** 2
		self.measurement_variance = measurement_variance ** 2
		self.kalman_value = kalman_value
		self.sensor_value = kalman_value
		self.P, self.K = 1.0, 1.0
		self.kalman_value_list = []
		self.sensor_value_list = []

	def update_kalman(self, sensor_value):
		self.P += self.process_variance
		self.K = self.P / (self.P + self.measurement_variance)
		self.kalman_value = self.K * sensor_value + (1 - self.K) * self.kalman_value
		self.P *= (1 - self.K)

		self.kalman_value_list.append(self.kalman_value)
		self.sensor_value_list.append(sensor_value)
		return self.kalman_value