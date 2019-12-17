# -*- coding: utf-8 -*-
"""
Created on Fri Nov 09 18:28:38 2018

With AutoCorrV3, extractTimestamps, AverageIntensityofeachPlaneinStacktotxt, 
extract, manipulate, and plot data from files specified in fileList below.  

Change iFact if you want to include interpolation of points for prettier plots. 

@author: rustyn
"""

import AutoCorrV3
import extractTimestamps
from AverageIntensityofeachPlaneinStacktotxt import averageStack
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import ScalarFormatter
from matplotlib.lines import Line2D
from scipy.stats import variation
from mpl_toolkits.axes_grid1.anchored_artists import AnchoredSizeBar
import matplotlib.font_manager as fm
import os
import json
from brewer2mpl import sequential

#%%

def regularizeAndAutocorrelate(fileName, iFact = 1, fcnReturn = 'autocorr', cropStack = ()):

    timestamps = extractTimestamps.getTimestamps(fileName)
    timestamps2 = np.delete(timestamps, 0) #delete first timestamp to match deleted first frame
    regTimestamps = extractTimestamps.regularizeTimestamps(timestamps2, interpFactor = iFact)
      
    regLags = regTimestamps - regTimestamps[0]
    
    data = averageStack(fileName, makePlot = False, cropToSize = cropStack)
    regData = extractTimestamps.regularizeDataToTimestamps(timestamps2, data, interpFact = iFact)

    trace = AutoCorrV3.autocorrTrace(regData)
    
    if fcnReturn == 'autocorr':
        traceList = [regLags, trace]
    elif fcnReturn == 'timeseries':
        traceList = [regTimestamps, regData]
    elif fcnReturn == 'autocorrAndTimeseries':
        traceList = [regLags, trace, regTimestamps, regData]
        
        
    return traceList

#if __name__ == "__main__":
    
#    fileList = [
#               r'C:\Users\kylab\Documents\Illumination Project\DATA\181009\Large Fiber\1ms\SRON_1ms\MMStack_Pos0.ome.tif', 
#                r'C:\Users\kylab\Documents\Illumination Project\DATA\181009\Large Fiber\2ms\SRON_2ms\MMStack_Pos0.ome.tif',
#                r'C:\Users\kylab\Documents\Illumination Project\DATA\181009\Large Fiber\4ms\SRON_4ms\MMStack_Pos0.ome.tif',
#                r'C:\Users\kylab\Documents\Illumination Project\DATA\181009\Large Fiber\8ms\SRON_8ms\MMStack_Pos0.ome.tif',
#                r'C:\Users\kylab\Documents\Illumination Project\DATA\181009\Large Fiber\16ms\SRON_16ms\MMStack_Pos0.ome.tif',
#                r'C:\Users\kylab\Documents\Illumination Project\DATA\181009\Large Fiber\32ms\SRON_32ms\MMStack_Pos0.ome.tif',
#                r'C:\Users\kylab\Documents\Illumination Project\DATA\181009\Large Fiber\64ms\SRON_64ms\MMStack_Pos0.ome.tif']


#    traceList = main(fileList, iFact = 10)
    
#    plt.savefig(r'C:\Users\kylab\Documents\Illumination Project\Testing\AutoCorrLgSqSRON.tif', dpi = 300)
    
#    for t in traceList:
    
#        AutoCorrV3.makeCorrelationPlot(t[0], [], t[1])   
#   plt.gca()
#    plt.semilogx([plt.gca().get_xlim()[0], plt.gca().get_xlim()[1]], [1, 1], c = 'gray', linestyle = ':')

