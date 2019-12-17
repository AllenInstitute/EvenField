# -*- coding: utf-8 -*-
"""
Created on Mon Nov  5 12:23:40 2018

@author: kylab
"""


# -*- coding: utf-8 -*-
"""
Created on Thu Sep 20 16:55:23 2018

@author: rustyn
edited by kylab to save figure 
"""

import numpy as np
import matplotlib.pyplot as plt

def autocorrTrace(trace, normalizeIntensity = True):

    """Generate autocorrelation of provided trace

    Parameters
    ----------
    trace : numpy array
	
		1D array from which autocorrelation will be generated. 
	
	Optional keyword parameters
    ----------
	normalizeIntensity : Boolean
	
		If true, normalize output to (mean(trace)^2 * len(trace))
		If false, normalize output to len(trace) only 
		
	Returns
    -------
    numpy array of floats (real + imaginary)
		
		Autocorrelation of provided trace.

    """
    
    tracemean = np.mean(trace)
   
   
    if normalizeIntensity:
       
#       return np.fft.ifft(np.fft.fft(trace - tracemean)*np.conj(np.fft.fft(trace - tracemean)))/(np.square(len(trace))) + 1
        return np.fft.ifft(np.fft.fft(trace)*np.conj(np.fft.fft(trace)))/(np.square(tracemean)*(len(trace))) 
   
    else:
   
       return np.fft.ifft(np.fft.fft(trace)*np.conj(np.fft.fft(trace)))/((len(trace)))

def findHalfTimeValue(corr):

    """Find halftime point of provided trace. Half-time defined as first timepoint beyond 1/2 of max 
	amplitude of the provided trace.

    Parameters
    ----------
    corr : numpy array
	
		1D array from which halftime point will be calculated
	
		
	Returns
    -------
    firstPast : numpy array of integer
		
		First element of corr vector with amplitude below 1/2 of max value.

    """
    
    maxCorr = np.amax(corr)
    halfMax = (maxCorr - 1)/2 + 1
    
    firstPast = np.argmax(corr < halfMax)
    
    return firstPast

def makeCorrelationPlot(frames, halfTime, corr, plotColor):

    """Plot autocorrelation results

    Parameters
    ----------
    frames : numpy array
	
		X values for plot.  
		
	halftime : int or float
	
		Half-time point to add to plot.  Provide as empty list ( [] ) to omit.
	
	corr : numpy array
	
		Y values for plot
	
		
	Returns
    -------
    Semilog plot of corr as a function of frames, with halftime annotated if provided. 
		

    """
    
    #plt.clf()
    
    #plt.semilogx([np.amin(frames), np.amax(frames)], [1, 1], color = '0.8')    
    #plt.semilogx([np.amin(frames), frames[halfTime]], [corr[halfTime], corr[halfTime]], linestyle = '--', color = '0.5')
    #plt.semilogx([frames[halfTime], frames[halfTime]], [0.95*np.amin(corr), corr[halfTime]], linestyle = '--', color = '0.5')    
    if len(plotColor) == 0:
        hand = plt.semilogx(frames, corr)
        
    else:
#        print(plotColor)
        hand = plt.semilogx(frames, corr, color = plotColor)
    
    plt.xlabel('Lag time (msec)')
    plt.ylabel('Correlation')
    
    #plt.xlim((np.amin(frames), np.amax(frames)))
    #plt.ylim(0, plt.gca().get_ylim())
    #plt.ylim((0.95*np.amin(corr), plt.gca().get_ylim()[1]))
    ##plt.ylim([-1000,6000])
    
    #plt.savefig(r'C:\Users\kylab\OneDrive - Allen Institute\Flat Field Illumination Project\181009\Large Fiber\1ms\SROFF_1ms\AutoCorrTest.tif')

    
    return hand

def main(frameTime):    
    data = {
        "1 ms exposure": np.loadtxt(r'..\data\Large Square Fiber Sample\Time Data\AverageIntensity1msSample.txt'), 
        "2 ms exposure": np.loadtxt(r'..\data\Large Square Fiber Sample\Time Data\AverageIntensity2msSample.txt'),
        #"4 ms exposure": np.loadtxt(r'C:\Users\kylab\OneDrive - Allen Institute\Flat Field Illumination Project\181009\Large Fiber\4ms\SRON_4ms\averageintensity.txt'),
        #"8 ms exposure": np.loadtxt(r'C:\Users\kylab\OneDrive - Allen Institute\Flat Field Illumination Project\181009\Large Fiber\8ms\SRON_8ms\averageintensity.txt'),
        #"16 ms exposure": np.loadtxt(r'C:\Users\kylab\OneDrive - Allen Institute\Flat Field Illumination Project\181009\Large Fiber\16ms\SRON_16ms\averageintensitydeletedfirstframe.txt'),
        #"32 ms exposure": np.loadtxt(r'C:\Users\kylab\OneDrive - Allen Institute\Flat Field Illumination Project\181009\Large Fiber\32ms\SRON_32ms\averageintensitydeletedfirstframe.txt'),
        #"64 ms exposure": np.loadtxt(r'C:\Users\kylab\OneDrive - Allen Institute\Flat Field Illumination Project\181009\Large Fiber\64ms\SRON_64ms\averageintensitydeletedfirstframe.txt')
    }

    legend = []
    for key, value in data.items():
        autocorr = autocorrTrace(value)
    
        maxPoints = int((len(autocorr))*0.9)
        frames = np.linspace(1*frameTime, maxPoints*frameTime, maxPoints)
    
        halfTime = findHalfTimeValue(autocorr[:maxPoints:])
    
        makeCorrelationPlot(frames, halfTime, autocorr[:maxPoints:])
        legend.append(key)
    
    plt.legend(legend)
    #plt.ylim(-800, 1500)
    #plt.savefig(r'insertsavepath', dpi = 300)
    plt.show()
    
    return frames[halfTime]
    
if __name__ == "__main__":
    
    frameTime = 1e-3 # frame interval in seconds   
    
    t_oneHalf = main(frameTime)
