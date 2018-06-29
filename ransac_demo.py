#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plot
import ransac

def run(max_rounds):

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
    for j in range(1, max_rounds):

        results = ransac.ransac_single_round(output, distance)

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

if __name__ == "__main__":

    # run the demo with a maximum of 10 rounds
    run(10)