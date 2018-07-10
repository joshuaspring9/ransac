#!/usr/bin/env python

import random
from math import sqrt
import scipy.optimize
import numpy as np
import itertools

def compute(input_points, max_distance, max_iterations, ratio):

    total_points = len(input_points)

    # if we don't have at least three input points to test, then the algorithm cannot be run
    if total_points < 3:
        return None

    min_inliers = total_points * ratio

    # remove duplicate points to prevent errors in the linear algebra
    input_points.sort()
    input_points = list(input_points for input_points,_ in itertools.groupby(input_points))

    if max_iterations == None:

        # use a while loop to indefinitely run RANSAC until we have a result
        while True:
            round_results = compute_single_round(input_points, max_distance)

            if round_results == None:
                # something went wrong with the linear algebra, try again
                continue
            elif round_results[6] >= min_inliers:
                # if we have more than the desired inliers, we have a good model so return the parameters of that model
                return round_results[:6]

    else:

        # stop when we hit the max number of iterations
        for _ in range(max_iterations):

            round_results = compute_single_round(input_points, max_distance)

            if round_results == None:
                # something went wrong with the linear algebra, try again
                continue
            elif round_results[6] >= min_inliers:
                # if we have more than the desired inliers, we have a good model so return the parameters of that model
                return round_results[:6]

        # no line fits the model with an acceptable number of inliers and we hit the max number of iterations, terminate
        return None


def compute_single_round(input_points, max_distance):

    # choose three random points to sample
    chosen_points = random.sample(input_points, 3)

    # make sure we actually copy the list
    input_points_filtered = input_points[:]

    # remove the points we are using from this iteration of the loop
    input_points_filtered.remove(chosen_points[0])
    input_points_filtered.remove(chosen_points[1])
    input_points_filtered.remove(chosen_points[2])

    # set up inliers/outliers list and count
    inliers_count = 0
    inliers = []
    outliers = input_points_filtered[:]


    # get lists of x and y coordinates ready
    x = [None] * 3
    y = [None] * 3

    # split each chosen point into x and y values
    for i in range(3):
        x[i] = chosen_points[i][0]
        y[i] = chosen_points[i][1]

    # using the fact that y = ax^2 + bx + c, we will set up a system of equations using the three selected points                  
    equations = np.array([[ x[0] ** 2, x[0], 1], [ x[1] ** 2, x[1], 1], [ x[2] ** 2, x[2], 1]])
    y_values = np.array(y)

    #this gives us a, b, and c using linear algebra to solve the system
    try:
        solution = np.linalg.solve(equations, y_values)
    except:
        # if there are no solutions or an infinite number of solutions, something went wrong
        return None

    # now define the quadratic function
    def f(x):
        return solution[0] * (x ** 2) + solution[1] * x + solution[2]

    # and use the quadratic function equal to zero as a constraint
    def constraint(pt):
        return f(pt[0]) - pt[1]

    # get ready to pass the constraint to scipy
    cons = {'type':'eq', 'fun': constraint}

    # now that we have the curve we can start testing the other points to find inliers
    for point in input_points_filtered:

        # define the distance function we want to optimize
        def distance(pt):
            return sqrt( (pt[0] - point[0]) ** 2 + (pt[1] - point[1]) ** 2)

        # find the point on the curve that is closest to the point we are testing using optimization
        best_point = scipy.optimize.minimize(distance, x0 = point, constraints=cons)['x']

        # get the actual distance
        dist_from_curve = distance(best_point)

        # if the point is close enough to the curve, add it to the inliers
        if dist_from_curve <= max_distance:
            inliers_count += 1
            inliers.append(point)
            outliers.remove(point)

    return [chosen_points, solution[0], solution[1], solution[2], inliers, outliers, inliers_count]


if __name__ == "__main__":

    # if we call this script directly explain that there is a separate demo file
    print("To use this file, simply import it.  To see a demo of how curve fitting RANSAC works, run the quadratic_demo.py file located in this directory.")
