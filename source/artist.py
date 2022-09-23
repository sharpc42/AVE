#  ****************************************************
#
#  Created by Christopher Sharp in 2021
#  Copyright (c) 2021, Christopher Sharp (MIT license)
#
#  Uses Athena++ by Princeton University without changes
#  Copyright (c) 2016, PrincetonUniversity (BSD 3-clause)
#
#  Uses imagio, Matplotlib, moviepy, and NumPy as modules without changes
#  Copyright (c) 2014-2021, imageio contributors (BSD 2-clause)
#  Copyright (c) 2012-2013 Matplotlib Development Team; All Rights Reserved (MDT)
#  Copyright (c) 2015-2017, Zulko (MIT)
#  Copyright (c) 2005-2021, NumPy Developers (BSD 3-clause)
#
#  ****************************************************

# Handles rendering and animating of data passed in from outside

import os
import sys

import imageio as imio
import matplotlib.pyplot as plt
import moviepy.editor as mp
import numpy as np

from library import get_filename as fnm

class Artist:

    def __init__ (self,var,data,prefix,vector,plot_type):

        self.__var         = var
        self.__data        = data
        self.__prefix      = prefix
        self.__vector      = vector
        self.__plot_type   = plot_type

        self.__num = 0
        self.__xmn = 0
        self.__xmx = 0
        self.__ymn = 0
        self.__ymx = 0
        self.__qmn = 0
        self.__qmx = 0

        self.__filenames = []

        self.__failed = False

    def __str__ (self):

        return 'This is a Python class to render/animate data of {self.var}.'

    # create individual images
    def __render(self,n):

        try:
            qmx_actual = self.__qmx
            if self.__qmx == 0:
                qmx_actual = np.max(self.__data[n])

            fig = plt.figure()
            img = plt.imshow(self.__data[n],
                             extent=[self.__xmn,
                                     self.__xmx,
                                     self.__ymn,
                                     self.__ymx],
                             vmin=self.__qmn,
                             vmax=np.max(self.__data[n]),
                             origin='lower')

            file = fnm.create_filename(self.__prefix,'.png',n)
            self.__filenames.append(file)

            fig.colorbar(img)
            plt.title("Render of " + self.__var + ", t = " + str(n+1))
            plt.xlabel("x (kpc)")
            plt.ylabel("y (kpc)")
            plt.savefig(file)
            plt.close(fig)

            print('   Created image ' + str(n+1))

        except Exception as e:
            self.__failed = True
            print('\nERROR: No valid output file to render.')
            print('Are there any left, and is the output file type .vtk?')
            print('syserror:',e)

    # animate output by rendering individual images then bringing together
    def animate(self,type):

        print('Rendering...\n')

        __gif_file = 'output/render.gif'
        __anm_file = 'output/render.mp4'
        for i in range(self.__num):
            self.__render(i)
        if self.__failed:
            __err_string = """
            \nAVE vizualization currently only takes .vtk output files
                 (with planned support for .ahdf in the future). If
                 rendering failed, double check that the simulation
                 output is .vtk in the parameter input file."""
            print(__err_string)

        try:
            print('\nDone.\n\nAnimating...\n')

            __images = []

            # save images for GIF
            for file in self.__filenames:
                __images.append(imio.imread(file))

            imio.mimsave(__gif_file,__images)     # create GIF from iamges
            gif = mp.VideoFileClip(__gif_file,audio=False)
            gif.write_videofile(__anm_file)     # create video from GIF
            os.system('rm ' + __gif_file)       # clean-up GIF

            os.system('mkdir -p output/images')
            os.system('mv output/*.png output/images')

            print('\nImages saved in folder in "output."\n')

        except Exception as e:
            print('ERROR: Animation failed. Did rendering also fail?')
            print('       ' + str(e))

    ### Public get/set methods for class member fields

    # num
    @property
    def num(self):
        return self.__num
    @num.setter
    def num(self,num):
        self.__num = num

    # xmn
    @property
    def xmn(self):
        return self.__xmn
    @xmn.setter
    def xmn(self,xmn):
        self.__xmn = xmn

    # xmx
    @property
    def xmx(self):
        return self.__xmx
    @xmx.setter
    def xmx(self,xmx):
        self.__xmx = xmx

    # ymn
    @property
    def ymn(self):
        return self.__ymn
    @ymn.setter
    def ymn(self,ymn):
        self.__ymn = ymn

    # ymx
    @property
    def ymx(self):
        return self.__ymx
    @ymx.setter
    def ymx(self,ymx):
        self.__ymx = ymx

    # qmn
    @property
    def qmn(self):
        return self.__qmn
    @qmn.setter
    def qmn(self,qmn):
        self.__qmn = qmn

    # qmx
    @property
    def qmx(self):
        return self.__qmx
    @qmx.setter
    def qmx(self,qmx):
        self.__qmx = qmx

    # (constructor read_only variables)

    @property
    def var(self):
        return self.__var
