# genetic algorithm search for the test coverage problem
# this is the multi-objective version of the problem

from numpy.random import randint
from numpy.random import rand
import matplotlib.pyplot as plt

import copy
class TestDatabase:
	# This class represents our test database
	# It is already implemented, no need to change it if you don't want

	def __init__(self):
		self.coverage=[]
		self.time=[]

	def get_time(self,i):
		return self.time[i]

	def get_coverage(self,i):
		return self.coverage[i]

	def get_number_of_tests(self):
		return len(self.time)

	def init_random(self,n_tests, max_time, max_code, p=0.05):
		# initialize a test database randomly
		self.coverage = []
		self.time = []

		for i in range(n_tests):
			t_time= randint(1,max_time)
			t_coverage=[]
			for i in range(1,max_code+1):
				if rand()<p:
					t_coverage.append(i)
			self.time.append(t_time)
			self.coverage.append(t_coverage)


	def load_from_file(self,fn):
		# load test database from file with name fn
		# file format:
		#  line i represents test i as comma separated value
		#   the first value is the time to execute the test
		#   the other values are the lines covered by the test
		#  Example
		#   5, 1, 5, 7   -> A test that covers lines 1,5,7 and takes 5 seconds to run

		self.coverage = []
		self.time = []
		with open(fn,'rt') as fd:
			for line in fd.readlines():
				words=line.split(",")
				self.time.append(float(words[0]))
				self.coverage.append(list(map(lambda x: int(x), words[1:])))

	def write_to_file(self,fn):
		# write the test database to a file with name fn
		with open(fn, 'wt') as fd:
			for time, coverage in zip(self.time, self.coverage):
				fd.write(str(time))
				for i in coverage:
					fd.write(", "+str(i))
				fd.write("\n")


# Each solution is a set of tests and has two objectives
# total execution time, to be minimized
# total program coverage, to be maximized

def objectives(x, db):
	# returns the objectives of a solution
	# this function is ready
	coverage  = set()
	total_time = 0

	for i in range(len(x)):
		if x[i] == 1:
			total_time = total_time + db.get_time(i)
			coverage = coverage.union( db.get_coverage(i))

	return (total_time, len(coverage))

# fitness function
def fitness(x, db):
	# TODO implement a fitness function
	# You do not want to use the same fitness function as in your solution for Week 5

	o1,o2 =objectives(x,db)

	# This is a not a good fitness function!
	return 1/o1+0.5*o2

# selection
def selection(population, scores):
	# TODO implement a (better) selection function
	# Your selection operator should be aware of the
	# multiple objectives and the population pareto front

	# Here we just select an individual at random
	# this is a bad strategy... you should implement something better
	selection_ix = randint(len(population))
	return population[selection_ix]

# crossover two parents to create two children
def crossover(p1, p2, r_cross):
	# TODO implement a (better) crossover function
	# You can probably use the same operator as in your solution for Week 5

	# children are copies of parents by default
	c1, c2 = p1.copy(), p2.copy()
	return [c1, c2]

# mutation operator
def mutation(bitstring, r_mut):
	# TODO implement a (better) mutation function
	# You can probably use the same operator as in your solution for Week 5
	for i in range(len(bitstring)):
		pass

def pareto_domination(a,b,db):
	# Returns True if solution a dominates solution b ?

	# First objective (time) should be minimized
	# The second objective (coverage) should be maximized

	r= False
	if objectives(a,db)[0] < objectives(b,db)[0]:
		r = True
	elif  objectives(b,db)[0] < objectives(a,db)[0]:
		return False
	if objectives(a,db)[1] > objectives(b,db)[1]:
		r = True
	elif  objectives(b,db)[1] > objectives(a,db)[1]:
		return False
	return r

def pareto_front(population,db):
	# Returns the pareto front of the population

	r= set()
	for p in population:
		r.add(tuple(p))
		for i in copy.copy(r):
			if i == tuple(p):
				continue
			if pareto_domination(i,p,db):
				r.remove(tuple(p))
				break
			elif pareto_domination(p,i,db):
				r.remove(tuple(i))
	return r

# genetic algorithm
# This is ready, no need to change it if you don't want
def genetic_algorithm(db, fitness, n_bits, n_iter, n_pop, r_cross, r_mut):
	# initial population of random bitstring
	population = [randint(0, 2, n_bits).tolist() for _ in range(n_pop)]

	# enumerate generations
	for gen in range(n_iter):
		# evaluate all candidates in the population
		scores = [fitness(c,db ) for c in population]
		# select parents
		selected = [selection(population, scores) for _ in range(n_pop)]
		# create the next generation
		children = list()
		for i in range(0, n_pop, 2):
			# get selected parents in pairs
			p1, p2 = selected[i], selected[i+1]
			# crossover and mutation
			for c in crossover(p1, p2, r_cross):
				# mutation
				mutation(c, r_mut)
				# store for next generation
				children.append(c)
		# replace population
		population = children

		# plot progress
		if gen % 10 == 0:
			plot_population(gen, population,db)

	# plot final population
	plot_population(n_iter, population, db)
	return pareto_front(population,db), population

# show a plot with the population and the pareto front
def plot_population(generation,population, db):
	front=pareto_front(population, db)
	plt.scatter(list(map(lambda i: objectives(i, db)[0], population)),
				list(map(lambda i: objectives(i, db)[1], population)), color="blue")
	plt.scatter(list(map(lambda i: objectives(i, db)[0], front)),
				list(map(lambda i: objectives(i, db)[1], front)), color="red")
	plt.title("Generation "+str(generation))
	plt.xlabel("Time")
	plt.ylabel("Code Coverage")
	plt.show()

# intialize the problem
db= TestDatabase()
db.load_from_file("problem1.txt")

# define the total iterations, you can change this
n_iter = 100
# bits: one bit per each test that may be executed
n_bits =  db.get_number_of_tests()
# define the population size, you can change this
n_pop = 100
# crossover rate, you can change this
r_cross = 0.9
# mutation rate, you can change this
r_mut = 1.0 / float(n_bits)

# perform the genetic algorithm search
front, population= genetic_algorithm(db, fitness, n_bits, n_iter, n_pop, r_cross, r_mut)


