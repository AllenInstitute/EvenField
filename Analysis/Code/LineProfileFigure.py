# -*- coding: utf-8 -*-
"""
Created on Tue Oct 16 15:04:45 2018

@author: kylab
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Sep 19 13:31:46 2018
This code calculates the center of mass of an image using weighted intensity and plots a horizontal line profile
using the center of mass coordinates and subtracts the darkfield image from data image.
@author: kylab
"""


from matplotlib import pyplot as plt
import numpy as np
import skimage
import tifffile
from scipy.optimize import minimize
import json
import os
from matplotlib.path import Path
from scipy.stats import variation


def tophat(x, base_level, hat_level, hat_mid, hat_width):
    return np.where((hat_mid-hat_width/2. < x) & (x < hat_mid+hat_width/2.), hat_level, base_level)

def tanHTopHat(x, bkgd, amp, center, width, b):
        stepDown = bkgd + (amp/2) - (amp/2)*np.tanh((x - center-(width/2))/b)
        stepUp = bkgd + (amp/2) + (amp/2)*np.tanh((x - center+(width/2))/b)
        
        whichFcn = x > center 
        s = stepUp
        s[whichFcn] = stepDown[whichFcn]
        
        return s

def objective(params, x, y):
    return np.sum(np.abs(tophat(x, *params) - y))

def objectiveTanH(params, x, y):
    return np.sum(np.abs(tanHTopHat(x, *params) - y))

def rgb(r, g, b, darken = 1., lighten=1.):
    return [darken*float(r)/(lighten*255), darken*float(g)/(lighten*255), darken*float(b)/(lighten*255)]

def pointsToMask(imgShape, pointsList):
    x, y = np.meshgrid(np.arange(imgShape[0]), np.arange(imgShape[1]))
    x, y = x.flatten(), y.flatten()
    
    points = np.vstack((x,y)).T
    
    path = Path(pointsList)

    grid = path.contains_points(points)
    grid = grid.reshape((imgShape[1], imgShape[0])).T
    
    return grid

def calcAxLimits(boundSquareHigh, border = 0.1):
    xDiff = 0.1*(boundSquareHigh[2] - boundSquareHigh[0])
    yDiff = 0.1*(boundSquareHigh[3] - boundSquareHigh[1])
    
    xRange = np.array([boundSquareHigh[0] - xDiff, boundSquareHigh[2] + xDiff])
    yRange = np.array([boundSquareHigh[1] - yDiff, boundSquareHigh[3] + yDiff])
    
    return xRange, yRange

#%%
#inputImage = r'..\data\Large Square Fiber Sample\Fiber Image Data\1msLargeFiber.tif'
#darkfieldImage = r'..\data\Large Square Fiber Sample\Fiber Image Data\Darkfield.tif'

outputFolder = r'C:\Users\rustyn\OneDrive - Allen Institute\evenField\Figures'

writeToDisk = False

executeList = []

# -------------------------
# Optotune
# -------------------------
# -------- 
# ON
# --------
# large square
executeList.append({'baseFolder' : r'C:\Users\rustyn\OneDrive - Allen Institute\evenField', 
                    'inputImage' : r'\190121\Large Sq\16ms\180121_SRON_16ms\MMStack_Pos0.ome.tif', 
                    'darkfieldImage' : r'\190121\Large Sq\darkfield\darkfield.tif',
                    'scrambler' : 'optotune',
                    'fiber' : 'largeSquare',
                    'collimator' : 'ThorlabsPAF2P-18A',
                    'status' : 'ON'})

# small square

executeList.append({'baseFolder' : r'C:\Users\rustyn\OneDrive - Allen Institute\evenField', 
                    'inputImage' : r'\181219\Small Square\16ms\181219_SRON_16ms\MMStack_Pos0.ome.tif', 
                    'darkfieldImage' : r'\181219\Small Square\AvgDarkfield.tif',
                    'scrambler' : 'optotune',
                    'fiber' : 'smallSquare',
                    'collimator' : 'objective',
                    'status' : 'ON'})    

# circle 
    
