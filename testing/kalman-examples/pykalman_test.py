from pykalman import KalmanFilter
import matplotlib.pyplot as plt
import numpy as np

# specify parameters
random_state = np.random.RandomState(0)
transition_matrix = [[1, 0.1], [0, 1]]
transition_offset = [-0.1, 0.1]
observation_matrix = np.eye(2) + random_state.randn(2, 2) * 0.1
observation_offset = [1.0, -1.0]
transition_covariance = np.eye(2)
observation_covariance = np.eye(2) + random_state.randn(2, 2) * 0.1
initial_state_mean = [5, -5]
initial_state_covariance = [[1, 0.1], [-0.1, 1]]

# sample from model
kf = KalmanFilter(
    transition_matrix, observation_matrix, transition_covariance,
    observation_covariance, transition_offset, observation_offset,
    initial_state_mean, initial_state_covariance,
    random_state=random_state
)
states, observations = kf.sample(
    n_timesteps=50,
    initial_state=initial_state_mean
)

# estimate state with filtering and smoothing
filtered_state_estimates = kf.filter(observations)[0]
smoothed_state_estimates = kf.smooth(observations)[0]

# draw estimates
plt.figure()
lines_true = plt.plot(states, color='b')
# lines_filt = plt.plot(filtered_state_estimates, color='r')
lines_smooth = plt.plot(smoothed_state_estimates, color='g')
# plt.legend((lines_true[0], lines_filt[0], lines_smooth[0]),
#           ('true', 'filt', 'smooth'),
#           loc='lower right'
# )
plt.legend((lines_true[0], lines_smooth[0]),
          ('true', 'smooth'),
          loc='lower right'
)
plt.show()