



from pykalman import KalmanFilter
import numpy as np
import matplotlib.pyplot as plt
import time
measurements = np.asarray([399, 403, 409, 416, 418, 420, 429, 423, 429, 431, 433, 434, 434, 433, 431, 430, 428, 427, 425, 429, 431, 410, 406, 402, 397, 391, 376, 372, 351, 336, 327, 307])
initial_state_mean = [measurements[0], 0]
times = range(measurements.shape[0])
transition_matrix = [[1, 1],
                   [0, 1]]
observation_matrix = [[1, 0]]
# kf1 is used to find the observation covariance, 10x of that value is used in kf3
kf1 = KalmanFilter(transition_matrices = transition_matrix,
                observation_matrices = observation_matrix,
                initial_state_mean = initial_state_mean)
kf1 = kf1.em(measurements, n_iter=5)
(smoothed_state_means, smoothed_state_covariances) = kf1.smooth(measurements)
# Number of real time data points, we won't use this variable in the actual thing
n_real_time = 3
# kf3 is the "model" that we train and later use to guess future data points
kf3 = KalmanFilter(transition_matrices = transition_matrix,
                observation_matrices = observation_matrix,
                initial_state_mean = initial_state_mean,
                observation_covariance = 10*kf1.observation_covariance,
                em_vars=['transition_covariance', 'initial_state_covariance'])
# This is where we trian on the "training data", which is really just the first few points
kf3 = kf3.em(measurements[:-n_real_time], n_iter=5)
time_before = time.time()
(filtered_state_means, filtered_state_covariances) = kf3.filter(measurements[:-n_real_time])
print("Time to build and train kf3: %s seconds" % (time.time() - time_before))
print("\n SDFSD", filtered_state_means.shape)
x_now = filtered_state_means[-1]
P_now = filtered_state_covariances[-1]
x_new = np.zeros((n_real_time,filtered_state_means.shape[1]))
i = 0
# For each new measurement (this is the live update loop)
for measurement in measurements[-n_real_time:]:
  time_before = time.time()
  # kf3.filter_update is basically the predict method
  (x_now, P_now) = kf3.filter_update(filtered_state_mean = x_now,
                                     filtered_state_covariance = P_now,
                                     observation = measurement)
  print("Time to update kf3: %s seconds" % (time.time() - time_before))
  print(x_now)
  # x_now is the normalized data point
  x_new[i] = x_now
  i = i + 1
# Plotting: Blue points are the original measurements, Blue line is the normalized line, Green points are the predicted points
plt.figure(3)
old_times = range(measurements.shape[0] - n_real_time)
new_times = range(measurements.shape[0]-n_real_time, measurements.shape[0])
plt.plot(times, measurements, 'bo',
       old_times, filtered_state_means[:, 0], 'b--',
       new_times, x_new[:, 0], 'go')
plt.show()