executeList.append({'baseFolder' : r'C:\Users\rustyn\OneDrive - Allen Institute\evenField', 
                    'inputImage' : r'\181219\Circle\16ms\181219_SRON_16ms\MMStack_Pos0.ome.tif',
                    'darkfieldImage' : r'\181219\Circle\AvgDarkfield.tif',
                    'scrambler' : 'optotune',
                    'fiber' : 'circle',
                    'collimator' : 'objective',
                    'status' : 'ON'})  
    
# Borealis
    
executeList.append({'baseFolder' : r'C:\Users\rustyn\OneDrive - Allen Institute\evenField', 
                    'inputImage' : r'\181102\Borealis\16ms\181102_SRON_16ms\MMStack_Pos0.ome.tif', 
                    'darkfieldImage' : r'\181102\Borealis\Darkfield\AVG_MMStack_Pos0.ome.tif',
                    'scrambler' : 'borealis',
                    'fiber' : 'borealis',
                    'collimator' : 'objective',
                    'status' : 'ON'})  

# -------- 
# OFF
# --------
# large square
    
executeList.append({'baseFolder' : r'C:\Users\rustyn\OneDrive - Allen Institute\evenField', 
                    'inputImage' : r'\190121\Large Sq\16ms\180121_SROFF_16ms\MMStack_Pos0.ome.tif', 
                    'darkfieldImage' : r'\190121\Large Sq\darkfield\darkfield.tif',
                    'scrambler' : 'optotune',
                    'fiber' : 'largeSquare',
                    'collimator' : 'ThorlabsPAF2P-18A',
                    'status' : 'OFF'})  


# small square
    
executeList.append({'baseFolder' : r'C:\Users\rustyn\OneDrive - Allen Institute\evenField', 
                    'inputImage' : r'\181219\Small Square\16ms\181219_SROFF_16ms\MMStack_Pos0.ome.tif', 
                    'darkfieldImage' : r'\181219\Small Square\AvgDarkfield.tif',
                    'scrambler' : 'optotune',
                    'fiber' : 'smallSquare',
                    'collimator' : 'objective',
                    'status' : 'OFF'})  

# circle 
    
executeList.append({'baseFolder' : r'C:\Users\rustyn\OneDrive - Allen Institute\evenField', 
                    'inputImage' : r'\181219\Circle\16ms\181219_SROFF_16ms\MMStack_Pos0.ome.tif', 
                    'darkfieldImage' : r'\190121\Large Sq\darkfield\darkfield.tif',
                    'scrambler' : 'optotune',
                    'fiber' : 'circle',
                    'collimator' : 'objective',
                    'status' : 'OFF'})  
    
# Borealis
    
executeList.append({'baseFolder' : r'C:\Users\rustyn\OneDrive - Allen Institute\evenField', 
                    'inputImage' : r'\181102\Borealis\16ms\181102_SROFF_16ms\MMStack_Pos0.ome.tif', 
                    'darkfieldImage' : r'\190121\Large Sq\darkfield\darkfield.tif',
                    'scrambler' : 'borealis',
                    'fiber' : 'borealis',
                    'collimator' : 'objective',
                    'status' : 'OFF'}) 

# -------------------------
# Diffuser
# -------------------------  
# -------- 
# ON
# --------  
# large square

    # Objective collimator
executeList.append({'baseFolder' : r'C:\Users\rustyn\OneDrive - Allen Institute\evenField', 
                'inputImage' : r'\190820\fullFrame_moving_0125msec\MMStack_Pos0.ome.tif', 
                'darkfieldImage' : r'\190820\noLaser_0125msec\MMStack_Pos0.ome.tif',
                'scrambler' : 'diffuser',
                'fiber' : 'largeSquare',
                'collimator' : 'objective',
                'status' : 'ON'}) 

# Thorlabs collimator
executeList.append({'baseFolder' : r'C:\Users\rustyn\OneDrive - Allen Institute\evenField', 
                'inputImage' : r'\190820\thorlabs_moving_0125msec\MMStack_Pos0.ome.tif', 
                'darkfieldImage' : r'\190820\noLaser_0125msec\MMStack_Pos0.ome.tif',
                'scrambler' : 'diffuser',
                'fiber' : 'largeSquare',
                'collimator' : 'ThorlabsPAF2P-18A',
                'status' : 'ON'}) 
    
