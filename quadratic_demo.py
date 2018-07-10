#!/usr/bin/env python

# set the folder where the charts will be written to
OUTPUT_DIR = "./Output"
# set the maximum number of rounds for the demo to run
MAX_ROUNDS = 20

import numpy as np
import matplotlib.pyplot as plot
import quadratic
import os

def run(max_rounds):

    # first clear the output directory of any charts from previous runs
    listing = os.listdir(OUTPUT_DIR)
    for item in listing:
        if item.endswith(".png"):
            os.remove(os.path.join(OUTPUT_DIR, item))

    # use numpy to generate random samples.  multiply by 20, subtract 0.5 to get a wide array of numbers between -10 and 10
    # (500,1) means that the array generated is 500 rows x 1 column
    x = 20 * (np.random.random( (500,1) ) - 0.5)
 
    # generate the a, b, and c parameters for the quadratic equation
    # multiply by 2 to get numbers between -2 and 2, but usually closer to 0
    a, b, c = 2 * np.random.normal( size=(3, 1) )

    # generate the quadratic function
    def f(x):
        return a * (x ** 2) + b * x + c
    
    # get the vectorizer ready
    y_func = np.vectorize(f)

    # apply the function to every x value
    y = y_func(x)

    # offset every coordinate by adding a random number from a gaussian distribution
    x_scattered = x + np.random.normal(size=x.shape)
    y_scattered = y + np.random.normal(size=y.shape)


    # now add outliers to the points, using an outlier ratio of 0.4
    x_scattered = np.append(x_scattered, 30 * np.random.random( (int(500 * 0.4), 1) ) - 15, axis=0)

    # determine the concavity of the parabola, and center the distribution at either 50 or -50 depending on concavity
    if a > 0:
        y_scattered = np.append(y_scattered, 50 * np.random.normal( size=(int(500 * 0.4), 1) ) + 50, axis=0)
    else:
        y_scattered = np.append(y_scattered, 50 * np.random.normal( size=(int(500 * 0.4), 1) ) - 50, axis=0)

    # compute the min and max y values after adding the outliers
    min_y_value = min(y_scattered)
    max_y_value = max(y_scattered)

    # produce coordinates compatible with the ransac function
    output = []

    for i in range(len(x_scattered)):
        output.append( (x_scattered[i,0], y_scattered[i,0]) )

    # set the min percent of inliers needed to 60%
    ratio = 0.6
    # set the max distance on each side of the line
    distance = 2.0

    # figure out the minumum number of inliers needed for a model to be considered good
    total_points = len(output)
    min_inliers = total_points * ratio

    # run the demonstration for a maximum of 10 rounds
    for j in range(1, max_rounds + 1):

        results = quadratic.compute_single_round(output, distance)

        # pull out all the values from the return array
        # convert the lists of points to a numpy array because the indexing is easier to work with
        chosen_points = np.array(results[0])
        a = results[1]
        b = results[2]
        c = results[3]
        inliers = np.array(results[4])
        outliers = np.array(results[5])
        num_inliers = results[6]
     
        plot.figure("RANSAC iteration " + str(j), figsize=(15.0, 15.0))
     
        # grid for the plot
        grid = [min(x_scattered) - 10, max(x_scattered) + 10, min_y_value - 20, max_y_value + 20]
        plot.axis(grid)
     
        # put grid on the plot
        plot.grid(b=True, which='major', color='0.75', linestyle='--')
        plot.xticks([i for i in range(min(x_scattered) - 10, max(x_scattered) + 10, 5)])
        plot.yticks([i for i in range(min_y_value - 20, max_y_value + 20, 4000.0/(max_y_value - min_y_value))])
     
        # plot input points
        plot.plot(inliers[:,0], inliers[:,1], marker='o', label='Inlier points', color='#00cc00', linestyle='None', alpha=0.4)
        plot.plot(outliers[:,0], outliers[:,1], marker='o', label='Outlier points', color='#0000cc', linestyle='None', alpha=0.4)
        plot.plot(chosen_points[0:3,0], chosen_points[0:3,1], marker='o', label='Selected points', color='#cc0000', linestyle='None', alpha=0.4) 
        
        # draw the parabola, first sorting the x coordinates in order so each segment connects to the next
        x_scattered = np.sort(x_scattered, axis=0)
        plot.plot(x_scattered, f(x_scattered), label='Quadratic model', color='#cc0000', linewidth=1.0)

        print("On interation number " + str(j))
     
        if num_inliers >= min_inliers:
            plot.title('RANSAC Results')
            plot.legend()
            plot.savefig(OUTPUT_DIR + "/ransac_results.png")
            plot.close()
            print("Algorithm Complete!")
            break
        else:
            plot.title('RANSAC Iteration ' + str(j))
            plot.legend()
            plot.savefig(OUTPUT_DIR + "/ransac_iteration_" + str(j) + ".png")
            plot.close()

if __name__ == "__main__":

    # run the demo with using the max rounds parameter set the top of the file
    run(MAX_ROUNDS)