import numpy as np
import random
#this takes in two 2D arrays and creates another array which is the average of the inputs
def add_arrays(a1, a2):
	a1 = np.array(a1)
	a2 = np.array(a2)	
	array = a1+a2
	array /= 2
	return array


def mutate_2D(array):
	array = np.array(array)
	shape = array.shape
	for _ in range(3):
		num1 = random.randint(0,shape[0]-1)
		num2 = random.randint(0,shape[1]-1)
		array[num1][num2] += random.uniform(-0.001,0.001)
	return array

def mutate_1D(array):
	for _ in range(3):
		num = random.randint(0,len(array)-1)
		array[num] += random.uniform(-0.001,0.001)
	return array