# Thorlabs collimator + thorlabs square fiber
executeList.append({'baseFolder' : r'C:\Users\rustyn\OneDrive - Allen Institute\evenField', 
                'inputImage' : r'\190829\fullFrame_thorlabsSquare_moving_0125ms\MMStack_Pos0.ome.tif', 
                'darkfieldImage' : r'\190829\noLaser_0001ms\MMStack_Pos0.ome.tif',
                'scrambler' : 'diffuser',
                'fiber' : 'smallSquare',
                'collimator' : 'ThorlabsPAF2P-18A',
                'status' : 'ON'}) 

# -------- 
# OFF
# --------
# large square
    
# Objective collimator
executeList.append({'baseFolder' : r'C:\Users\rustyn\OneDrive - Allen Institute\evenField', 
                'inputImage' : r'\190820\fullFrame_static_0125msec\MMStack_Pos0.ome.tif', 
                'darkfieldImage' : r'\190820\noLaser_0125msec\MMStack_Pos0.ome.tif',
                'scrambler' : 'diffuser',
                'fiber' : 'largeSquare',
                'collimator' : 'objective',
                'status' : 'OFF'}) 

# Thorlabs collimator    
executeList.append({'baseFolder' : r'C:\Users\rustyn\OneDrive - Allen Institute\evenField', 
                'inputImage' : r'\190820\thorlabs_static_0125msec\MMStack_Pos0.ome.tif', 
                'darkfieldImage' : r'\190820\noLaser_0125msec\MMStack_Pos0.ome.tif',
                'scrambler' : 'diffuser',
                'fiber' : 'largeSquare',
                'collimator' : 'ThorlabsPAF2P-18A',
                'status' : 'OFF'}) 
    
# Thorlabs collimator + thorlabs square fiber
executeList.append({'baseFolder' : r'C:\Users\rustyn\OneDrive - Allen Institute\evenField', 
                'inputImage' : r'\190829\fullFrame_thorlabsSquare_static_0125ms\MMStack_Pos0.ome.tif', 
                'darkfieldImage' : r'\190829\noLaser_0001ms\MMStack_Pos0.ome.tif',
                'scrambler' : 'diffuser',
                'fiber' : 'smallSquare',
                'collimator' : 'ThorlabsPAF2P-18A',
                'status' : 'OFF'}) 



#%% Load in image

    
    
#i = 0 
#exHere = executeList[i]
# START LOOP HERE
    
