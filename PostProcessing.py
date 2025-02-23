##############################################################
#   This module contains post-processing routines for after the 
#   GPU iterations.
#	
#   Siddharth Maddali
#   Argonne National Laboratory
#   2018
##############################################################

import numpy as np
try:
    from pyfftw.interfaces.numpy_fft import fftshift, fftn, ifftn
except: 
    from numpy.fft import fftshift, fftn, ifftn

def centerObject( img, sup ):
    
    imgC = img.copy()
    supC = sup.copy()
    span = np.where( supC > 0.5 )
    for n in list( range( len( span ) ) ):
        if 1+span[n].max()-span[n].min()==supC.shape[n]: 
                # i.e. obj split across periodic boundary for some reason
            imgC = np.roll( imgC, imgC.shape[n]//2, axis=n )
            supC = np.roll( supC, supC.shape[n]//2, axis=n )

    y, x, z = np.meshgrid( 
        np.arange( supC.shape[0] ), 
        np.arange( supC.shape[1] ), 
        np.arange( supC.shape[2] ) 
    )
    sm = supC.sum()
    xc = ( x*supC ).sum() // sm
    yc = ( y*supC ).sum() // sm
    zc = ( z*supC ).sum() // sm
    c = [ int( xc ), int( yc ), int( zc ) ]

    for n in list( range( 3 ) ):
        imgC = np.roll( imgC, imgC.shape[n]//2 - c[n], axis=n )
        supC = np.roll( supC, supC.shape[n]//2 - c[n], axis=n )

    return removePhaseRamps( imgC ), supC

def removePhaseRamps( img ): #... by centering the Bragg peak in the array
    fimg = fftshift( fftn( fftshift( img ) ) )
    intens = np.absolute( fimg )**2
    maxHere = np.where( intens==intens.max() )
    for n in [ 0, 1, 2 ]:
        fimg = np.roll( fimg, fimg.shape[n]//2-maxHere[n], axis=n )
    imgout = fftshift( ifftn( fftshift( fimg ) ) )
    return imgout


