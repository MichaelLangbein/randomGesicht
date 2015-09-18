# -*- coding: utf-8 -*-
import sys

import skimage.io as io
from skimage.color import rgb2grey
from skimage.exposure import equalize_hist
from skimage.filters import gaussian_filter
from skimage import measure
from skimage.transform import downscale_local_mean
#from skimage.morphology import skeletonize
#from skimage.morphology import medial_axis

import numpy as np
import matplotlib.pyplot as plt


def show_images(images,titles=None):
    """Display a list of images"""
    n_ims = len(images)
    if titles is None: titles = ['(%d)' % i for i in range(1,n_ims + 1)]
    fig = plt.figure()
    n = 1
    for image,title in zip(images,titles):
        a = fig.add_subplot(1,n_ims,n) # Make subplot
        if image.ndim == 2: # Is image grayscale?
            plt.gray() # Only place in this blog you can't replace 'gray' with 'grey'
        plt.imshow(image)
        a.set_title(title)
        n += 1
    fig.set_size_inches(np.array(fig.get_size_inches()) * n_ims)
    plt.show()

def processImage(pathNname, outpname):
    # Einlesen Original
    name = pathNname
    one = io.imread(name)

    # Grau, bessere Kontraste, blurren von zu viel Details
    one_grey = rgb2grey(one)
    one_grey = downscale_local_mean(one_grey, (2, 2))
    one_grey = equalize_hist(one_grey)
    one_grey = gaussian_filter(one_grey, sigma=1)

    # Schw5arz/Weiß auf basis von Threshold
    one_bin = np.where(one_grey > np.mean(one_grey)- 1.3*np.var(one_grey)**0.5, 1, 0)

    # Ecken entdecken
    #contours = measure.find_contours(one_bin, 0.5)
    #skeleton = skeletonize(one_bin)
    #skeleton = medial_axis(one_bin)

    #show_images([one, one_grey, one_bin],['Original', 'Grau, Hist-eq und Blur', 'Binary, Threshold'])

    io.imsave(outpname, one_bin, 'simpleitk')



if __name__ == '__main__':

    try:
        filename = sys.argv[1]
        pathNname = '/home/michael/codes/python_codes/randomGesicht/bilder/' + filename
        outpname = '/home/michael/codes/python_codes/randomGesicht/bilder/bin_' + filename
        
    except IndexError:
        pathNname = '/home/michael/codes/python_codes/randomGesicht/bilder/one.jpg'
        outpname = '/home/michael/codes/python_codes/randomGesicht/bilder/bin_one.jpg'
        
        
    processImage(pathNname, outpname)
        

