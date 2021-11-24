"""
    karstdiver:astropy_project

    Generate and plot FITS files

    The functions in here are called via callbacks on the gui.

    usage:
    import fits_plotters

"""

from astropy.io import fits

##############################################################################
# Set up matplotlib and use a nicer set of plot parameters
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
from astropy.visualization import astropy_mpl_style
plt.style.use(astropy_mpl_style)

import numpy as np
import re


##############################################################################
def get_fits_image_data(image_pathname, block=0):

    """ open FITS file and return image data from block """
    try:
        hdu_list = fits.open(image_pathname, cache=True)
    except:
        print(f"ERROR: cannot open file: {image_pathname}")
        raise Exception
    else:
        print(f"INFO: Opened image filename: {image_pathname}")

    hdu_list.info()  # display blocks info
    image_data = hdu_list[0].data  # get image data from primary block
    print(f"primary block image type:  {type(image_data)}")
    print(f"primary block image shape: {image_data.shape}")

    hdu_list.close()  # got image data so close ok here

    #image_data = fits.getdata(image_pathname)
    print(f"fits.getdata type:  {type(image_data)}")
    print(f"fits.getdata shape: {type(image_data)}")

    print('Min:', np.min(image_data))
    print('Max:', np.max(image_data))
    print('Mean:', np.mean(image_data))
    print('Stdev:', np.std(image_data))

    return image_data


##############################################################################
def plot_image_cb(image_pathname, save=True):

    """ plot and save image from FITS file """

    plt.title(f"IMAGE PLOT \n {image_pathname}")
    plt.xlabel("Horizontal Axis")
    plt.ylabel("Vertical Axis")
    plt.grid(False)

    try:
        image_data = get_fits_image_data(image_pathname)
    except:
        print("ERROR: No image data found")
        return

    try:
        #plt.imshow(image_data, cmap='gray', norm=LogNorm())
        #plt.imshow(image_data, cmap='Reds')
        plt.imshow(image_data, cmap='gray')
    except:
        print("ERROR: Unable to plot image (plt.imshow()). Is it a 3D RGB fits?")
        return

    plt.colorbar()
    plt.show()

    # save histogram file
    filename = image_pathname.split("/")[-1]
    plot_pathname = re.compile(r"\..*$").sub('-plot.png', image_pathname)
    if save:
        print(f"INFO: saving plot file: {plot_pathname}")
        plt.savefig(plot_pathname)
    else:
        print("INFO: not saving plot file")


##############################################################################
def plot_histogram_cb(image_pathname, save=True):

    """ plot and save histogram from FITS file """

    try:
        image_data = get_fits_image_data(image_pathname)
    except:
        print("ERROR: No image data found")
        return

    try:
        histogram = plt.hist(image_data.flatten(), bins='auto')
    except:
        print("ERROR: Unable to plot histogram (plt.hist())")
        return

    plt.title(f"FLATTENED HISTOGRAM \n {image_pathname} \n Block Image Shape: {image_data.shape} \n Color Min: {np.min(image_data)}  Max: {np.max(image_data)}")
    plt.xlabel("Image Data Values (color)")
    plt.ylabel("Number of Values (intensity)")
    plt.grid(False)

    plt.show()

    # save histogram file
    filename = image_pathname.split("/")[-1]
    hist_pathname = re.compile(r"\..*$").sub('-hist.png', image_pathname)
    if save:
        print(f"INFO: saving historgram file: {hist_pathname}")
        plt.savefig(hist_pathname)
    else:
        print("INFO: not saving historgram file")