#%% 
if __name__ == "__main__":
    
    outputFolder = r'C:\Users\rustyn\OneDrive - Allen Institute\evenField\Figures'
    
    
    executeList = []
    
    # Optotune
    
    # Circle fiber
    executeList.append({'scrambler' : 'optotune',
                        'fiber' : 'circle',
                        'collimator' : 'objective',
                        'status' : 'ON', 
                        'fileList' : [{'name' : "1 ms",
                                       'file' : r'C:\Users\rustyn\OneDrive - Allen Institute\evenField\181219\Circle\1ms\SRON_1ms\MMStack_Pos0.ome.tif'}, 
                                      {'name' : "2 ms",
                                       'file' : r'C:\Users\rustyn\OneDrive - Allen Institute\evenField\181219\Circle\2ms\SRON_2ms\MMStack_Pos0.ome.tif'}, 
                                      {'name' : "4 ms",
                                       'file' : r'C:\Users\rustyn\OneDrive - Allen Institute\evenField\181219\Circle\4ms\SRON_4ms\MMStack_Pos0.ome.tif'}, 
                                      {'name' : "8 ms",
                                       'file' : r'C:\Users\rustyn\OneDrive - Allen Institute\evenField\181219\Circle\8ms\SRON_8ms\MMStack_Pos0.ome.tif'}, 
                                      {'name' : "16 ms",
                                       'file' : r'C:\Users\rustyn\OneDrive - Allen Institute\evenField\181219\Circle\16ms\SRON_16ms\MMStack_Pos0.ome.tif'}, 
                                      {'name' : "32 ms",
                                       'file' : r'C:\Users\rustyn\OneDrive - Allen Institute\evenField\181219\Circle\32ms\SRON_32ms\MMStack_Pos0.ome.tif'}, 
                                      {'name' : "64 ms",
                                       'file' : r'C:\Users\rustyn\OneDrive - Allen Institute\evenField\181219\Circle\64ms\SRON_64ms\MMStack_Pos0.ome.tif'}]})
    
    # Large square fiber
    executeList.append({'scrambler' : 'optotune',
                        'fiber' : 'largeSquare',
                        'collimator' : 'ThorlabsPAF2P-18A',
                        'status' : 'ON', 
                        'fileList' : [{'name' : "1 ms",
                                       'file' : r'C:\Users\rustyn\OneDrive - Allen Institute\evenField\190121\Large Sq\1ms\SRON_1ms\MMStack_Pos0.ome.tif'}, 
                                      {'name' : "2 ms",
                                       'file' : r'C:\Users\rustyn\OneDrive - Allen Institute\evenField\190121\Large Sq\2ms\SRON_2ms\MMStack_Pos0.ome.tif'}, 
                                      {'name' : "4 ms",
                                       'file' : r'C:\Users\rustyn\OneDrive - Allen Institute\evenField\190121\Large Sq\4ms\SRON_4ms\MMStack_Pos0.ome.tif'}, 
                                      {'name' : "8 ms",
                                       'file' : r'C:\Users\rustyn\OneDrive - Allen Institute\evenField\190121\Large Sq\8ms\SRON_8ms\MMStack_Pos0.ome.tif'}, 
                                      {'name' : "16 ms",
                                       'file' : r'C:\Users\rustyn\OneDrive - Allen Institute\evenField\190121\Large Sq\16ms\SRON_16ms\MMStack_Pos0.ome.tif'}, 
                                      {'name' : "32 ms",
                                       'file' : r'C:\Users\rustyn\OneDrive - Allen Institute\evenField\190121\Large Sq\32ms\SRON_32ms\MMStack_Pos0.ome.tif'}, 
                                      {'name' : "64 ms",
                                       'file' : r'C:\Users\rustyn\OneDrive - Allen Institute\evenField\190121\Large Sq\64ms\SRON_64ms\MMStack_Pos0.ome.tif'}]})
  

    
    # Thorlabs fiber
    executeList.append({'scrambler' : 'optotune',
                        'fiber' : 'smallSquare',
                        'collimator' : 'objective',
                        'status' : 'ON', 
                        'fileList' : [{'name' : "1 ms",
                                       'file' : r'C:\Users\rustyn\OneDrive - Allen Institute\evenField\181219\Small Square\1ms\SRON_1ms\MMStack_Pos0.ome.tif'}, 
                                      {'name' : "2 ms",
                                       'file' : r'C:\Users\rustyn\OneDrive - Allen Institute\evenField\181219\Small Square\2ms\SRON_2ms\MMStack_Pos0.ome.tif'}, 
                                      {'name' : "4 ms",
                                       'file' : r'C:\Users\rustyn\OneDrive - Allen Institute\evenField\181219\Small Square\4ms\SRON_4ms\MMStack_Pos0.ome.tif'}, 
                                      {'name' : "8 ms",
                                       'file' : r'C:\Users\rustyn\OneDrive - Allen Institute\evenField\181219\Small Square\8ms\SRON2_8ms\MMStack_Pos0.ome.tif'}, 
                                      {'name' : "16 ms",
                                       'file' : r'C:\Users\rustyn\OneDrive - Allen Institute\evenField\181219\Small Square\16ms\SRON_16ms\MMStack_Pos0.ome.tif'}, 
                                      {'name' : "32 ms",
                                       'file' : r'C:\Users\rustyn\OneDrive - Allen Institute\evenField\181219\Small Square\32ms\SRON_32ms\MMStack_Pos0.ome.tif'}, 
                                      {'name' : "64 ms",
                                       'file' : r'C:\Users\rustyn\OneDrive - Allen Institute\evenField\181219\Small Square\64ms\SRON_64ms\MMStack_Pos0.ome.tif'}]})
    
    # Borealis
    executeList.append({'scrambler' : 'borealis',
                        'fiber' : 'borealis',
                        'collimator' : 'objective',
                        'status' : 'ON', 
                        'fileList' : [{'name' : "1 ms",
                                       'file' : r'C:\Users\rustyn\OneDrive - Allen Institute\evenField\181102\Borealis\1ms\SRON_1ms\MMStack_Pos0.ome.tif'}, 
                                      {'name' : "2 ms",
                                       'file' : r'C:\Users\rustyn\OneDrive - Allen Institute\evenField\181102\Borealis\2ms\SRON_2ms\MMStack_Pos0.ome.tif'}, 
                                      {'name' : "4 ms",
                                       'file' : r'C:\Users\rustyn\OneDrive - Allen Institute\evenField\181102\Borealis\4ms\SRON_4ms\MMStack_Pos0.ome.tif'}, 
                                      {'name' : "8 ms",
                                       'file' : r'C:\Users\rustyn\OneDrive - Allen Institute\evenField\181102\Borealis\8ms\SRON_8ms\MMStack_Pos0.ome.tif'}, 
                                      {'name' : "16 ms",
                                       'file' : r'C:\Users\rustyn\OneDrive - Allen Institute\evenField\181102\Borealis\16ms\SRON_16ms\MMStack_Pos0.ome.tif'}, 
                                      {'name' : "32 ms",
                                       'file' : r'C:\Users\rustyn\OneDrive - Allen Institute\evenField\181102\Borealis\32ms\SRON_32ms\MMStack_Pos0.ome.tif'}, 
                                      {'name' : "64 ms",
                                       'file' : r'C:\Users\rustyn\OneDrive - Allen Institute\evenField\181102\Borealis\64ms\SRON_64ms\MMStack_Pos0.ome.tif'}]})
    
    
    # Rotating Diffuser
    # large square fiber
    executeList.append({'scrambler' : 'diffuser',
                        'fiber' : 'largeSquare',
                        'collimator' : 'objective',
                        'status' : 'ON', 
                        'fileList' : [{'name' : "1 ms",
                                       'file' : r'C:\Users\rustyn\OneDrive - Allen Institute\evenField\190820\moving_0001msec\cropped_1\cropped_1_MMStack_Pos0.ome.tif'}, 
                                      {'name' : "2 ms",
                                       'file' : r'C:\Users\rustyn\OneDrive - Allen Institute\evenField\190820\moving_0002msec\cropped_1\cropped_1_MMStack_Pos0.ome.tif'}, 
                                      {'name' : "4 ms",
                                       'file' : r'C:\Users\rustyn\OneDrive - Allen Institute\evenField\190820\moving_0004msec\cropped_1\cropped_1_MMStack_Pos0.ome.tif'}, 
                                      {'name' : "8 ms",
                                       'file' : r'C:\Users\rustyn\OneDrive - Allen Institute\evenField\190820\moving_0008msec\cropped_1\cropped_1_MMStack_Pos0.ome.tif'}, 
                                      {'name' : "16 ms",
                                       'file' : r'C:\Users\rustyn\OneDrive - Allen Institute\evenField\190820\moving_0016msec\cropped_1\cropped_1_MMStack_Pos0.ome.tif'}, 
                                      {'name' : "32 ms",
                                       'file' : r'C:\Users\rustyn\OneDrive - Allen Institute\evenField\190820\moving_0032msec\cropped_1\cropped_1_MMStack_Pos0.ome.tif'}, 
                                      {'name' : "64 ms",
                                       'file' : r'C:\Users\rustyn\OneDrive - Allen Institute\evenField\190820\moving_0064msec\cropped_1\cropped_1_MMStack_Pos0.ome.tif'}]})
    
    # Large square fiber, change voltage
    executeList.append({'scrambler' : 'diffuserVoltage',
                        'fiber' : 'largeSquare',
                        'collimator' : 'objective',
                        'status' : 'ON', 
                        'fileList' : [{'name' : "12 V",
                                       'file' : r'C:\Users\rustyn\OneDrive - Allen Institute\evenField\190820\moving_0001msec_12v\cropped_1\cropped_1_MMStack_Pos0.ome.tif'}, 
                                      {'name' : "10 V",
                                       'file' : r'C:\Users\rustyn\OneDrive - Allen Institute\evenField\190820\moving_0001msec_10v\cropped_1\cropped_1_MMStack_Pos0.ome.tif'}, 
                                      {'name' : "8 V",
                                       'file' : r'C:\Users\rustyn\OneDrive - Allen Institute\evenField\190820\moving_0001msec_08v\cropped_1\cropped_1_MMStack_Pos0.ome.tif'}, 
                                      {'name' : "6 V",
                                       'file' : r'C:\Users\rustyn\OneDrive - Allen Institute\evenField\190820\moving_0001msec_06v\cropped_1\cropped_1_MMStack_Pos0.ome.tif'}, 
                                      {'name' : "4 V",
                                       'file' : r'C:\Users\rustyn\OneDrive - Allen Institute\evenField\190820\moving_0001msec_04v\cropped_1\cropped_1_MMStack_Pos0.ome.tif'}, 
                                      {'name' : "2 V",
                                       'file' : r'C:\Users\rustyn\OneDrive - Allen Institute\evenField\190820\moving_0001msec_02v\cropped_1\cropped_1_MMStack_Pos0.ome.tif'}, 
                                      {'name' : "0 V",
                                       'file' : r'C:\Users\rustyn\OneDrive - Allen Institute\evenField\190820\moving_0001msec_00v\cropped_1\cropped_1_MMStack_Pos0.ome.tif'}]})

    # small square fiber
    executeList.append({'scrambler' : 'diffuser',
                        'fiber' : 'smallSquare',
                        'collimator' : 'ThorlabsPAF2P-18A',
                        'status' : 'ON', 
                        'fileList' : [{'name' : "1 ms",
                                       'file' : r'C:\Users\rustyn\OneDrive - Allen Institute\evenField\190829\thorlabsSquare_moving_0001msec\stack_2\stack_2_MMStack_Pos0.ome.tif'}, 
                                      {'name' : "2 ms",
                                       'file' : r'C:\Users\rustyn\OneDrive - Allen Institute\evenField\190829\thorlabsSquare_moving_0002msec\stack_1\stack_1_MMStack_Pos0.ome.tif'}, 
                                      {'name' : "4 ms",
                                       'file' : r'C:\Users\rustyn\OneDrive - Allen Institute\evenField\190829\thorlabsSquare_moving_0004msec\stack_1\stack_1_MMStack_Pos0.ome.tif'}, 
                                      {'name' : "8 ms",
                                       'file' : r'C:\Users\rustyn\OneDrive - Allen Institute\evenField\190829\thorlabsSquare_moving_0008msec\stack_1\stack_1_MMStack_Pos0.ome.tif'}, 
                                      {'name' : "16 ms",
                                       'file' : r'C:\Users\rustyn\OneDrive - Allen Institute\evenField\190829\thorlabsSquare_moving_0016msec\stack_1\stack_1_MMStack_Pos0.ome.tif'}, 
                                      {'name' : "32 ms",
                                       'file' : r'C:\Users\rustyn\OneDrive - Allen Institute\evenField\190829\thorlabsSquare_moving_0032msec\stack_1\stack_1_MMStack_Pos0.ome.tif'}, 
                                      {'name' : "64 ms",
                                       'file' : r'C:\Users\rustyn\OneDrive - Allen Institute\evenField\190829\thorlabsSquare_moving_0064msec\stack_1\stack_1_MMStack_Pos0.ome.tif'}]})
    
    
