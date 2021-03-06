import random

class GeneticOperations():
	def __init__(self):

		self.params = {
			'populationSize': 20,
			'tournamentNumber': 3,
			'generationNumber': 1,
			'mutationRate': (1,2)
		}
	def distance(self, p1, p2):
		#calculates distance from two points
		d = (((p2[0] - p1[0])**2) + ((p2[1] - p1[1])**2))**.5
		return int(d)



	def tournamentSelection(self, population):
		"""
			Function will select three individuals, then make the mating pair
			fitnessLink maps the sequence to the fitness Value for easy comparison and sorting
		"""

		fitnessLink = {}

		#randomly selects n number of candidates from the population. Sample is great because it cannot select repeats
		selectedIndividuals = random.sample(population, self.params['tournamentNumber'])


		for individual in selectedIndividuals:
			fitnessLink[str(self.fitnessEvaluation(individual))] = individual


		#to find the sequences with the lowest travel time, the fitness values are sorted and matched aganist the orginal dictionary
		fitnessOrdered = sorted(map(int, fitnessLink.keys()))
		matingPair = (fitnessLink[str(fitnessOrdered[0])], fitnessLink[str(fitnessOrdered[1])])

		return matingPair


	def fitnessEvaluation(self, individual):
		"""Takes an individual, returns the fitness value (travelCost) by summing the costs of each node"""

		travelCost = 0


		#loop will go through each node and calculate the distance between the two of them
		for i in range(1, len(individual)):
			p1 = Nodes[str(individual[i-1])]
			p2 = Nodes[str(individual[i])]
			travelCost += self.distance(p2, p1) #distance formula

		return travelCost



	def crossover(self, mates):
		"""
		Crossover will take mates, and will return one child.
		A splice is taken from the mother and inserted into child
		The nodes in the father are added to the child, if and only if, they do not
		appear in the splice. Offspring cannot have duplicates.

		"""

		mates = list(mates)
		random.shuffle(mates)#switching up who is mother and father a bit
		mother = mates[0]
		father = mates[1]
		child = [None] * len(mother)



		#setting start and endpoints for sequence to be crossed. Sorted makes sure its always
		#in least to greatest. Sample makes sure there are no duplicates
		points = sorted(random.sample(list(range(0,len(mother))), 2))
		start = points[0]
		end = points[1]

		spliced = mother[start:end]
		child[start:end] = spliced
		print('initial Child: ', child)

		pointer = 0
		for index, slot in enumerate(child):
			if slot == None:
				gene = father[pointer]
				while gene in spliced:
					pointer +=1
					gene = father[pointer]

				child[index] = father[pointer]
				pointer += 1

		print("Mother: ", mother)
		print("Father: ", father)
		print("Points: ", points)
		print('Spliced: ', spliced)
		print('Final Child: ', child)

	def mutation(self, candidate):
		"""
			Mutation is vital to add genetic diversity
			a random number, r, is generated and if that matches the mutation rate then a swap mutation will occur
			a swap is necessary in order to produce a valid sequence
		"""
		r = random.randint(1,100)


		if r in self.params['mutationRate']:
			print("Mutation will occur on: ", candidate)
			points = sorted(random.sample(list(range(0,len(candidate))), 2))
			candidate[points[0]], candidate[points[1]] = candidate[points[1]], candidate[points[0]]
			print("Candidate after mutation: ", candidate)
			return candidate
		else:
			return candidate

#Function will create initial Population. Size is length of pop, eleSize is length of TSP
def generatePopulation(size,eleSize):
	"""
	Creates the initial population. 1 is the origin so it must be the first node
	"""

	P = [] #holds population
	lang = tuple([ x for x in range(2,eleSize+1) ]) #generating matching node names

	#Loop creates the n number of candidates
	for candidate in range(0, size):

		chromosome = []
		poss = list(lang)

		#loops to create visiting sequence
		while len(poss) != 0:

			selected = random.choice(poss) #randomly chooses a possible node
			del poss[poss.index(selected)] #deletes that node so it doesnt repeat
			chromosome.append(selected)

		chromosome.insert(0,1)
		P.append(chromosome)

	return P


#Controlling Evolution function. Actual generation iteration happens here
def Evolution(population, params):
	print(population, end='\n\n')
	input('Ready?')

	#TERMINATION CONDITION GOES HERE
	for x in range(0, params['generationNumber']):
		newPopulation = []
		mates = []

		#run for half the population. Each mate pair will make two children
		while len(newPopulation) != params['populationSize']:
			mates = G.tournamentSelection(population)
			child = G.crossover(mates)
			newPopulation.append(child)

		for candidate in newPopulation:
			#Attempts to mutate. If mutation does not occur then return candidate back to population to restart cycle
			population.append(G.mutation(candidate))

		display(population, x)



def display(population, x):
	costs = []
	for individual in population:
		costs.append(G.fitnessEvaluation(individual))

	lowestsCost = min(costs)
	selectIndiv = population[costs.index(lowestCost)]


	print("Generation Number: ", x,end="\n")
	print("Fittest Individual: " + ' '.join(list(map(str, selectIndiv))), end='\n')
	print("Travel Cost: " + str(lowestCost),end='\n')
	input("Continue...")



def main():
	global G
	global Nodes

	Nodes = {
		'1': (565.0, 575.0),
		'2': (25.0, 185.0),
		'3': (345.0, 750.0),
		'4': (945.0, 685.0),
		'5': (845.0, 655.0),
		'6': (880.0, 660.0),
		'7': (25.0, 230.0),
		'8': (525.0, 1000.0),
		'9': (580.0, 1175.0),
		'10': (650.0, 1130.0),
		'11': (1605.0, 620.0),
		'12': (1220.0, 580.0),
		'13': (1465.0, 200.0),
		'14': (1530.0, 5.0),
		'15': (845.0, 680.0)
	}


	G = GeneticOperations()


	population = generatePopulation(G.params['populationSize'], len(Nodes))
	Evolution(population, G.params)


if __name__ == '__main__':
	main()
