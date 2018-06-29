#!/usr/bin/env python

import random
from math import sqrt

def ransac(input_points, max_distance, max_iterations, ratio):

    total_points = len(input_points)
    min_inliers = total_points * ratio

    if max_iterations == None:

        # use a while loop to indefinitely run RANSAC until we have a result
        while True:
            round_results = ransac_single_round(input_points, max_distance)

            # if we have more than the desired inliers, we have a good model so return m and b of that model
            if round_results[5] >= min_inliers:
                return round_results[:5]

    else:

        # stop when we hit the max number of iterations
        for _ in range(max_iterations):

            round_results = ransac_single_round(input_points, max_distance)

            # if we have more than the desired inliers, we have a good model so return m and b of that model
            if round_results[5] >= min_inliers:
                return round_results[:5]

        # no line fits the model with an acceptable number of inliers and we hit the max number of iterations, terminate
        return None


def ransac_single_round(input_points, max_distance):
    
    # choose two random points to sample
    chosen_points = random.sample(input_points, 2)
    # make sure we actually copy the list
    input_points_filtered = input_points[:]
    # remove the points we are using from this iteration of the loop
    input_points_filtered.remove(chosen_points[0])
    input_points_filtered.remove(chosen_points[1])

    inliers_count = 0
    inliers = []
    outliers = input_points_filtered[:]

    # numerator and denominator of the slope
    bottom = chosen_points[1][0] - chosen_points[0][0]
    top = chosen_points[1][1] - chosen_points[0][1]

    if bottom == 0:
        slope = None
    elif top == 0:
        slope = 0
    else:
        slope = top / (1.0 * bottom)
        y_int = chosen_points[0][1] - (chosen_points[0][0] * slope)

    # now that we have a slope and y intercept we can start testing the other points to find inliers
    for point in input_points_filtered:
        # if the line is vertical, use just y component for distance
        if slope == None:
            distance = abs(chosen_points[0][1] - point[1])
        # if the line is horiozontal, use just x component for distance
        elif slope == 0:
            distance = abs(chosen_points[0][0] - point[0])
        # otherwise compute the line from the outlier point to the model line, and then get the point of intersection on the model line
        # then compute the distance and check if it is acceptable
        else:
            slope_normal = -1/slope
            x = (point[1] - y_int - (slope_normal * point[0])) / (slope - slope_normal)
            y = slope_normal * (x - point[0]) + point[1]
            distance = sqrt( (x - point[0]) ** 2 + (y - point[1]) ** 2 )
        if distance <= max_distance:
            inliers_count += 1
            inliers.append(point)
            outliers.remove(point)

    return [chosen_points, slope, y_int, inliers, outliers, inliers_count]


if __name__ == "__main__":

    # if we call this script directly run a demonstration of how the alogrithm works

    import numpy as np
    import matplotlib.pyplot as plot

    # use numpy to generate random samples.  multiply by 20 to get a wide array of number between 0 and 20
    # (500,1) means that the array generated is 500 rows x 1 column
    x = 20 * np.random.random( (500,1) )

 
    # generate line's slope, but choose from a gaussian distribution so it more likely that we have a slope closer to 0
    slope = np.random.normal(scale=0.5)
 
    # multiply every x value by the slope to get the y value (y = mx + b, we assume the y intercept here is 0)
    y = np.dot(x, slope)

    # offset every coordinate by adding a random number from a gaussian distribution
    x_scattered = x + np.random.normal(size=x.shape)
    y_scattered = y + np.random.normal(size=y.shape)


    # produce coordinates compatible with the function
    output = []

    for i in range(len(x_scattered)):
        output.append( (x_scattered[i,0], y_scattered[i,0]) )

    # set the min percent of inliers needed to 60%
    ratio = 0.6
    # set the max distance on each side of the line
    distance = 1.0

    # figure out the minumum number of inliers needed for a model to be considered good
    total_points = len(output)
    min_inliers = total_points * ratio

    # run the demonstration for a maximum of 10 rounds
    for j in range(1,11):

        results = ransac_single_round(output, distance)

        # pull out all the values from the return array
        # convert the lists of points to a numpy array because the indexing is easier to work with
        chosen_points = np.array(results[0])
        slope = results[1]
        y_int = results[2]
        inliers = np.array(results[3])
        outliers = np.array(results[4])
        num_inliers = results[5]
     
        plot.figure("Ransac iteration " + str(j), figsize=(15.0, 15.0))
     
        # grid for the plot
        grid = [min(x) - 10, max(x) + 10, min(y) - 20, max(y) + 20]
        plot.axis(grid)
     
        # put grid on the plot
        plot.grid(b=True, which='major', color='0.75', linestyle='--')
        plot.xticks([i for i in range(min(x) - 10, max(x) + 10, 5)])
        plot.yticks([i for i in range(min(y) - 20, max(y) + 20, 10)])
     
        # plot input points
        plot.plot(inliers[:,0], inliers[:,1], marker='o', label='Inlier points', color='#00cc00', linestyle='None', alpha=0.4)
        plot.plot(outliers[:,0], outliers[:,1], marker='o', label='Outlier points', color='#0000cc', linestyle='None', alpha=0.4)
        plot.plot(chosen_points[0:2,0], chosen_points[0:2,1], marker='o', label='Selected points', color='#cc0000', linestyle='None', alpha=0.4) 
        
        # draw the selected line, using the fact that y = mx + b
        plot.plot(x_scattered, slope * x_scattered + y_int, 'r', label='Line model', color='#0076ff', linewidth=1.0)

        print("On interation number " + str(j))
     
        if num_inliers >= min_inliers:
            plot.title('RANSAC Results')
            plot.legend()
            plot.savefig("ransac_results.png")
            plot.close()
            print("Algorithm Complete!")
            break
        else:
            plot.title('RANSAC Iteration ' + str(j))
            plot.legend()
            plot.savefig("ransac_iteration_" + str(j) + ".png")
            plot.close()