#    
#%% 
    

    bmap = sequential.GnBu[len(executeList[0]['fileList'])+2]
        
    for eNum, eL in enumerate(executeList):
    
        legend = []
        traceList = []
        for entry in eL['fileList']:
            traceList.append(regularizeAndAutocorrelate(entry['file'], iFact = 10, fcnReturn = 'autocorrAndTimeseries', cropStack = (64, 64)))
            legend.append(entry['name'])
    
    #%%
            
        
        # Deal with coefficient of variation here
        coeffVar = np.zeros(len(traceList))                
        autoCorrFigure = plt.figure()
        
        handList = []
        for i, t in enumerate(traceList):
            
            coeffVar[i] = (variation(t[3]))
        
            handList.append(AutoCorrV3.makeCorrelationPlot(t[0], [], t[1], plotColor = bmap.mpl_colors[i+2])[0])
    
        
        plt.gca().get_yaxis().get_major_formatter().set_useOffset(False)
        plt.semilogx([plt.gca().get_xlim()[0], plt.gca().get_xlim()[1]], [1, 1], c = 'gray', linestyle = ':')
        plt.gca().legend(handList, legend, loc = 1)
    #    plt.figlegend(legend, bbox_to_anchor=(0.5, 0, 0.7, 0.7))
        plt.xlim([1,1000])
        plt.xlabel('Lag time (msec)')
        plt.ylabel('Autocorrelation')

    # Scale autocorr to same y values as optotune range:
