data = 0
P = 1.0
varP = 0.01 ** 2
varM = 0.01 ** 2
K = 1.0
Kalman = 2500.0

data_list = []
kalman_list = []
index_list = [i for i in range(100)]

for i in range(100):
   data = random.randrange(2450, 2550)
   if 50 <= i <= 51:
      data = 2900
   data_list.append(data)
   P = P + varP
   K = P / (P + varM)
   Kalman = K * data + (1 - K) * Kalman
   P = (1 - K) * P
   kalman_list.append(Kalman)

plt.figure()
measured_data = plt.plot(index_list, data_list, color='g')
kalman_data = plt.plot(index_list, kalman_list, color='b')
plt.axis([0, 100, 2000, 3000])
plt.show()
