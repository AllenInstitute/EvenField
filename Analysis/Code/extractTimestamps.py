# -*- coding: utf-8 -*-
"""
Created on Thu Nov 08 22:43:55 2018

@author: rustyn
"""

import xml.etree.ElementTree as ET
import tifffile
import numpy as np
from AverageIntensityofeachPlaneinStacktotxt import averageStack


def getTimestamps(fileName):

    """Return timestamps from OME-TIFF metadata given filename

    Parameters
    ----------
    fileName : str
	
		File path string to OME-TIFF file.  Should be image stack file which includes
		metadata in image description field.  Timestamps are pulled from this XML. 
		
	Returns
    -------
    timeList : List of floats
		
		List of timestamps of each frame in a timelapse extracted from OME-TIFF file provided.

    """

    timeList = []
    
    with tifffile.TiffFile(fileName) as tif:
        if tif.is_ome:
            try:
                md = tif.pages[0].description
            except:
                md = tif[0].image_description
            
    xmltree = ET.fromstring(md)
    ns={'n':'http://www.openmicroscopy.org/Schemas/OME/2015-01'}
    imgMD =  xmltree.findall('n:Image', namespaces = ns) # Finding first instance of this tag regardless?

    

    for m, imgSibs in enumerate(imgMD):
        pixMD = imgSibs.find('n:Pixels', namespaces = ns)
        
        planesMD = pixMD.findall('n:Plane', namespaces = ns)
        
        for k in range(len(planesMD)):
            tHere = float(planesMD[k].attrib['DeltaT'])
            
            timeList.append(tHere)
            
    timeList = np.array(timeList)
    timeList =timeList - timeList[0]
    
    return timeList

def regularizeTimestamps(timeList, interpFactor = 1):

    """Interpolate timestamps to regular linear spacing.

    Parameters
    ----------
    timeList : list of floats
	
		List of timestamps.  Format as returned by getTimestamps().  
		
	interpFactor : int
	
		Multiplier for number of points to interpolate over.  Returned number of points will be 
		product of interpFactor and length of timeList (rounded). 
		
	Returns
    -------
    numpy array of floats
		
		Array of interpolated timestamps.  Will be linear spacing of points between first and last 
		points in input timeList.  Number of points in returned array will be product of  length of 
		input list and the interpFactor (rounded). 

    """
    
    return np.linspace(np.amin(timeList), np.amax(timeList), int(len(timeList)*interpFactor))

def regularizeDataToTimestamps(timeList, data, interpFact = 1):

    """Interpolate data to linearly interpolated points 

    Parameters
    ----------
    timeList : list of floats
	
		List of timestamps.  Format as returned by getTimestamps(). 

	data : array
	
		Data points taken at timeList points in data series.  
		
	interpFact : int
	
		Multiplier for number of points to interpolate over.  Returned number of points will be 
		product of interpFactor and length of timeList (rounded). 
		
	Returns
    -------
    regData : numpy array of floats
		
		List of interpolated data points at interpolated timepoints.  Timepoints will be linear spacing of 
		points between first and last points in input timeList, as returned by regTimestamps.  
		Number of points in returned list will be product of length of input list and the interpFact (rounded). 

    """
    
    regTimestamps = regularizeTimestamps(timeList, interpFactor = interpFact)
    # interpolate data points to this regularized timescale
    
    regData = np.interp(regTimestamps, timeList, data) 
    
    return regData
    

############
    
def main():
    
    import matplotlib.pyplot as plt

	# List of file paths to data stacks
    fileList = [r'C:\Users\kylab\Documents\Illumination Project\DATA\181009\Large Fiber\1ms\SRON_1ms\MMStack_Pos0.ome.tif', 
                r'C:\Users\kylab\Documents\Illumination Project\DATA\181009\Large Fiber\2ms\SRON_2ms\MMStack_Pos0.ome.tif',
                r'C:\Users\kylab\Documents\Illumination Project\DATA\181009\Large Fiber\4ms\SRON_4ms\MMStack_Pos0.ome.tif',
                r'C:\Users\kylab\Documents\Illumination Project\DATA\181009\Large Fiber\8ms\SRON_8ms\MMStack_Pos0.ome.tif',
                r'C:\Users\kylab\Documents\Illumination Project\DATA\181009\Large Fiber\16ms\SRON_16ms\MMStack_Pos0.ome.tif',
                r'C:\Users\kylab\Documents\Illumination Project\DATA\181009\Large Fiber\32ms\SRON_32ms\MMStack_Pos0.ome.tif',
                r'C:\Users\kylab\Documents\Illumination Project\DATA\181009\Large Fiber\64ms\SRON_64ms\MMStack_Pos0.ome.tif']
    
	# Loop over file list
    for k in range(len(fileList)):
        
        timestamps = getTimestamps(fileList[k])  # Pull timestamps from data
        timestamps2 = np.delete(timestamps, 0)   #delete first timestamp ???
        regTimestamps = regularizeTimestamps(timestamps2)  # Regularize these timestamps
        
        data = averageStack(fileList[k], makePlot = False) # Pull data over defined region in image stack
        regData = regularizeDataToTimestamps(timestamps2, data) # Regularize data to linearly-spaced timestamps
        
        
        plt.plot(timestamps2, data, 'c', markersize = 2)  # Plot raw data and timestamps
        plt.plot(regTimestamps, regData, 'r', markersize = 2) # Plot regularized data and timestamps.  Should reasonably match raw.
#        plt.plot(np.array([np.amin(timestamps), np.amax(timestamps)]), 
#                 np.array([np.amin(regTimestamps), np.amax(regTimestamps)]), 
#                 c = 'gray', linestyle = '--')
        plt.show()
        

if __name__ == "__main__":
    
    main()

    