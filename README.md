# EvenField - An easy, cost effective alternative to commercial based illumination systems for fluorescence microscopy


Coherent laser sources with Gaussian output profiles have been a preferred choice in many optical microscopy systems due to their high spatial intensity and monochromaticity. While these traits can beneficial in many applications, the high spatial coherence of these lasers results in interference effects as the light propagates through various optics toward the sample plane. These inference patterns superimposed onto the Gaussian laser profile result in an uneven illumination of the sample that get transferred into resulting images. For applications such as single molecule fluorescence imaging, the resulting field inhomogeneity  often clouds the signal that is to be detected. In addition, when these sources are used for imaging large areas that require tiling of multiple fields of view, the circular 2D illumination profile excites a larger field of view than is captured by the camera resulting in additional, unneeded photobleaching of these areas.

A simple deployment of a square multimode fiber between the illumination source and destination corrects this issue; however, the propogation of multiple laser modes through the fiber increases the potential for interference and results in additional laser speckle noise in the output beam. Researchers have developed several solutions to circumvent the laser speckle problem including, fiber vibration, tunable oscillating lenses, and spinning diffusers. 

We test some of these solutions and compare them to a commercial product, the Borealis system by Andor. 

----

Our full evaluation of this system can be found in our preprint : 
{bioRxiv link TBD}
  
---
  
We converged on a simple, cost-effective solution which we call the EvenField Illumination system. 


## So you're interested in building the EvenField system? ...We've got you covered.


This repository contains all of the information you will need to get started on building and employing the Evenfield system in your lab. This system can be used on a traditional, commercial laser launch or can be combined with the open source [Nicolase 3500] diode combiner and fiber launch for a cost effective, total solution for your illumination needs.

![alt text](https://github.com/AllenInstitute/EvenField/blob/master/Hardware/EvenFieldSchematic.png "EvenField System")

#### Hardware:
A complete list of associated hardware can be found [here](/Hardware).

This folder contains everything needed to build the EvenField system, including: 

* A complete [bill of materials] (optics and mounts)
* CAD renderings and .STEP files for the spinning diffuser component
* Details on custom optical fiber from Mitsubishi Cable Industries (MCI).
* *Coming Soon:* Optical alignment guide 

#### Analysis:
The analysis code used for the EvenField publication has also been provided within this repo and may prove useful for evaluating the field flatness of your system. Code was written in Python and can be found [here].

[Nicolase 3500]: https://github.com/PRNicovich/NicoLase 
[bill of materials]: https://github.com/AllenInstitute/EvenField/blob/master/Hardware/EvenField%20Parts%20List.md
[here]: https://github.com/AllenInstitute/EvenField/tree/master/Analysis