for i, exHere in enumerate(executeList):
    baseFolder = exHere['baseFolder']
        
    with tifffile.TiffFile(exHere['baseFolder'] + exHere['inputImage']) as tif:
        image_stack = tif.asarray().astype('float')
        
    with tifffile.TiffFile(exHere['baseFolder'] + exHere['darkfieldImage']) as tif:
        darkfield = tif.asarray().astype('float')
    
    image_stack2 = image_stack - darkfield
    
    #%%  Threshold image and do some calcs
    
    thresh = skimage.filters.threshold_otsu(image_stack2) # Automatically find threshold between object and background
    regProps = skimage.measure.regionprops(skimage.measure.label(image_stack2 > thresh), image_stack2) # Measure properties of this binarized object
    regPropsOutside = skimage.measure.regionprops(skimage.measure.label(image_stack2 < thresh), image_stack2) # Measure properties of this binarized object
    area = [x.filled_area for x in regProps] # Pull area of all detected objects above threshold
    bigCentroid = [x.centroid for x in regProps if x.filled_area == np.amax(area)] # Find centroid of largest object
    bigReg = [x for x in regProps if x.filled_area == np.amax(area)]
    
    
    # Pull intensity lines along centroid coordinates
    xLine = image_stack2[:, int(bigCentroid[0][1])]
    yLine = image_stack2[int(bigCentroid[0][0]), :]
    
    
    xDom = range(image_stack2.shape[0])
    yDom = range(image_stack2.shape[1])
    
    # X fit
    xGuesses = [ [np.sum(image_stack2[image_stack2 < thresh])/np.sum(image_stack2 < thresh), # base intensity
                 bigReg[0].mean_intensity, # peak intensity
                 bigCentroid[0][0], # center
                 bigReg[0].bbox[2] - bigReg[0].bbox[0], # width
                 10] ] # b parameter
    
    
    
    for guess in xGuesses:
        resX = minimize(objectiveTanH, guess, args=(xDom, xLine), method='Nelder-Mead')
        print(resX.x)
        
    # Y fit  
    yGuesses = [ [np.sum(image_stack2[image_stack2 < thresh])/np.sum(image_stack2 < thresh), 
                 bigReg[0].mean_intensity, 
                 bigCentroid[0][1], 
                 bigReg[0].bbox[3] - bigReg[0].bbox[1], 
                 10] ]
    
    
    
    for guess in yGuesses:
        resY = minimize(objectiveTanH, guess, args=(yDom, yLine), method='Nelder-Mead')
        print(resY.x)
    
    
        
    #%% Calculate bounding boxes of 'on' and 'off' regoins
    
    xFit = tanHTopHat(xDom, *(resX.x))
    yFit = tanHTopHat(yDom, *(resY.x))
    
    xStartStop = [np.where(np.abs(xFit - (resX.x[0])) > 0.01*(resX.x[1]) )[0][[0,-1]], np.where(np.abs(xFit - (resX.x[1] + resX.x[0])) < 0.01*(resX.x[1] + resX.x[0]) )[0][[0,-1]]] #[(inner values for signal > baseline)]
    yStartStop = [np.where(np.abs(yFit - (resY.x[0])) > 0.01*(resX.x[1]) )[0][[0,-1]], np.where(np.abs(yFit - (resY.x[1] + resY.x[0])) < 0.01*(resY.x[1] + resY.x[0]) )[0][[0,-1]]]
    
    boundSquareLow = np.array([yStartStop[0][0], xStartStop[0][0],  
                                 yStartStop[0][1], xStartStop[0][1]])
    
    boundSquareHigh= np.array([yStartStop[1][0], xStartStop[1][0],  
                                 yStartStop[1][1], xStartStop[1][1]])
    
    #boundBinary = np.zeros_like(image_stack2)
    #boundBinary[boundSquare90Pct[0]:boundSquare90Pct[1], boundSquare90Pct[2]:boundSquare90Pct[3]] = 1
    #inOutofBoundBox = np.sum(boundBinary*(image_stack2 - np.amin(image_stack2)))/np.sum(np.sum(image_stack2 - np.amin(image_stack2)))
    
    #boundBinary10 = np.zeros_like(image_stack2)
    #boundBinary10[boundSquare10Pct[0]:boundSquare10Pct[1], boundSquare10Pct[2]:boundSquare10Pct[3]] = 1
    
    #binSizeComparison = np.sum(boundBinary)/np.sum(boundBinary10)
    
    #########################
    #Calculate Variance of the region of xLine that is above upper threshold
    #########################
    ##print("xLineArrayValues = " +str(xLineArrayValues))
    #Variance = np.var(xLineArrayValues)
    #print("Variance = " +str(Variance))
    #StdDev = np.std(xLineArrayValues)
    #print("Standard Deviation = " +str(StdDev))
    #mean90Pct = np.mean(xLineArrayValues)
    #print("Mean of 90% Region = " +str(mean90Pct))
    #PctDev = np.divide(StdDev, mean90Pct)
    #print("% Deviation of 90% Region from Mean = " +str(PctDev))
    #print("Coefficient of variation in 99% bound box = " + 'xxx')
    #print("LengthXLineArray = " +str(LengthxLineArray))
    ##slope, intercept, r_value, p_value, std_err = stats.linregress(xLineArray, xLineArrayValues)
    ##print("r-squared: %f" % r_value**2)
    ##plt.plot(xLineArray[0], xLineArrayValues, 'o', label='original data')
    ##plt.plot(xLineArray[0], intercept + slope*xLineArray[0], 'r', label='fitted line')
    ##plt.legend()
    ##plt.show()
    
    #%%
    # Make plots
        
    boundBoxOut = rgb(241, 196, 15)
    boundBoxIn = rgb(243, 156, 18)
    
    xTraceColor= rgb(52, 152, 219)
    yTraceColor = rgb(231, 76, 60)
    
    xTraceFitColor = rgb(41, 128, 185, darken=0.6)
    yTraceFitColor = rgb(192, 57, 43,  darken=0.6)
    
    xAxisLim, yAxisLim = calcAxLimits(boundSquareLow, border = 0.2)
    
    
    fig, (ax, ax1, ax2) = plt.subplots(ncols=3, figsize = (18, 4.78))
    ##fig.suptitle('Figure 1', fontsize=16, fontweight='bold')
    
    
    ax = plt.subplot(131)
    ax.imshow(image_stack2, origin='upper', cmap = 'gray')
    #ax.plot([bigCentroid[0][1], bigCentroid[0][1]], [0, (image_stack2.shape[0]-1)], 'r-') #"ro-" is fmt (format string), r is red, o is circle, - is line
    ax.plot([0, (image_stack2.shape[1]-1)], [bigCentroid[0][0], bigCentroid[0][0]], '-', color = yTraceColor)
    ax.plot([bigCentroid[0][1], bigCentroid[0][1]], [0, (image_stack2.shape[0]-1)], '-', color = xTraceColor)
    
    
    box10,=ax.plot(boundSquareHigh[[0, 0, 2, 2, 0]], boundSquareHigh[[1, 3, 3, 1, 1]], c = boundBoxOut, linestyle=':', linewidth=2)
    #box10.set_label("10% Bound Box")
    box90,=ax.plot(boundSquareLow[[0, 0, 2, 2, 0]], boundSquareLow[[1, 3, 3, 1, 1]], c = boundBoxIn, linestyle=':' , linewidth=2)
    #box90.set_label("99% Bound Box")
    
    #ax.set_xlim([0, image_stack2.shape[1]])
    #ax.set_ylim([0, image_stack2.shape[0]])
    ax.set_xlabel('X Position (pixels)')
    ax.set_ylabel('Y Position (pixels)')
    ax.set_xlim(xAxisLim)
    ax.set_ylim(yAxisLim)
    
    ax.legend()
    
    
    # Plot some results
    
    
    ax1 = plt.subplot(132)
    ax1.plot(xDom,xLine, color = xTraceColor)
    ax1.plot(xDom, tanHTopHat(xDom, *(resX.x)), color =xTraceFitColor)
    vertRange = ax1.get_ylim()
    left = plt.plot([xStartStop[0][0], xStartStop[0][0]], vertRange,  c= boundBoxIn, linestyle='--')
    right = plt.plot([xStartStop[0][1], xStartStop[0][1]], vertRange,  c= boundBoxIn, linestyle='--')
    left = plt.plot([xStartStop[1][0], xStartStop[1][0]], vertRange,  c= boundBoxOut, linestyle='--')
    right = plt.plot([xStartStop[1][1], xStartStop[1][1]], vertRange,  c= boundBoxOut, linestyle='--')
    ax1.set_xlim([0, image_stack2.shape[0]])
    ax1.set_xlabel('Y Position (pixels)')
    ax1.set_ylabel('Intensity (a.u.)')
    ax1.set_ylim(vertRange)
    ax1.set_xlim(yAxisLim)
    
    
    ax2 = plt.subplot(133)
    
    ax2.plot(yDom,yLine, color = yTraceColor)
    ax2.plot(yDom, tanHTopHat(yDom, *(resY.x)), color = yTraceFitColor)
    vertRange = ax2.get_ylim()
    left = plt.plot([yStartStop[0][0], yStartStop[0][0]], vertRange,  c= boundBoxIn, linestyle='--')
    right = plt.plot([yStartStop[0][1], yStartStop[0][1]], vertRange,  c= boundBoxIn, linestyle='--')
    left = plt.plot([yStartStop[1][0], yStartStop[1][0]], vertRange,  c= boundBoxOut, linestyle='--')
    right = plt.plot([yStartStop[1][1], yStartStop[1][1]], vertRange,  c= boundBoxOut, linestyle='--')
    ax2.set_xlim([0, image_stack2.shape[1] ])
    ax2.set_xlabel('Y Position (pixels)')
    ax2.set_ylabel('Intensity (a.u.)')
    ax2.set_ylim(vertRange)
    ax2.set_xlim(xAxisLim)
    plt.show()
    
    # Save figure to disk
    figSavePath = 'Lineprofile_{}_{}_{}_{}.png'.format(exHere['fiber'], exHere['scrambler'], exHere['status'], exHere['collimator'])
    if writeToDisk:
        plt.savefig(os.path.join(outputFolder, figSavePath), bbox_inches='tight', dpi = 1200)
    
    #%%
    ################################
    # Area of Bounding Boxes
    ###############################
    #
    #print("yStartStop10_90 = " + str(yStartStop10_90))
    Area10 = np.subtract(yStartStop[0][1], yStartStop[0][0]) * np.subtract(xStartStop[0][1], xStartStop[0][0])
    Area90 = np.subtract(yStartStop[1][1], yStartStop[1][0]) * np.subtract(xStartStop[1][1], xStartStop[1][0])
    DiffArea10_90= (np.subtract(Area10, Area90))
    DiffAreaPct = np.multiply(100, np.divide(DiffArea10_90.astype('float'), Area10.astype('float')))
    
    outerMask = pointsToMask(image_stack2.shape, [(xStartStop[0][0], yStartStop[0][0]), 
                                                  (xStartStop[0][1], yStartStop[0][0]),
                                                  (xStartStop[0][1], yStartStop[0][1]),
                                                  (xStartStop[0][0], yStartStop[0][1]),
                                                  (xStartStop[0][0], yStartStop[0][0])])
        
    innerMask = pointsToMask(image_stack2.shape, [(xStartStop[1][0], yStartStop[1][0]), 
                                                  (xStartStop[1][1], yStartStop[1][0]),
                                                  (xStartStop[1][1], yStartStop[1][1]),
                                                  (xStartStop[1][0], yStartStop[1][1]),
                                                  (xStartStop[1][0], yStartStop[1][0])])

    # Coefficient of variation within inner square region
    coeffVarTotal = variation(image_stack2[innerMask])
    executeList[i]['CoefficientOfVariation'] = coeffVarTotal
    
    coeffVarX = variation(xLine[xStartStop[1][0]:xStartStop[1][1]])
    coeffVarY = variation(yLine[yStartStop[1][0]:yStartStop[1][1]])
    executeList[i]['CoefficientOfVariation_XYTraces'] = [coeffVarX, coeffVarY]
    
    # Area above threshold outside 'inside' region
    threshBin = np.bitwise_xor((image_stack2 > thresh), innerMask)
    executeList[i]['ThreshAreaOutsideInner'] = np.sum(threshBin)
    
    
    # Area below threshold inside 'outside' region
    threshBin = np.bitwise_xor((image_stack2 < thresh), np.invert(outerMask))
    executeList[i]['ThreshAreaInsideOuter'] = np.sum(threshBin)
    
    # Append to JSON list
    executeList[i]['AreaOuter'] = int(Area10)
    executeList[i]['AreaInner'] = int(Area90)
    executeList[i]['DiffArea'] = int(DiffArea10_90)
    executeList[i]['DiffAreaPct'] = float(DiffAreaPct)
    
    executeList[i]['ImageThreshold'] = thresh
    executeList[i]['ImageSize'] = image_stack2.shape
    
    # intensity in inner vs outer mask area
    executeList[i]['IntensityInAndOutofInnerMask'] = [np.sum(image_stack2[innerMask]), np.sum(image_stack2[np.invert(innerMask)])]
    executeList[i]['IntensityInAndOutofOuterMask'] = [np.sum(image_stack2[outerMask]), np.sum(image_stack2[np.invert(outerMask)])]
    
    executeList[i]['XCurveFit'] = resX.x.tolist()
    executeList[i]['YCurveFit'] = resY.x.tolist()
    
    executeList[i]['figSavePath'] = os.path.join(outputFolder, figSavePath)

    plt.close('all')

