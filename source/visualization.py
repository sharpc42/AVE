#  ****************************************************
#
#  Created by Christopher Sharp in 2021
#  Copyright (c) 2021, Christopher Sharp (MIT)
#
#  Uses Athena++ by Princeton University without changes
#  Copyright (c) 2016, PrincetonUniversity (BSD 3-clause)
#
#  Uses NumPy as Python module without changes
#  Copyright (c) 2005-2021, NumPy Developers (BSD 3-clause)
#
#  ****************************************************

# Visualizes output data of Athena++ simulations by
# gathering relevant variables from parameter input
# files, importing the data from the output files,
# creating .csv table files for each time step, then
# rendering the data as an animated video.

import os
import shutil

import numpy as np

import library.process_data as process
import library.get_filename as fnm

from . import artist

class Visualizer:

    def __init__(self,var,qmn,qmx,vector,dims,plot_type):

        self.__var         = var
        self.__qmn         = qmn
        self.__qmx         = qmx
        self.__vector      = vector
        self.__dims        = dims
        self.__plot_type   = plot_type

        self.__tlim   = 0
        self.__dt     = 0
        self.__num    = 0
        self.__xmn    = 0
        self.__xmx    = 0
        self.__ymn    = 0
        self.__ymx    = 0
        self.__zmx    = 0

        self.__prob_in    = ""
        self.__prob_out   = ""
        self.__prefix     = ""
        self.__suffix     = ""
        self.__file       = ""

        self.__data = []

    def __str__(self):

        return 'This is a Python Class to visualize outputs of {self.var}.'

    # get parameters from input file assuming standards (see docs)
    def get_params(self):

        cwd = os.getcwd()
        file_path = cwd + '/athena/bin/athinput.' + self.__prob_in.lower()
        paraminput = open(file_path)
        paramlines = [line.strip() for line in paraminput]

        # get parameter from input file, searching by block
        def returnparam(ident,block):
            blk_found = False
            for i in range(0,len(paramlines)):
                line = paramlines[i]
                if block in line: blk_found = True  # block always before ident
                if ident in line and blk_found: return line.split()[2]
            return ""

        # Get file extention to expect for ouptut - this may be
        # in either output block in the parameter input file
        # with other option being .hst history file which AVE
        # does not currently use

        suffix_poss_1 = '.' + str(returnparam("file_type","output1"))
        out_blk_num_poss_1 = 1
        suffix_poss_2 = '.' + str(returnparam("file_type","output2"))
        out_blk_num_poss_2 = 2

        # Dont' want the history file
        if suffix_poss_1 == '.hst':
            self.__suffix = suffix_poss_2
            self.__prefix += 'out' + str(out_blk_num_poss_2) + '.'
        elif suffix_poss_2 == '.hst':
            self.__suffix = suffix_poss_1
            self.__prefix += 'out' + str(out_blk_num_poss_1) + '.'
        else:
            #print("\n   DONALD TRUMP GUILTY???   /n")
            print("\n   Couldn't find the file extension correctly!   \n")

        # Grab both time limit and time step the calculate the
        # expected number of files.

        self.__tlim = float(returnparam("tlim","time"))
        self.__dt = float(returnparam("dt","output2"))
        self.__num  = int(self.__tlim / self.__dt)

        # Grab spatial dimensions

        self.__xmn = float(returnparam("x1min","mesh"))
        self.__ymn = float(returnparam("x2min","mesh"))
        self.__zmn = float(returnparam("x3min","mesh"))

        self.__xmx = float(returnparam("x1max","mesh"))
        self.__ymx = float(returnparam("x2max","mesh"))
        self.__zmx = float(returnparam("x3max","mesh"))

        print('Done.\n')

    def move_output_files(self):
        os.system("mv athena/bin/*" + self.__suffix + " output")

    # scalar quantity assumed; will support vectors in the future
    def get_data(self):

        self.__data = process.file_data(self.__var,
                                        self.__prefix,
                                        self.__suffix,
                                        self.__num,
                                        self.__vector)
        print('Done.\n')

    # create and save a .csv file
    def create_csv(self):

        print('Creating CSVs from output files...')
        try:
            for i in range(self.__num):
                file = fnm.create_filename(self.__prefix,'.csv',i)
                np.savetxt(file,self.__data[i])
        except:
            print('ERROR: Ran out of output files. Did the simulation complete?')

        # outside try/exc bc still want to move incomplete set of files
        os.system('mkdir -p output/csv')
        os.system('mv output/*.csv output/csv')

    # render individual frames and animate, then compress files
    def render_data(self):

        art = artist.Artist(self.__var,
                            self.__data,
                            self.__prefix,
                            self.__vector,
                            self.__plot_type)

        art.num = self.__num
        art.xmn = self.__xmn
        art.xmx = self.__xmx
        art.ymn = self.__ymn
        art.ymx = self.__ymx
        art.qmn = self.__qmn
        art.qmx = self.__qmx

        art.animate('render')

        print('Compressing images and CSVs...')
        shutil.make_archive('output/images','zip','output/images')
        print('Images done.')
        shutil.make_archive('output/csv','zip','output/csv')
        print('CSVs done\nDone.\n')

    ### Public get/set methods for class member fields

    # output prob ID
    @property
    def prob_out(self):
        return self.__prob_out
    @prob_out.setter
    def prob_out(self,prob_out):
        self.__prob_out = prob_out

    # input prob ID
    @property
    def prob_in(self):
        return self.prob_in
    @prob_in.setter
    def prob_in(self,prob_in):
        self.__prob_in = prob_in

    # prefix
    @property
    def prefix(self):
        return self.__prefix
    @prefix.setter
    def prefix(self,prfx):
        self.__prefix = prfx

    # (constructor read-only fields)

    @property
    def tlim(self):
        return self.__tlim
    @property
    def dt(self):
        return self.__dt
    @property
    def num(self):
        return self.__num
    @property
    def xmn(self):
        return self.__xmn
    @property
    def xmx(self):
        return self.__xmx
    @property
    def ymn():
        return self.__ymn
    @property
    def ymx(self):
        return self.__ymx
    @property
    def zmn(self):
        return self.__zmn
    @property
    def zmx(self):
        return self.__zmx
    @property
    def suffix(self):
        return self.__suffix
    @property
    def file(self):
        return self.__file
    @property
    def data(self):
        return self.__data
