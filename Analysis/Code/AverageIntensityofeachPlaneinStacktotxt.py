# -*- coding: utf-8 -*-
"""
Created on Tue Oct 23 08:57:21 2018

@author: kylab
"""
import tifffile
from matplotlib import pyplot as plt
import numpy as np
import operator

def cropND(img, bounding):
    '''
    Return center of numpy array.  Returned array will be center (X, Y) elements, where 
    bounding = (X,Y)
    
    Parameters
    ----------
    img = input array
    bounding = tuple defining number of pixels in center of array to return
    
    Returns
    -------
    array size defined by bounding from center of input array
    
    
        https://stackoverflow.com/questions/39382412/crop-center-portion-of-a-numpy-image
    '''
    
    bounding = (len(img), bounding[0], bounding[1])

    start = tuple(map(lambda a, da: a//2-da//2, img.shape, bounding))
    end = tuple(map(operator.add, start, bounding))
    slices = tuple(map(slice, start, end))
    
    return img[slices]


def averageStack(inputData, makePlot = True, cropToSize = ()):

    """Return average intensity in each plane of an image stack

    Parameters
    ----------
    inputData : str
	
		File path string to OME-TIFF file.  Image stack file to be averaged. 
	
	Optional keyword parameters
    ----------
	makePlot : Boolean
	
		If true, display intensity-vs-time trace of data in inputData path
		If true, function returns handle to plot as second argument.
		
	Returns
    -------
    a : numpy array of floats
    b : numpy array of floats with first value deleted due to dark images appearing in first plane for random tests
		
		Array of average intensity in each frame from inputData file.

    """
    
    image_stack = tifffile.imread(inputData) # Read inputData file
    
    if len(cropToSize) > 0:
        # Crop each plane in file to center size given
        print(cropToSize)
        image_stack = cropND(image_stack, cropToSize)
    
    a = np.mean(np.mean(image_stack, axis=2), axis=1)
    b = np.delete(a, 0)

    if makePlot:
        plt.figure(figsize=(10,5))
        plotHand = plt.plot(b)
    
        return b, plotHand
    else:
        return b

def saveSummary(figDestination, outputFig, txtDestination, outputData):

    """Return average intensity in each plane of an image stack

    Parameters
    ----------
    figDestination : str
	
		File path for saving outputFig to disk. 
		
	outputFig : Figure handle
	
		Handle to figure to save. 
	
	txtDestination : str
	
		File path for saving outputData to CSV file.
	
	outputData : array
		
		Array to save to CSV file at destination txtDestination. 
	
	Returns
    -------
    Boolean 
		
		1 if file saved.  0 if encountered error. 

    """


    try:
        plt.figure(outputFig.number)
        plt.savefig(figDestination)
        np.savetxt(txtDestination, outputData, delimiter=',')
        
        return 1
    
    except:
        
        return 0
    
def main():
    
    #inputData = r'insertfilepath'
    inputData = r'..\data\Large Square Fiber Sample\Time Data\1msTimeDataSample.tif'

    figDestination = r'insertfilepath'
    txtDestination = r'insertfilepath'
    
    b, plotHand = averageStack(inputData)
    
    saveCheck = saveSummary(figDestination, plotHand, txtDestination, b)
    
if __name__ == "__main__":
    
    main()
