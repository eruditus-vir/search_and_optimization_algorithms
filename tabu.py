#!/usr/bin/python3
# -*- coding: utf-8 -*-

import math

import numpy as np

class Solution:

    def __init__(self, permutation, flows, distances):
        self.permutation = np.array(permutation)
        self.flows = flows
        self.distances = distances
        self.objective = self._evaluate_objective(self.permutation, self.flows, self.distances)

    def __str__(self):
        return str(self.permutation)

    def _evaluate_objective(self, permutation, flows, distances):
        # When doing a swap the objective can be updated with less cost, but we
        # do not care.
        objective = 0.0
        for i in range(flows.shape[0]):
            for j in range(i + 1, flows.shape[1]):
                #print(i, j)
                #print("{} * {} = {}".format(flows[i,j], distances[permutation[i], permutation[j]], flows[i, j] * distances[permutation[i], permutation[j]]))
                objective += flows[i, j] * distances[permutation[i], permutation[j]]

        # The matrices are symmetric.
        return 2*objective

    def neighbors(self, tabu=None, threshold=0):
        # TODO: Implement this. The returned value should be a list of tuples
        # (i,j) representing non-tabu swaps.
        neighborhood = []
        # ...

        return neighborhood

    def best_neighbor_swap(self, tabu=None, threshold=0):
        # TODO: Implement this. The result should be the swap (i,j), when
        # applied to self, yields the best objective value. If no such (i,j)
        # exists, None should be returned.
        best_swap = None
        best_objective = math.inf
        # ...

        return best_swap

    def swap(self, i, j):
        tmp = self.permutation[i]
        P = self.permutation.copy()
        P[i] = self.permutation[j]
        P[j] = tmp

        return Solution(P, self.flows, self.distances)

# The instance from p. 52. Notice that the book results should be multiplied by
# 2 to be correct.
F = np.array([0,1,0,1, 1,0,0,2, 0,0,0,3, 1,2,3,0]).reshape(4,4)
D = np.array([0,4,3,5, 4,0,5,3, 3,5,0,4, 5,3,4,0]).reshape(4,4)
#X = Solution([3,2,0,1], F, D)
#X = Solution([3,1,2,0], F, D)

"""
# The NUG5 problem instance from p. 54. It seems that the book has incorrect
# fitness for the proposed initial solution. Here the fitness is 70 not 72.
F = np.array([0,5,2,4,1, 5,0,3,0,2, 2,3,0,0,0, 4,0,0,0,5, 1,2,0,5,0]).reshape(5, 5)
D = np.array([0,1,1,2,3, 1,0,2,1,2, 1,2,0,1,2, 2,1,1,0,1, 3,2,2,1,0]).reshape(5, 5)
# We use 0-indexing whereas the book uses 1-indexing.
#X = Solution(np.array([2,4,1,5,3]) - 1, F, D)
"""

