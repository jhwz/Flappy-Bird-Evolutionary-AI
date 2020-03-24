import numpy as np


#This is a neural network with only one hidden layer, but you can define the sizes of all three 
#layers and get a value back between 0 and 1
class Neural_Network:
	def __init__(self, inpt, hl, out):
		#Sizes of network
		self._input_size = inpt
		self._hidden_size = hl
		self._output_size = out
		
		#Arrays to hold all the values
		self.weight_array_one = self.set_weights(self._input_size, self._hidden_size)
		self.weight_array_two = self.set_weights(self._hidden_size, self._output_size)
		
		self.hidden = np.zeros(self._hidden_size)
		self.outputs = np.zeros(self._output_size)
		self.bias = 1


	#activation function
	def sigmoid(self,x):
		return 1/(1+np.exp(-x))
		
	#this defines a bunch of random weights between the input layer and hidden layer
	def set_weights(self, layer_one_size, layer_two_size):
		array = np.zeros((layer_two_size, layer_one_size))
		for i in range(layer_two_size):
			for j in range(layer_one_size):
				array[i][j] = np.random.uniform(-1,1)
		return array
	
	#this function gets the random weights and the previous layer, and adds them all up to 
	#get the value of each neuron for current layer
	def set_next_layer(self, prev_layer, weights, layer_size):
		array = np.zeros(layer_size)
		for i in range(layer_size):
			for j in range(len(prev_layer)):
				array[i] += prev_layer[j] * weights[i][j]
			array[i] = self.sigmoid(array[i])
		return array 

	
	def return_weights(self):
		return [self.weight_array_one, self.weight_array_two]
		
	def change_weights(self, array):
		self.weight_array_one = array[0]
		self.weight_array_two = array[1]


	#The main function for the network
	def predict(self, input_vals):
		if (len(input_vals) == self._input_size):
			#sets hidden layer
			self.hidden = self.set_next_layer(input_vals, self.weight_array_one, self._hidden_size)
			#sets outputs
			self.outputs = self.set_next_layer(self.hidden, self.weight_array_two, self._output_size)
			return self.outputs
		else:
			print("Input array was of incorrect size")



test = Neural_Network(3,5,3)

