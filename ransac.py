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

    # if we call this script directly explain that there is a separate demo file

    print("To use this file, simply import it.  To see a demo of how RANSAC works, run the ransac_demo.py file located in this directory.")