# END LOOP HERE

# Output results to JSON file
if writeToDisk:
    with (open(os.path.join(outputFolder, 'lineProfileResults.json'), 'w+')) as outFile:
        json.dump(executeList, outFile, sort_keys = True, indent = 4)


#print("Area5 = " +str(Area10))
#print("Area99 = " +str(Area90))
#print("Difference Between Area5 and Area99 = " +str(DiffArea10_90))
#print("Percent Area Unoccupied by Area 99 =" +str(DiffAreaPct))
##################################
#
#ax2 = plt.subplot(132)
#ax2.plot(yLine, c="cyan")
#ax2.set_xlim([100,2400])
#bot = plt.plot([0, image_stack2.shape[1]], [y10_90[0], y10_90[0]],  c= "0.9", linestyle=':', linewidth = 2)
#top = plt.plot([0, image_stack2.shape[1]], [y10_90[1], y10_90[1]],  c= "0.7", linestyle=':', linewidth = 2)
#NinetyLeft = plt.plot([yStartStop10_90[1][0], yStartStop10_90[1][0]], [x10_90[1], x10_90[0]],  c= "0.4", linestyle='--')
#NinetyRight = plt.plot([yStartStop10_90[1][1], yStartStop10_90[1][1]], [x10_90[1], x10_90[0]],  c= "0.4", linestyle='--')
#TenLeft = plt.plot([yStartStop10_90[0][0], yStartStop10_90[0][0]], [x10_90[1], x10_90[0]],  c= "0.6", linestyle='--')
#TenRight = plt.plot([yStartStop10_90[0][1], yStartStop10_90[0][1]], [x10_90[1], x10_90[0]],  c= "0.6", linestyle='--')
#ax2.set_xlim([0, image_stack2.shape[1]])
#ax2.set_xlabel('X Position (pixels)')
#ax2.set_ylabel('Intensity (a.u.)')

