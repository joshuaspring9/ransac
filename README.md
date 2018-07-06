# Ransac
A simple python based implementation of the Ransac algorithm.  This implementation attempts to fit a line to a dataset containing outliers that could throw off a least squares approach.
## Requirements
There are no additional libraries needed to use the ransac.py module.  It should run under both Python 2 and 3.  To run the ransac_demo.py module, you will need the numpy and matplotlib libraries.  You can install them with pip:
```
pip install numpy matplotlib
```
## How to use
Simply import the module, and then call the compute function:
```python
import ransac

result = ransac.linear.compute(input_points, max_distance, max_iterations, ratio)

chosen_points = result[0]
slope = result[1]
y_int = result[2]
inliers = result[3]
outliers = result[4]
```
__Input values:__
* *input_points*: A list of coordinate pairs of the data points to be processed
* *max_distance*: The furthest a point can be from the model line while still being considered an inlier
* *max_iterations*: The number most number of times to run the algorithm before terminating, even if an optimal line has not been found
* *ratio*: The percentage of point that are inliers for a model line to be considered a good fit

__Return values:__
* *chosen_points*: A list of the coordinate pairs of the two points selected to form the model line
* *slope*: The slope of the model line
* *inliers*: A list of coordinate pairs of the inlier points
* *outliers*: A list of coordinate pairs of the outlier points
## Demonstration
To see a visual demonstration of the algorithm's iterative approach, simply run:
```
./linear_demo.py
```
The default will be to terminate after 10 cycles of the algorithm, which can be changed by the *MAX_ITERATIONS* parameter at the top of the file.  After every iteration, a graph including the chosen model line, inliers, and outliers will be produced in the "Output" directory.  This directory can be changed through the *OUTPUT_DIR* parameter at the top of the file.
