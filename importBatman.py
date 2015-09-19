# -*- coding: utf-8 -*-
import sys

import skimage.io as io
from skimage.color import rgb2grey
from skimage.exposure import equalize_hist
from skimage.filters import gaussian_filter, threshold_otsu
from skimage.transform import downscale_local_mean
from skimage import measure

import numpy as np
import matplotlib.pyplot as plt
import cv2


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
    img = io.imread(name)

    # Grau, bessere Kontraste, blurren von zu viel Details
    img_grey = rgb2grey(img)
    img_grey = downscale_local_mean(img_grey, (2, 2))
    img_grey = equalize_hist(img_grey)
    img_grey = gaussian_filter(img_grey, sigma=1)

    # Schw5arz/Weiß auf basis von Threshold
    thresh = threshold_otsu(img_grey)
    img_bin = img_grey > thresh
    
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')

    faces = face_cascade.detectMultiScale(img, 1, 5)
    img_det = img_bin
    for (x,y,w,h) in faces:
        img_det = cv2.rectangle(img_det, (x,y), (x+w, y+h), (255, 0, 0), 2)

    img_crop = img_bin[y:y+h, x:x+w]

    show_images([img, img_grey, img_bin, img_det, img_crop],
                ['Original', 'smll/Hist/Gauss', 'Bin', 'CV', 'Final'])
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
        




