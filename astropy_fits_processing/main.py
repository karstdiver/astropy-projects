"""
    karstdiver:astropy_project

    Main Program

    usage:
    python main.py

    requires:
    # pip install astropy
    # pip install numpy
    # pip install matplotlib
    # macOS > 11.0

"""

import gui  # for control panel; see callbacks
import os

# global variables
title = "FITS using Astropy"
cwd = os.getcwd()
image_dir = 'images'

##############################################################################
# run user control panel
gui.control_panel_gui(title, cwd, image_dir)


exit()
