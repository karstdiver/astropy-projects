"""
    karstdiver:astropy_project

    Generate and plot RGB/JPG files

    The functions in here are called via callbacks on the gui.

    usage:
    import rbg_plotters

"""

from astropy.io import fits

# Set up matplotlib and use a nicer set of plot parameters
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
from astropy.visualization import astropy_mpl_style
plt.style.use(astropy_mpl_style)

import numpy as np
from PIL import Image  # for jpg tools


import numpy as np
from PIL import Image
from astropy.io import fits

##############################################################################
# Set up matplotlib and use a nicer set of plot parameters

import matplotlib.pyplot as plt
from astropy.visualization import astropy_mpl_style
plt.style.use(astropy_mpl_style)


##############################################################################
def get_jpg_image_data(image_pathname):

    """ open JPG file and return image data """

    #image = Image.open('Hs-2009-14-a-web.jpg')
    #image_file="python/astropy/images/M33.jpg"
    try:
        image_data = Image.open(image_pathname)
    except:
        print(f"ERROR: cannot open file: {image_pathname}")
        raise Exception
    else:
        print(f"INFO: Opened image filename: {image_pathname}")

    # print interesting info about files
    xsize, ysize = image_data.size
    print(f"Image size: {ysize} x {xsize}")
    print(f"Image bands: {image_data.getbands()}")

    print('Min:', np.min(image_data))
    print('Max:', np.max(image_data))
    print('Mean:', np.mean(image_data))
    print('Stdev:', np.std(image_data))

    return image_data


##############################################################################
def plot_jpg_cb(image_pathname, save=True):

    """ plot and save JPG file """
    # Load and display the original 3-color jpeg image

    # get image data
    try:
        image_data = get_jpg_image_data(image_pathname)
    except:
        print("ERROR: No image data found")
        return

    # plot image data
    try:
        ax = plt.imshow(image_data)
    except:
        print("ERROR: Unable to plot image (plt.imgshow())")
        return

    #label image plot
    xsize, ysize = image_data.size
    plt.title(f"JPG PLOT \n {image_pathname} \n Image size: {ysize} x {xsize} \n Image bands: {image_data.getbands()}")
    plt.xlabel("Vertical Axis")
    plt.ylabel("Horizontal Axis")
    plt.grid(False)

    plt.show()

    print("INFO: not saving jpg file")


##############################################################################
def split_jpg_cb(image_pathname, save=True):

    """ split JPG file into constituant r,g,b FITS files """

    # get image data
    try:
        image_data = get_jpg_image_data(image_pathname)
    except:
        print("ERROR: No image data found")
        return

# Split the three channels (RGB) and get the data as Numpy arrays. The arrays
# are flattened, so they are 1-dimensional:
    # split image data
    try:
        r, g, b = image_data.split()
    except:
        print("ERROR: Unable to split image (image.split())")
        return

    # numpy image data
    try:
        r_data = np.array(r.getdata()) # data is now an array of length ysize*xsize
        g_data = np.array(g.getdata())
        b_data = np.array(b.getdata())
    except:
        print("ERROR: Unable to numpy image")
        return

    # print interesting info about files
    print("INFO: Got numpy arrays")
    print(f"red data shape:   {r_data.shape}")
    print(f"blue data shape:  {b_data.shape}")
    print(f"green data shape: {g_data.shape}")

    # Reshape the image arrays to be 2-dimensional:
    # reshape numpy image data
    xsize, ysize = image_data.size
    try:
        r_data = r_data.reshape(ysize, xsize) # data is now a matrix (ysize, xsize)
        g_data = g_data.reshape(ysize, xsize)
        b_data = b_data.reshape(ysize, xsize)
    except:
        print("ERROR: Unable to reshape numpy image")
        return

    # print interesting info about data
    print("INFO: resized numpy arrays")
    print(f"red data reshape:   {r_data.shape}")
    print(f"blue data reshape:  {b_data.shape}")
    print(f"green data reshape: {g_data.shape}")



    # Write out the channels as separate FITS images.
    # Add and visualize header info

    red = fits.PrimaryHDU(data=r_data)
    red.header['LATOBS'] = "32:11:56" # add spurious header info
    red.header['LONGOBS'] = "110:56"
    red.header['COMMENT'] = f"red image file: {image_pathname}"
    #red.writeto(f"python/astropy/images/red.fits")

    green = fits.PrimaryHDU(data=g_data)
    green.header['LATOBS'] = "32:11:56"
    green.header['LONGOBS'] = "110:56"
    green.header['COMMENT'] = f"green image file: {image_pathname}"
    #green.writeto(f"python/astropy/images/green.fits")

    blue = fits.PrimaryHDU(data=b_data)
    blue.header['LATOBS'] = "32:11:56"
    blue.header['LONGOBS'] = "110:56"
    blue.header['COMMENT'] = f"blue image file: {image_pathname}"
    #blue.writeto(f"python/astropy/images/blue.fits")

    from pprint import pprint
    pprint(red.header)

##############################################################################
# Delete the files created
#import os
#os.remove('red.fits')
#os.remove('green.fits')
#os.remove('blue.fits')
