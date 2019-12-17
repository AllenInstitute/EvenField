# -*- coding: utf-8 -*-
"""
Created on Mon Aug 26 16:58:57 2019

@author: rustyn
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.transforms as tForms
from scipy.optimize import fsolve
import tifffile

def makeGaussian(size, sigma = 3, center=None, amp = 1):
    """ Make a square gaussian kernel.

    size is the length of a side of the square
    fwhm is full-width-half-maximum, which
    can be thought of as an effective radius.
    https://stackoverflow.com/questions/7687679/how-to-generate-2d-gaussian-with-python
    """

    x = np.arange(0, size, 1, float)
    y = x[:,np.newaxis]

    if center is None:
        x0 = y0 = size // 2
    else:
        x0 = center[0]
        y0 = center[1]

    return (1./np.sqrt(2*np.pi))*amp*np.exp(- ((x-x0)**2 + (y-y0)**2) / (2*(sigma**2)))

def makeSquareTopHat(size, width = 3, center = None, amp = 1):
    x = np.arange(0, size, 1, float)
    y = x[:,np.newaxis]
    
    if center is None:
        
        x0 = y0 = size // 2
    
    else:
        x0 = center[0]
        y0 = center[1]
        
    topHatX = np.tile((x > (x0 - width/2)) & (x < (x0 + width/2)), [size, 1])
    topHatY = np.tile((y > (y0 - width/2)) & (y < (y0 + width/2)), [1, size])
    
    return (topHatX & topHatY).astype(float)

def matchIntensities(fcnA, fcnB):
    
    fun = lambda x: np.sum(fcnA*(fcnB > 0)*x - fcnB)
    
    res = fsolve(fun, [1])
    return res

def create_circular_mask(h, w, center=None, radius=None):
    #https://stackoverflow.com/questions/44865023/circular-masking-an-image-in-python-using-numpy-arrays

    if center is None: # use the middle of the image
        center = [int(w/2), int(h/2)]
    if radius is None: # use the smallest distance between the center and image walls
        radius = min(center[0], center[1], w-center[0], h-center[1])

    Y, X = np.ogrid[:h, :w]
    dist_from_center = np.sqrt((X - center[0])**2 + (Y-center[1])**2)

    mask = dist_from_center <= radius
    return mask.astype('float')

def addRectangleToPlot(ax, imgSize, edgeSize):
    
    rect = np.array([[imgSize[0]/2 - edgeSize[0]/2, imgSize[1]/2 - edgeSize[1]/2],
                     [imgSize[0]/2 + edgeSize[0]/2, imgSize[1]/2 - edgeSize[1]/2],
                     [imgSize[0]/2 + edgeSize[0]/2, imgSize[1]/2 + edgeSize[1]/2],
                     [imgSize[0]/2 - edgeSize[0]/2, imgSize[1]/2 + edgeSize[1]/2],
                     [imgSize[0]/2 - edgeSize[0]/2, imgSize[1]/2 - edgeSize[1]/2]])
    ax.plot(rect[:,0], rect[:,1], 'w--')
    
    return

def rgb(r, g, b, darken = 1., lighten=1.):
    return [darken*float(r)/(lighten*255), darken*float(g)/(lighten*255), darken*float(b)/(lighten*255)]

#%%
# Panel 1 of evenfield paper
# Square vs circumscribed circle vs inscribed circle vs Gaussian

imgSize = [1024, 1024]
chipSize = [512, 512]
ampPeak = 1

# Gaussian is easiest to figure out first
# FWHM = 2 sqrt(2 ln 2) * sigma
# sigma = FWHM / (2  * sqrt(2 * ln(2)))
sigmaFromFwhm = chipSize[0]/(2*np.sqrt(2*np.log(2)))

topHat = makeSquareTopHat(imgSize[0], chipSize[0])

gData =  makeGaussian(imgSize[0], sigma = sigmaFromFwhm, center = [512, 512], amp = 1)

matchPeak = matchIntensities(gData, topHat)

gDataFWHM =  makeGaussian(imgSize[0], sigma = sigmaFromFwhm, center = [512, 512], amp = matchPeak[0])


# 1/e^2 width Gaussian matching top hat width
# 2*sigma = 1/e^2 distance
sigmaFrom1overeSqd = chipSize[0]/4

gData =  makeGaussian(imgSize[0], sigma = sigmaFrom1overeSqd, center = [512, 512], amp = 1)

matchPeak = matchIntensities(gData, topHat)

gData1overeSqd =  makeGaussian(imgSize[0], sigma = sigmaFrom1overeSqd, center = [512, 512], amp = matchPeak[0])

# Circumscribed circle
matchPeakCircum = 1
circleTopHatCircum = matchPeakCircum*create_circular_mask(imgSize[0], imgSize[1], radius=0.5*chipSize[0]*np.sqrt(2))
    
# Inscribed circle
matchPeakInsc = (4./np.pi)
circleTopHatInsc = matchPeakInsc*create_circular_mask(imgSize[0], imgSize[1], radius=0.5*chipSize[0])

#%% Plot everything
imgColormap = 'gist_gray'

fig, ax = plt.subplots(nrows = 2, ncols = 3, sharex = 'all')

plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=0.1, hspace=0.1)

ax[0][0].imshow(topHat, cmap = imgColormap, vmin = 0, vmax = np.amax(gData1overeSqd))
addRectangleToPlot(ax[0][0], imgSize, chipSize)
ax[0][0].plot([0, imgSize[1]], chipSize, color = rgb(155, 89, 182))
ax[0][0].axis('off')

ax[0][1].imshow(gDataFWHM, cmap = imgColormap, vmin = 0, vmax = np.amax(gData1overeSqd))
addRectangleToPlot(ax[0][1], imgSize, chipSize)
ax[0][1].plot([0, imgSize[1]], chipSize, color = rgb(26, 188, 156))
ax[0][1].axis('off')

ax[0][2].imshow(gData1overeSqd, cmap = imgColormap, vmin = 0, vmax = np.amax(gData1overeSqd))
addRectangleToPlot(ax[0][2], imgSize, chipSize)
ax[0][2].plot([0, imgSize[1]], chipSize, color = rgb(52, 152, 219))
ax[0][2].axis('off')

ax[1][0].imshow(circleTopHatCircum, cmap = imgColormap, vmin = 0, vmax = np.amax(gData1overeSqd))
addRectangleToPlot(ax[1][0], imgSize, chipSize)
ax[1][0].plot([0, imgSize[1]], chipSize, color = rgb(241, 196, 15))
ax[1][0].axis('off')

ax[1][1].imshow(circleTopHatInsc, cmap = imgColormap, vmin = 0, vmax = np.amax(gData1overeSqd))
addRectangleToPlot(ax[1][1], imgSize, chipSize)
ax[1][1].plot([0, imgSize[1]], chipSize, color = rgb(231, 76, 60))
ax[1][1].axis('off')


ax[1][2].plot(gDataFWHM[:,512], color = rgb(26, 188, 156))
ax[1][2].plot(gData1overeSqd[:,512], color = rgb(52, 152, 219))
ax[1][2].plot(circleTopHatCircum[:,512], color = rgb(241, 196, 15))
ax[1][2].plot(circleTopHatInsc[:,512], color = rgb(231, 76, 60))
ax[1][2].plot(topHat[:,512], color = rgb(155, 89, 182))
ax[1][2].set_ylabel('Intensity (a.u.)')
ax[1][2].set_xlabel('Position (pixel)')
ax[1][2].set_xlim([0, imgSize[1]])
plt.setp( ax[1][2].get_xticklabels(), visible=False)
ax[1][2].xaxis.set_ticks_position('none') 

axPost = ax[1][2].get_position().get_points()
ax[1][2].set_position(tForms.Bbox([[0.70, axPost[0][1]], [0.89, axPost[1][1]]]))

plt.show()
fig.set_size_inches([ 10.31,   6.59])
plt.savefig(r'C:\Users\rustyn\OneDrive - Allen Institute\evenField\Figures\fiberOptions_2Rows.png', bbox_inches='tight', dpi = 1200)

#%% Plot everything, but in a different order
imgColormap = 'gist_gray'

fig, ax = plt.subplots(nrows = 3, ncols = 2, sharex = 'all')

plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=0.1, hspace=0.1)

ax[2][0].imshow(topHat, cmap = imgColormap, vmin = 0, vmax = np.amax(gData1overeSqd))
addRectangleToPlot(ax[2][0], imgSize, chipSize)
ax[2][0].plot([0, imgSize[1]], chipSize, color = rgb(155, 89, 182))
ax[2][0].axis('off')

ax[0][0].imshow(gDataFWHM, cmap = imgColormap, vmin = 0, vmax = np.amax(gData1overeSqd))
addRectangleToPlot(ax[0][0], imgSize, chipSize)
ax[0][0].plot([0, imgSize[1]], chipSize, color = rgb(26, 188, 156))
ax[0][0].axis('off')

ax[0][1].imshow(gData1overeSqd, cmap = imgColormap, vmin = 0, vmax = np.amax(gData1overeSqd))
addRectangleToPlot(ax[0][1], imgSize, chipSize)
ax[0][1].plot([0, imgSize[1]], chipSize, color = rgb(52, 152, 219))
ax[0][1].axis('off')

ax[1][0].imshow(circleTopHatCircum, cmap = imgColormap, vmin = 0, vmax = np.amax(gData1overeSqd))
addRectangleToPlot(ax[1][0], imgSize, chipSize)
ax[1][0].plot([0, imgSize[1]], chipSize, color = rgb(241, 196, 15))
ax[1][0].axis('off')

ax[1][1].imshow(circleTopHatInsc, cmap = imgColormap, vmin = 0, vmax = np.amax(gData1overeSqd))
addRectangleToPlot(ax[1][1], imgSize, chipSize)
ax[1][1].plot([0, imgSize[1]], chipSize, color = rgb(231, 76, 60))
ax[1][1].axis('off')


ax[2][1].plot(gDataFWHM[:,512], color = rgb(26, 188, 156))
ax[2][1].plot(gData1overeSqd[:,512], color = rgb(52, 152, 219))
ax[2][1].plot(circleTopHatCircum[:,512], color = rgb(241, 196, 15))
ax[2][1].plot(circleTopHatInsc[:,512], color = rgb(231, 76, 60))
ax[2][1].plot(topHat[:,512], color = rgb(155, 89, 182))
ax[2][1].set_ylabel('Intensity (a.u.)')
ax[2][1].set_xlabel('Position (pixel)')
ax[2][1].set_xlim([0, imgSize[1]])
plt.setp( ax[2][1].get_xticklabels(), visible=False)
ax[2][1].xaxis.set_ticks_position('none') 

axPost = ax[2][1].get_position().get_points()
ax[2][1].set_position(tForms.Bbox([[0.59, axPost[0][1]], [0.89, axPost[1][1]]]))

plt.show()
fig.set_size_inches([ 6.59,   10.31])
plt.savefig(r'C:\Users\rustyn\OneDrive - Allen Institute\evenField\Figures\fiberOptions_3Rows.png', bbox_inches='tight', dpi = 1200)

#%% Figure 1b
# Speckle is bad
# Speckle vs non-speckled image
# Use big square fiber - go ahead and give away the punch line

flatImg = r'C:\Users\rustyn\OneDrive - Allen Institute\evenField\Figures\circleFiberImg_specOFF.tif'
with tifffile.TiffFile(flatImg) as tif:
    img = tif.asarray()

fig, ax = plt.subplots(nrows = 1, ncols = 2, sharex = 'all')
ax[0].imshow(img, cmap = imgColormap)
ax[0].plot([0, img.shape[0]], [img.shape[1]/2, img.shape[1]/2], color = rgb(231, 76, 60))
ax[0].axis('off')

ax[1].plot(img[:,img.shape[1]/2], color = rgb(231, 76, 60))
ax[1].set_ylabel('Intensity (a.u.)')
ax[1].set_xlabel('Position (pixel)')
ax[1].set_xlim([0, img.shape[0]])
plt.setp( ax[1].get_xticklabels(), visible=False)
ax[1].xaxis.set_ticks_position('none')

axPost = ax[1].get_position().get_points()
ax[1].set_position(tForms.Bbox([[0.61, 0.25], [0.89, 0.75]]))

plt.show()
fig.set_size_inches([ 6.88,  4.78])
plt.savefig(r'C:\Users\rustyn\OneDrive - Allen Institute\evenField\Figures\circFiberShowSpeckle.png', bbox_inches='tight', dpi = 1200)









