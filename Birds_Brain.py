import numpy as np
import pickle

# pickle_in = open("training_data.pickle", "rb")
# data = pickle.load(pickle_in)

# x = []
# y = []

# data = data[0]
# for arr in data:
# 	x.append(arr[:-1])
# 	y.append(arr[3])

# x = np.asarray(x)
# y = np.asarray(y)

# x_test = x[-10:]
# y_test = y[-10:]

# print(x)


def return_random():
	rand = np.random.randint(10)
	if(rand<7):
		return 0
	else:
		return 1

