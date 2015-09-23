import MYSQLdb as mdb
import cv2
import numpy as np
from matplotlib import pyplot as plt

path = "/home/michael/codes/python_codes/randomGesicht/bilder/"

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

def preprocess(imgname):
    imgpath = path + imgname
    
    img = cv2.imread(imgpath)
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_blur = cv2.GaussianBlur(img_gray,(5,5),0)
    img_hist = img_blur #cv2.equalizeHist(img_blur)
    (thrshld, img_thr) = cv2.threshold(img_hist,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)

#    faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
#    faces = faceCascade.detectMultiScale(
#        img_gray,
#        scaleFactor=1.1,
#        minNeighbors=5,
#        minSize=(30, 30),
#        flags = cv2.cv.CV_HAAR_SCALE_IMAGE
#    )

    show_images([img, img_blur, img_hist, img_thr],['Orig', 'Blur', 'Hist', 'Thresh'])
    cv2.imwrite(path + 'prepr_' + imgname, img_thr)
    return img_thr

def importImage(imgname):

    try:
        con = mbd.connect('localhost', 'root', 'rinso86', 'rgdb')
        cur = con.cursor()
    except mdb.Error, e:
        print "Error %d: %s" % (e.args[0], e.args[1])
        
    imgarr = preprocess(imgname)
    