#asp = np.diff(ax1.get_xlim())[0] / np.diff(ax1.get_ylim())[0]
#asp /= np.abs(np.diff(ax.get_xlim())[0] / np.diff(ax.get_ylim())[0])
#asp1 = np.diff(ax2.get_xlim())[0] / np.diff(ax2.get_ylim())[0]
#asp1 /= np.abs(np.diff(ax.get_xlim())[0] / np.diff(ax.get_ylim())[0])
#
##ax1.set_aspect(asp)
#ax2.set_aspect(asp1)
#
#plt.tight_layout()
#
#plt.savefig(baseFolder + r'\DatatoSendtoLaserBoxManufacturer\Large Square Analysis 190121 Camera Stroke.png', dpi = 300) #either line 123 or line 124 must be commented out. plt.show clears figure, comment out to save
#plt.show()



#%%

#centroid = scipy.ndimage.measurements.center_of_mass(image_stack2)
##this center of mass calculation requires image to be grayscale 
#
#plt.show(centroid)
#print(centroid)
#maxint = scipy.ndimage.maximum(image_stack2)
#print(maxint)
#
#x0 , y0 = 0, 2447
#x1 , y1 = centroid
#I = maxint
#num = 2448
#x, y = np.linspace(x0, y0, num), np.linspace(x1, x1, num)
##Returns num evenly spaced samples, calculated over the interval -> make the line to profile
#"""x, y = np.linspace(first_x_coordinate, second_x_coordinate, number of samples to generate between),
#np.linspace(first_y_coordinate, second_y_coordinate, number of samples to generate between)"""
#
###plt.plot(x, y)
#
#zi = scipy.ndimage.map_coordinates(image_stack2, np.vstack((y,x)))
## Extract the intensity profile along created line, reversed x,y because imshow flips x and y axes
#
#fig = plt.figure(1, figsize=(13, 3))
###fig.suptitle('Figure 1', fontsize=16, fontweight='bold')
#a = plt.subplot(131)
#a.imshow(image_stack2)
#a.plot([x0,y0], [x1,x1], 'r-') #"ro-" is fmt (format string), r is red, o is circle, - is line
#a.axis('image')
#b = plt.subplot(132)
#b.plot(zi, c="red")
#b.set_xlim([100,2400])
#bot = plt.plot(np.linspace(x0, y0, 10), np.linspace(0.07*I, 0.07*I, 10), c= "gray", linestyle=':')
#top = plt.plot(np.linspace(x0, y0, 10), np.linspace(0.8*I, 0.8*I, 10), c= "gray", linestyle=':')
#
#plt.tight_layout()
#
#plt.show()
#fig.savefig(r'C:\Users\kylab\OneDrive - Allen Institute\Flat Field Illumination Project\181009\Large Fiber\64ms\181009_SROFF_64ms\DarkfieldCorrectedLineProfile_SROff_64ms.tif')
