import pygame
import numpy as np
import Birds_Brain as brain
import pickle
import Neural_Net as nn
import sys
import Matrixs

#Globals
screen_width = 800
screen_height = 600
tick_length = 100

population = 100
counter = 1
gen = 0
pillars = []
birds = []
dead_birds = []
exit = False
pillar_speed = 6

RED = (255,0,0)
BLACK = (0,0,0)
WHITE = (255,255,255)



#Initialise pygame
pygame.init()
screen = pygame.display.set_mode([screen_width,screen_height])
pygame.display.set_caption('Flappy Bird')
clock = pygame.time.Clock()



###My Classes

#class for the bird
class _Bird:
	def __init__(self):
		self.x = screen_width/3
		self.y = screen_height/2
		self.velocity = 0
		self.gravity = 1
		self.neural_net = nn.Neural_Network(3,4,1)
		self.colour = (np.random.randint(255),np.random.randint(255),np.random.randint(255))

	def update(self):
		self.velocity+=self.gravity
		self.y+=self.velocity	
	
	def draw(self):
		pygame.draw.ellipse(screen, self.colour, [self.x, self.y, 20, 20])

	def jump(self):
		self.velocity = -15

	#The folliwing two methods are for the neural net
	def decide(self):
		data = self.find_pole()
		data.append(int(self.y))
		choice = self.neural_net.predict(data)[0]
		if (choice > 0.5):
			self.jump()
	
	def find_pole(self):
			for i in range(len(pillars)):
				if (pillars[i].x>self.x):
					x_dist = int(pillars[i].x-self.x)
					y_dist = int((pillars[i].top+(pillars[i].gap/2)) - self.y)
					return [(x_dist), (y_dist)]


	def return_neural_network_weights(self):
		return self.neural_net.return_weights()
	def set_neural_network_weights(self, weights):
		self.neural_net.change_weights(weights)

					
#Class to create pillars
class pillar:
	def __init__(self):
		self.top = np.random.randint(screen_height - ((screen_height/5)*3), screen_height - ((screen_height/5)))
		self.gap = 100
		self.bottom = screen_height - (self.top+self.gap)
		self.width = 30
		self.x = screen_width
		self.move_rate = pillar_speed
		self.passed = False
		

	######NEED MORE ELEGANT SOLUTION FOR CHECKING TO MAKE SURE THE GAME DOESNT GO TOO SLOW
	def move(self):
		self.x -= self.move_rate
		if(self.x < screen_width/3 and self.x+self.width > screen_width/3):
			check_collision(self.top, self.gap)

		if(self.passed == False and self.x < (screen_width/2)):
			add_pillar()
			self.passed = True


	def draw(self):
		pygame.draw.rect(screen, BLACK, [self.x,0, self.width, self.top])
		pygame.draw.rect(screen, BLACK, [self.x, screen_height-self.bottom, self.width, self.bottom])

	




###My Methods

def check_collision(top, gap):
	global birds, dead_birds
	for index, bird in enumerate(birds):
		if (bird.y < top or bird.y> top+gap):
			dead_birds.append(birds.pop(index))

#updates generation
def make_new_generation():
	#intitiate all the variables
	global birds, dead_birds
	fill_bird_array()
	#this gives top %10 of previous population
	num = int(population / 10)
	good_birds = dead_birds[-num:]
	best_bird = dead_birds[population-1]
	

	for i in range(population-int(num/2)):
		if (i< num):
			weights = good_birds[i].return_neural_network_weights()
		#mutates the first bunch of birds
		elif(i<population/2):
			weights = best_bird.return_neural_network_weights()
			weights[0] = Matrixs.mutate_2D(weights[0])
			weights[1] = Matrixs.mutate_1D(weights[1])

		#combines random birds
		else:
			weights1 = best_bird.return_neural_network_weights()
			weights2 = good_birds[np.random.randint(num)].return_neural_network_weights()
			return_arr1 = Matrixs.add_arrays(weights1[0],weights2[0])
			return_arr2 = Matrixs.add_arrays(weights1[1],weights2[1])
			weights = [return_arr1, return_arr2]

		birds[i].set_neural_network_weights(weights)

		

#Resets game to the start
def set_game():
	global pillars, gen, counter, pillar_speed
	print("Generation: ", gen, "      Score: ", counter)

	make_new_generation()
	pillars = []
	add_pillar()
	pillar_speed = 7
	counter = 0
	gen += 1
	if(not exit):
		loop()
	

#fills bird array
def fill_bird_array():
	global birds
	for _ in range(population):
		birds.append(_Bird())

#adds pillar
def add_pillar():
	pillars.append(pillar())

#pygame loop
def loop():
	global counter, exit, pillar_speed
	end = False
	while not end:
		#gets inputs - for when a user is playing
		for event in pygame.event.get():
			
			if event.type == pygame.QUIT:
				exit = True
				end = True
				break

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE:
					birds[0].jump()			


		#this is to do some checks every once in a while
		if (counter % 50 == 0):

			#get rid of any pillars to the left so the list doesnt get massive
			if (pillars[0].x<0):
				del pillars[0]

			#check if all the birds are dead
			if (len(birds) == 0):
				end = True
				break
				

		#Decide if the birds should jump
		for i in birds:
		 		i.decide()

		##All the stuff here is the main loop for printing to the pygame window and moving objects
		screen.fill(WHITE)

		#update bird       
		for i in birds:
			i.update()			
			i.draw()


		#update pillars
		for i in pillars:
			i.move()
			i.draw()

		pygame.display.flip()

		if (counter % 1000 == 0 ):
			pillar_speed+=1
			print("Num birds alive: ",len(birds))

		counter += 1
		clock.tick(tick_length)

	set_game()

fill_bird_array()
add_pillar()
loop()


