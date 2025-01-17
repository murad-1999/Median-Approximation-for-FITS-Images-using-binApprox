# Import the running_stats function
from helper import running_stats
# Write your median_bins_fits and median_approx_fits here:
import time, numpy as np
from astropy.io import fits
from helper import running_stats


def median_bins_for_fits(filenames, B):
  # Calculate the mean and standard dev
  mean, std = running_stats(filenames)
    
  dimensions = mean.shape # Dimension of the FITS arrays
    
  # Initialise bins
  left_bin = np.zeros(dimensions)
  bins = np.zeros((dimensions[0], dimensions[1], B))
  bin_width = 2 * std / B 

  # Loop over all FITS files
  for filename in filenames:
      HDUlist = fits.open(filename)
      data = HDUlist[0].data

      # Loop over every point in the 2D array
      for i in range(dimensions[0]):
        for j in range(dimensions[1]):
          value = data[i, j]
          mean_ = mean[i, j]
          std_ = std[i, j]

          if value < mean_ - std_:
            left_bin[i, j] += 1
                
          elif value >= mean_ - std_ and value < mean_ + std_:
            bin = int((value - (mean_ - std_))/bin_width[i, j])
            bins[i, j, bin] += 1

  return mean, std, left_bin, bins


def median_approx_for_fits(filenames, B):
  mean, std, left_bin, bins = median_bins_fits(filenames, B)
    
  dimensions = mean.shape # dimensions of the FITS arrays
    
  # Position of the middle element over all files
  N = len(filenames)
  mid = (N + 1)/2
	
  bin_width = 2*std / B
  # Calculate the approximated median for each array element
  median = np.zeros(dimensions)   
  for i in range(dimensions[0]):
    for j in range(dimensions[1]):    
      count = left_bin[i, j]
      for b, binCount in enumerate(bins[i, j]):
        count += binCount
        if count >= mid:
          # Stop when the cumulative count exceeds the midpoint
          break
      median[i, j] = mean[i, j] - std[i, j] + bin_width[i, j]*(b + 0.5)
      
  return median
    
    
mean, std, left_bin, bins = median_bins_for_fits(['img0.fits', 'img1.fits', 'img2.fits'], 5)
median = median_approx_for_fits(['img0.fits', 'img1.fits', 'img2.fits'], 5)
