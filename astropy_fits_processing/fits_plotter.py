"""
    FITS file plotter
"""

# requires
# pip install astropy
# pip install numpy
# pip install matplotlib
# macOS > 11.0

from astropy.io import fits
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import re
import os
import glob
import tkinter as tk
from tkinter import ttk

# global variables
title = "Plot FITS using Astropy"
cwd = os.getcwd()
image_dir = 'images'


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



def plot_image(image_pathname, save=True):

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
        plt.imshow(image_data, cmap='Reds')
        #plt.imshow(image_data, cmap='gray')
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




def plot_histogram(image_pathname, save=True):

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

    plt.title(f"FLATTENED HISTOGRAM \n {image_pathname}")
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




def gui(title, cwd, image_dir):

    """ User Control Panel """

    win = tk.Tk()
    win.title(title)
    win.geometry('600x200')

    # working directory
    cwd_l_sv = tk.StringVar()
    cwd_l = ttk.Label(win, textvariable=cwd_l_sv)
    cwd_l_sv.set('Working Directory')
    cwd_l.grid(column=0,row=0)

    cwd_e_sv = tk.StringVar()
    cwd_e = tk.Entry(win,width=30, bg='#58F', textvariable=cwd_e_sv)
    cwd_e_sv.set(cwd)
    cwd_e.grid(column=20, row=0)
    cwd_e.focus_set()

    # image directory
    img_l_sv = tk.StringVar()
    img_l = tk.Label(win, textvariable=img_l_sv)
    img_l_sv.set('Image Directory')
    img_l.grid(column=0,row=1)

    img_e_sv = tk.StringVar()
    img_e = tk.Entry(win,width=30, bg='#58F', textvariable=img_e_sv)
    img_e_sv.set(image_dir)
    img_e.grid(column=20, row=1)
    img_e.focus_set()

    # filename combobox selector
    fil_l_sv = tk.StringVar()
    fil_l = tk.Label(win, textvariable=fil_l_sv)
    fil_l_sv.set('Image File')
    fil_l.grid(column=0,row=3)

    # get list of fits files in image directory
    image_dir = cwd_e.get() + '/' + img_e.get() + 'lll'
    files = os.listdir(image_dir)
    # using re + search() to get string with substring
    fits_files = [file for file in files if re.search('.[fF][iI][tT][sS]$', file)]
    fil_e_sv = tk.StringVar()
    fil_cb = ttk.Combobox(win,width=30, textvariable=fil_e_sv)
    fil_cb['values'] = fits_files
    fil_cb.current(0)
    fil_cb.grid(column=20, row=3)

    # generate histogram
    hist_b = tk.Button(win, text='Generate Histogram',
             command=lambda: plot_histogram(cwd_e.get() + '/' +
                                            img_e.get() + '/' +
                                            fil_cb.get()))
    hist_b.grid(column=0, row=4)

    # generate image
    img_b = tk.Button(win, text='Show Image',
             command=lambda: plot_image(cwd_e.get() + '/' +
                                        img_e.get() + '/' +
                                        fil_cb.get()))
    img_b.grid(column=0, row=5)

    # cause program exit
    exit_b = tk.Button(win, text='Exit',
           command=lambda: exit())
    exit_b.grid(column=3, row=7)

    win.mainloop()

# run user control panel
gui(title, cwd, image_dir)

exit()