#        if eL['scrambler'] == 'optotune':
        if eNum == 0:
            optoLimit = plt.ylim()
#        else:
#            plt.ylim(optoLimit)

#        plt.savefig(r'C:\Users\kylab\OneDrive - Allen Institute\Flat Field Illumination Project\DatatoSendtoLaserBoxManufacturer\AutoCorrLgSq190121.png', bbox_inches='tight', dpi = 300)
        saveName = 'autoCorr_{}_{}_{}.png'.format(eL['fiber'], eL['scrambler'], eL['collimator'])
        
        executeList[eNum]['autocorrFigurePath'] = os.path.join(outputFolder, saveName)
        
        autoCorrFigure.set_size_inches(8.64, 4.78)
        plt.savefig(executeList[eNum]['autocorrFigurePath'], bbox_inches='tight', dpi = 1200)
        
        plt.show()
        
#        if not (eL['scrambler'] == 'optotune'):
        if eNum > 0:
            plt.ylim(optoLimit)
            saveName = 'autoCorr_{}_{}_{}_MatchZoom.png'.format(eL['fiber'], eL['scrambler'], eL['collimator'])
            executeList[eNum]['autocorrMatchZoomFigurePath'] = os.path.join(outputFolder, saveName)
            plt.savefig(executeList[eNum]['autocorrMatchZoomFigurePath'], bbox_inches='tight', dpi = 1200)
        
        