"""
# NUG20.
F = np.array([
[0, 1, 2, 3, 4, 1, 2, 3, 4, 5, 2, 3, 4, 5, 6, 3, 4, 5, 6, 7],
[1, 0, 1, 2, 3, 2, 1, 2, 3, 4, 3, 2, 3, 4, 5, 4, 3, 4, 5, 6],
[2, 1, 0, 1, 2, 3, 2, 1, 2, 3, 4, 3, 2, 3, 4, 5, 4, 3, 4, 5],
[3, 2, 1, 0, 1, 4, 3, 2, 1, 2, 5, 4, 3, 2, 3, 6, 5, 4, 3, 4],
[4, 3, 2, 1, 0, 5, 4, 3, 2, 1, 6, 5, 4, 3, 2, 7, 6, 5, 4, 3],
[1, 2, 3, 4, 5, 0, 1, 2, 3, 4, 1, 2, 3, 4, 5, 2, 3, 4, 5, 6],
[2, 1, 2, 3, 4, 1, 0, 1, 2, 3, 2, 1, 2, 3, 4, 3, 2, 3, 4, 5],
[3, 2, 1, 2, 3, 2, 1, 0, 1, 2, 3, 2, 1, 2, 3, 4, 3, 2, 3, 4],
[4, 3, 2, 1, 2, 3, 2, 1, 0, 1, 4, 3, 2, 1, 2, 5, 4, 3, 2, 3],
[5, 4, 3, 2, 1, 4, 3, 2, 1, 0, 5, 4, 3, 2, 1, 6, 5, 4, 3, 2],
[2, 3, 4, 5, 6, 1, 2, 3, 4, 5, 0, 1, 2, 3, 4, 1, 2, 3, 4, 5],
[3, 2, 3, 4, 5, 2, 1, 2, 3, 4, 1, 0, 1, 2, 3, 2, 1, 2, 3, 4],
[4, 3, 2, 3, 4, 3, 2, 1, 2, 3, 2, 1, 0, 1, 2, 3, 2, 1, 2, 3],
[5, 4, 3, 2, 3, 4, 3, 2, 1, 2, 3, 2, 1, 0, 1, 4, 3, 2, 1, 2],
[6, 5, 4, 3, 2, 5, 4, 3, 2, 1, 4, 3, 2, 1, 0, 5, 4, 3, 2, 1],
[3, 4, 5, 6, 7, 2, 3, 4, 5, 6, 1, 2, 3, 4, 5, 0, 1, 2, 3, 4],
[4, 3, 4, 5, 6, 3, 2, 3, 4, 5, 2, 1, 2, 3, 4, 1, 0, 1, 2, 3],
[5, 4, 3, 4, 5, 4, 3, 2, 3, 4, 3, 2, 1, 2, 3, 2, 1, 0, 1, 2],
[6, 5, 4, 3, 4, 5, 4, 3, 2, 3, 4, 3, 2, 1, 2, 3, 2, 1, 0, 1],
[7, 6, 5, 4, 3, 6, 5, 4, 3, 2, 5, 4, 3, 2, 1, 4, 3, 2, 1, 0]
])
D = np.array([
[0,  0,  5,  0,  5,  2, 10,  3,  1,  5,  5,  5,  0,  0,  5,  4,  4,  0,  0,  1],
[0,  0,  3, 10,  5,  1,  5,  1,  2,  4,  2,  5,  0, 10, 10,  3,  0,  5, 10,  5],
[5,  3,  0,  2,  0,  5,  2,  4,  4,  5,  0,  0,  0,  5,  1,  0,  0,  5,  0,  0],
[0, 10,  2,  0,  1,  0,  5,  2,  1,  0, 10,  2,  2,  0,  2,  1,  5,  2,  5,  5],
[5,  5,  0,  1,  0,  5,  6,  5,  2,  5,  2,  0,  5,  1,  1,  1,  5,  2,  5,  1],
[2,  1,  5,  0,  5,  0,  5,  2,  1,  6,  0,  0, 10,  0,  2,  0,  1,  0,  1,  5],
[10,  5,  2,  5,  6,  5,  0,  0,  0,  0,  5, 10,  2,  2,  5,  1,  2,  1,  0, 10],
[3,  1,  4,  2,  5,  2,  0,  0,  1,  1, 10, 10,  2,  0, 10,  2,  5,  2,  2, 10],
[1,  2,  4,  1,  2,  1,  0,  1,  0,  2,  0,  3,  5,  5,  0,  5,  0,  0,  0,  2],
[5,  4,  5,  0,  5,  6,  0,  1,  2,  0,  5,  5,  0,  5,  1,  0,  0,  5,  5,  2],
[5,  2,  0, 10,  2,  0,  5, 10,  0,  5,  0,  5,  2,  5,  1, 10,  0,  2,  2,  5],
[5,  5,  0,  2,  0,  0, 10, 10,  3,  5,  5,  0,  2, 10,  5,  0,  1,  1,  2,  5],
[0,  0,  0,  2,  5, 10,  2,  2,  5,  0,  2,  2,  0,  2,  2,  1,  0,  0,  0,  5],
[0, 10,  5,  0,  1,  0,  2,  0,  5,  5,  5, 10,  2,  0,  5,  5,  1,  5,  5,  0],
[5, 10,  1,  2,  1,  2,  5, 10,  0,  1,  1,  5,  2,  5,  0,  3,  0,  5, 10, 10],
[4,  3,  0,  1,  1,  0,  1,  2,  5,  0, 10,  0,  1,  5,  3,  0,  0,  0,  2,  0],
[4,  0,  0,  5,  5,  1,  2,  5,  0,  0,  0,  1,  0,  1,  0,  0,  0,  5,  2,  0],
[0,  5,  5,  2,  2,  0,  1,  2,  0,  5,  2,  1,  0,  5,  5,  0,  5,  0,  1,  1],
[0, 10,  0,  5,  5,  1,  0,  2,  0,  5,  2,  2,  0,  5, 10,  2,  2,  1,  0,  6],
[1,  5,  0,  5,  1,  5, 10, 10,  2,  2,  5,  5,  5,  0, 10,  0,  0,  1,  6,  0]
 ])
"""

assert F.shape == D.shape, "Flow and distance matrices have to be of the same shape."

# Set seed for deterministic results.
np.random.seed(2023)

# X is the current solution.
X = Solution(np.random.permutation(D.shape[0]), F, D)
# This is the tabu list.
# TODO: Initialize an appropriate Numpy array called tabu which corresponds to
# the tabu list described on p. 54 of the book.
tabu = ...
# Tenure for tabu solutions.
tenure = 5

# Number of iterations.
N = 50

best_solution = X
for iteration in range(1, N + 1):
    print("Iteration {}".format(iteration))
    print("Current solution {}.".format(X))
    current_objective = X.objective
    best_swap = X.best_neighbor_swap(tabu, iteration)
    if best_swap is None: break
    X = X.swap(*best_swap)
    print("Best swap {} with objective {}. Difference to current {}.".format(best_swap, X.objective, X.objective - current_objective))
    # TODO: Implement the update of the best solution and update of the tabu list.
    # ...

    print("Current best solution {} with objective {}.".format(best_solution, best_solution.objective))
    print("Tabu list state:")
    print(tabu)
    print()

print("Best solution {} with objective {}.".format(best_solution, best_solution.objective))

