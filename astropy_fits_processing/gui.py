"""
    karstdiver:astropy_project

    User Control Panel Guide

    Call this function from main.py

    usage:
    import gui

"""

import fits_plotters  # for fits file plots callbacks
import rgb_plotters  # for jpg file plots callbacks

import re
import os
import glob
import tkinter as tk
from tkinter import ttk


##############################################################################
def control_panel_gui(title, cwd, image_dir):

    """ User Control Panel """

    win = tk.Tk()
    win.title(title)
    win.geometry('600x400')  # hor x ver

    # working directory
    row_count = 0
    cwd_l_sv = tk.StringVar()
    cwd_l = ttk.Label(win, textvariable=cwd_l_sv)
    cwd_l_sv.set('Working Directory')
    cwd_l.grid(column=0,row=row_count)

    cwd_e_sv = tk.StringVar()
    cwd_e = tk.Entry(win,width=30, bg='#58F', textvariable=cwd_e_sv)
    cwd_e_sv.set(cwd)
    cwd_e.grid(column=20, row=row_count)
    cwd_e.focus_set()

    # image directory
    row_count = row_count + 1
    img_l_sv = tk.StringVar()
    img_l = tk.Label(win, textvariable=img_l_sv)
    img_l_sv.set('Image Directory')
    img_l.grid(column=0,row=row_count)

    img_e_sv = tk.StringVar()
    img_e = tk.Entry(win,width=30, bg='#58F', textvariable=img_e_sv)
    img_e_sv.set(image_dir)
    img_e.grid(column=20, row=row_count)
    img_e.focus_set()

    # fits filename combobox selector
    row_count = row_count + 1
    fits_l_sv = tk.StringVar()
    fits_l = tk.Label(win, textvariable=fits_l_sv)
    fits_l_sv.set('FITS Image File')
    fits_l.grid(column=0,row=row_count)

    # get list of fits files in image directory
    image_dir = cwd_e.get() + '/' + img_e.get()
    files = os.listdir(image_dir)
    # using re + search() to get string with substring
    fits_files = [file for file in files if re.search('.[fF][iI][tT][sS]$', file)]
    fits_e_sv = tk.StringVar()
    fits_cb = ttk.Combobox(win,width=30, textvariable=fits_e_sv)
    fits_cb['values'] = fits_files
    fits_cb.current(0)
    fits_cb.grid(column=20, row=row_count)

    # generate histogram button
    row_count = row_count + 1
    hist_b = tk.Button(win, text='Generate FITS Histogram',
             command=lambda: fits_plotters.plot_histogram_cb(
                                            image_pathname =
                                            cwd_e.get() + '/' +
                                            img_e.get() + '/' +
                                            fits_cb.get()),
             relief=tk.RAISED,
             font=('Arial', 14))
    hist_b.grid(column=0, row=row_count)

    # generate image button
    row_count = row_count + 1
    img_b = tk.Button(win, text='Show FITS Image',
             command=lambda: fits_plotters.plot_image_cb(
                                        image_pathname =
                                        cwd_e.get() + '/' +
                                        img_e.get() + '/' +
                                        fits_cb.get()),
             relief=tk.RAISED,
             font=('Arial', 14))
    img_b.grid(column=0, row=row_count)

    # jpg filename combobox selector
    row_count = row_count + 1
    jpg_l_sv = tk.StringVar()
    jpg_l = tk.Label(win, textvariable=jpg_l_sv)
    jpg_l_sv.set('JPG Image File')
    jpg_l.grid(column=0,row=row_count)

    # get list of jpg files in image directory
    image_dir = cwd_e.get() + '/' + img_e.get()
    files = os.listdir(image_dir)
    # using re + search() to get string with substring
    jpg_files = [file for file in files if re.search('.[jJ][pP][eE]*[gG]$', file)]
    jpg_e_sv = tk.StringVar()
    jpg_cb = ttk.Combobox(win,width=30, textvariable=jpg_e_sv)
    jpg_cb['values'] = jpg_files
    jpg_cb.current(0)
    jpg_cb.grid(column=20, row=row_count)

    # generate jpg button
    row_count = row_count + 1
    jpg_b = tk.Button(win, text='Show JPG Image',
             command=lambda: rgb_plotters.plot_jpg_cb(
                                            image_pathname =
                                            cwd_e.get() + '/' +
                                            img_e.get() + '/' +
                                            jpg_cb.get()),
             relief=tk.RAISED,
             font=('Arial', 14))
    jpg_b.grid(column=0, row=row_count)

    # split jpg into fits button
    row_count = row_count + 1
    split_b = tk.Button(win, text='Split JPG Image',
             command=lambda: rgb_plotters.split_jpg_cb(
                                            image_pathname =
                                            cwd_e.get() + '/' +
                                            img_e.get() + '/' +
                                            jpg_cb.get()),
             relief=tk.RAISED,
             font=('Arial', 14))
    split_b.grid(column=0, row=row_count)

    # cause program exit
    row_count = row_count + 2
    exit_b = tk.Button(win, text='EXIT',
           command=lambda: exit(),
           relief=tk.RAISED,
           font=('Arial Bold', 14))
    exit_b.grid(column=3, row=row_count)

    win.mainloop()