# --------------------------------------
        # Timeseries plots
        
        whichEntries = [0, 4]
        
        # Make stacked intensity vs time plot for these traces
        

        
        traceFigure, axs = plt.subplots(len(whichEntries))
        maxRange = 0
        
        for i, k in enumerate(whichEntries):
            
            
            axs[i].plot(traceList[k][2], traceList[k][3], color = bmap.mpl_colors[k + 2])
            
            rangeHere = axs[i].get_ylim()
            maxRange = np.max([maxRange, np.subtract(rangeHere[1], rangeHere[0])])
            
            axs[i].set_xlim([np.amin(traceList[k][2]), np.amax(traceList[k][2])])
            axs[i].axes.get_xaxis().set_visible(False)
            axs[i].set_frame_on(False)
            axs[i].set_ylabel('Intensity (a.u.)')
            
            fontprops = fm.FontProperties(size=12)
            
            scalebar = AnchoredSizeBar(axs[i].transData,
               0, legend[k], 2, frameon=False)

            axs[i].add_artist(scalebar)
            
            
            
            if i == len(whichEntries)-1:
                scalebar = AnchoredSizeBar(axs[i].transData,
                               500, '500 ms', 4, frameon=False)

                axs[i].add_artist(scalebar)
            
            
            
        
        for ax in axs:
            
            rangeHere = ax.get_ylim()
            medRange = np.mean(rangeHere)
            
            offset = np.mean(maxRange) - medRange
            
            ax.set_ylim(medRange - maxRange/2, medRange + maxRange/2)
            
            xmin, xmax = ax.get_xaxis().get_view_interval()
            ymin, ymax = ax.get_yaxis().get_view_interval()
            ax.add_artist(Line2D((xmin, xmin), (ymin, ymax), color='black', linewidth=1))
        
        traceFigure.set_size_inches(13, 4.78)
        plt.show()
        
        
        saveName = 'timeTrace_{}_{}_{}.png'.format(eL['fiber'], eL['scrambler'], eL['collimator'])
        executeList[eNum]['intensityTraceFigurePath'] = os.path.join(outputFolder, saveName)
        plt.savefig(executeList[eNum]['intensityTraceFigurePath'], bbox_inches='tight', dpi = 1200)
        
        
        # Write results to dict
        executeList[eNum]['whichEntriesPlotted'] = whichEntries
        executeList[eNum]['coefficientOfVariation'] = list(coeffVar)
        
        plt.close('all')
        
    # Dump everything to JSON output file
    with open(os.path.join(outputFolder, 'autocorrOutput.json'), 'w+') as outFile:
        json.dump(executeList, outFile, sort_keys = True, indent = 4)
        
        
        #%%
        
#    fileListList = [fileListOptotune, fileListRotating, fileListRPM]
#    coeffVar = np.zeros([len(fileListOptotune), len(fileListList)])
#    for fL, fListHere in enumerate(fileListList):
#    
#        legend = []
#        intensityVsTime = []
#        
#        
#        
#        for i, entry in enumerate(fListHere):
#            intensityVsTime.append(regularizeAndAutocorrelate(entry['file'], iFact = 10, fcnReturn = 'timeseries', cropStack = (64, 64)))
#            legend.append(entry['name'])
#            coeffVar[i][fL] = (variation(intensityVsTime[i][1]))
#            
#            
#            
#        # Make plot of intensity vs time for selected conditions
#        
#        bmap = sequential.GnBu[len(fileListOptotune)+2]

            
        
    
    
#%% Save coefficient of variation as txt file
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    