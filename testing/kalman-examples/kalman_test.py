import matplotlib.pyplot as plt

data = 0
P = 1.0
varP = 0.01 ** 2
varM = 0.01 ** 2
K = 1.0
Kalman = 100

data_list = [19, 59, 1045, 30, 1058, 1015, 14, 4074, 27, 56, 92, 68, 62, 47, 79, 64, 1076, 33, 60, 67, 77, 1046, 14, 33, 52]
kalman_list = []
index_list = [i for i in range(25)]

for i in range(25):
   # data = random.randrange(2450, 2550)
   #    # if 50 <= i <= 51:
   #    #    data = 2900
   #    # data_list.append(data)
   data = data_list[i]
   P = P + varP
   K = P / (P + varM)
   Kalman = K * data + (1 - K) * Kalman
   P = (1 - K) * P
   kalman_list.append(Kalman)

plt.figure()
measured_data = plt.plot(index_list, data_list, color='g')
kalman_data = plt.plot(index_list, kalman_list, color='b')
plt.axis([0, 25, 0, 5000])
plt.show()
print(kalman_list)