# Brief introduction to histograms using Python
# Taken from
# http://www.python-course.eu/matplotlib_histograms.php


import matplotlib.pyplot as plt
import numpy as np

# generate some Gaussian distributed random numbers

mu = 0.0
sigma = 1.0
size = 10000
gaussian_numbers = np.random.normal(mu, sigma, size)

# make a basic histogram of the data
plt.hist(gaussian_numbers, bins = 100)
plt.title("Gaussian Histogram")

#s = np.random.standard_cauchy(1000000)
#s = s[(s>-25) & (s<25)]  # truncate distribution so it plots well
#plt.title("Cauchy Histogram")
#plt.hist(s, bins=100)

plt.xlabel("Value")
plt.ylabel("Frequency")
plt.show()

# determine the number of bins used to make the histogram
n, bins, patches = plt.hist(gaussian_numbers)
print("Sum over n: ", sum(n))
print("Number of bins: ", len(bins))
#for i in range(len(bins)-1):
#    print(bins[i+1] -bins[i])
#print("patches: ", patches)
#print(patches[1])

del n
del bins
del patches


