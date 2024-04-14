# genetic algorithm search of the test coverage problem
from numpy.random import randint
from numpy.random import rand

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

# fitness function, it is ready, no need to change it
def fitness(x, db, max_time):
	coverage  = set()
	total_time = 0

	for i in range(len(x)):
		if x[i] == 1:
			coverage = coverage.union( db.get_coverage(i))
			total_time = total_time + db.get_time(i)

	if total_time <= max_time:
		return len(coverage)
	else:
		return 0


# selection
def selection(population, scores):
	# TODO implement a (better) selection function

	# Here we just select an individual at random
	# this is a bad strategy... you should implement something better
	selection_ix = randint(len(population))
	return population[selection_ix]

# crossover two parents to create two children
def crossover(p1, p2, r_cross):
	# TODO implement a (better) crossover function

	# children are copies of parents by default
	c1, c2 = p1.copy(), p2.copy()
	return [c1, c2]

# mutation operator
def mutation(bitstring, r_mut):
	# TODO implement a (better) mutation function
	for i in range(len(bitstring)):
		pass


# genetic algorithm
# This is ready, no need to change it if you don't want
def genetic_algorithm(db, maxtime, fitness, n_bits, n_iter, n_pop, r_cross, r_mut):
	# initial population of random bitstring
	population = [randint(0, 2, n_bits).tolist() for _ in range(n_pop)]
	# keep track of best solution
	best, best_eval = 0, fitness(population[0],db,maxtime)

	# enumerate generations
	for gen in range(n_iter):
		# evaluate all candidates in the population
		scores = [fitness(c,db,maxtime ) for c in population]
		# check for new best solution
		for i in range(n_pop):
			if scores[i] > best_eval:
				best, best_eval = population[i], scores[i]
				print(">%d, new best f(%s) = %.3f" % (gen,  population[i], scores[i]))
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
	return [best, best_eval]


# intialize the problem
db= TestDatabase()
db.load_from_file("problem1.txt")
max_time=1000

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
best, score = genetic_algorithm(db, max_time, fitness, n_bits, n_iter, n_pop, r_cross, r_mut)
print('Done!')
print('f(%s) = %f' % (best, score))