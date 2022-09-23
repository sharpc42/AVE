
#  ****************************************************
#
#  Created by Christopher Sharp in 2021
#  Copyright (c) 2021, Christopher Sharp (MIT)
#
#  Uses Athena++ by Princeton University without changes
#  Copyright (c) 2016, PrincetonUniversity (BSD 3-clause)
#
#  ****************************************************

# Main script for the AVE interface, taking user input
# to identify variables which can't be automatically
# determined, but otherwise tries to find everything
# without any help.

import argparse
import os
import sys

from .visualization import Visualizer

global prob_out
global prob_src
global prob_in
global config_line
global mag_fields

def main():

    # three prob IDs to get
    prob_out    = ''
    prob_src    = ''
    prob_in     = ''

    config_line = ''

    #global user_input = 0

    #global force_config = False
    #mag_fields = False
    #global sim          = False
    #global viz          = False

    parser = argparse.ArgumentParser()
    parser.add_argument('--config', help="force configuration", action='store_true')
    args = parser.parse_args()
    force_config = args.config



    # ---------------------------------
    # Get messages and ask for use case
    # ---------------------------------

    msg_file = open('library/messages','r')
    msg_list = msg_file.read().splitlines()
    messages = {msg.split(":")[0]: msg.split(":")[1] for msg in msg_list}

    while True:
        print('')
        for i in range(0,4): print(messages['input_ave_'+str(i)])
        user_input = input('')
        try: user_input = int(user_input)
        except: print(messages['num_err'] + '\n')

        if user_input == 1:
            sim = True
            break
        elif user_input == 2:
            viz = True
            break
        elif user_input == 3:
            sim = True
            viz = True
            break
        else:
            print(messages['options_err'] + '\n')



    # ------------------------------------------------
    # Get problem ID to run simulation. First, try the
    # bin folder and deduce automatically. Second, try
    # to get a valid input from user based on lists
    # built from overlapping pgen/input files, and try
    # to move appropriate input file to bin folder.
    # ------------------------------------------------

    contents = os.listdir('athena/bin')
    input_file = [c for c in contents if 'athinput' in c]
    input_file.sort()   # alphabetical order used if multiple files

    # ---------------------------------
    # Get problem IDs from manual input
    # ---------------------------------

    def getProblemManually():

        mag_fields = False

        os.system('sh library/getprobfiles.sh')  # using source pgen files
        p = open('problist.txt','r')
        problist = p.read().splitlines()
        os.system('rm problist.txt')

        input_hydro_path = 'athena/inputs/hydro/athinput.'
        input_mhd_path   = 'athena/inputs/mhd/athinput.'
        dest_folder_path = 'athena/bin'

        for i in range(1,4): print(messages['path_err_'+str(i)])

        os.system('sh library/getinputfiles.sh')  # get hydro and mhd inputs

        h = open('hydroinputlist.txt','r')
        hydrolist = h.read().splitlines()
        os.system('rm hydroinputlist.txt')

        m = open('mhdinputlist.txt','r')
        mhdlist = m.read().splitlines()
        os.system('rm mhdinputlist.txt')

        # for safety, only want inputs with exact name overlaps with pgen files
        problist = set(problist)
        hydro_temp = []
        mhd_temp = []
        for hydro in hydrolist:
            if hydro in problist: hydro_temp.append(hydro)
        for mhd in mhdlist:
            if mhd in problist: mhd_temp.append(mhd)
        hydrolist = hydro_temp
        mhdlist = mhd_temp

        # get user input and display options if needed
        while True:
            user_input = input('\n' + messages['input_prob'] + '\n')
            if user_input in problist: 
                prob_src = user_input
                break
            else:
                if user_input != '':
                    print('\n' + messages['prob_err'])
                print(messages['prob_list'] + '\n\nHydro')
                for hydro in hydrolist: print('    ' + hydro)
                print('MHD')
                for mhd in mhdlist: print('    ' + mhd)

        # go ahead and get magnetic fields from user choice
        if prob_src.lower() in mhdlist and prob_src.lower() not in hydrolist:
            mag_fields = True   # since user selected from mhd exclusively
        elif prob_src.lower() in mhdlist and prob_src.lower() in hydrolist:
            while True:
                user_input = input(messages['input_mag_field'] + '\n')
                if user_input == 'y':
                    mag_fields = True
                    break
                elif user_input == 'n': break
                else: print(messages['yes_no_err'])

        # input prob ID is config prob ID as per above, copy input file to right folder
        prob_in = prob_src
        if mag_fields:
            os.system('cp ' + input_mhd_path + prob_in.lower() + ' ' + dest_folder_path)
        else:
            os.system('cp ' + input_hydro_path + prob_in.lower() + ' ' + dest_folder_path)

        # get output prob ID from the input file using input prob ID
        # (also get variable type and config line)
        file = open('athena/bin/athinput.' + prob_in)
        lines = [line.strip() for line in file]
        for line in lines:
            if 'problem_id' in line:
                prob_out = line.split()[2].split('=')[0]
            if 'variable' in line:
                var_type = line.split('=')[-1].split()[0]
            if 'configure' in line:
                eq = line.find('=')
                config_line = line[eq+2:].replace("==","=")
                if '-b' in config_line: mag_field = True

        # caution to check to make sure right file
        for i in range(1,8): print(messages['path_warn_'+str(i)])
        print('')



    # found input file automatically
    if input_file:

        paraminput = open('athena/bin/' + input_file[0])
        paramlines = [line.strip() for line in paraminput]

        for i in  range(0,len(paramlines)):
            line = paramlines[i]

            if "variable" in line:
                var_type = line.split('=')[-1].split()[0]  # get prim/cons variable

            if "configure" in line:
                eq = line.find('=')
                config_line = line[eq+2:].replace("==","=")  # get configuration
                if '-b' in config_line:
                    mag_fields = True  # detected automatically
                for arg in config_line.split():
                    if '--prob' in arg:
                        prob_src = arg.split('=')[-1]  # get config prob ID

            if "problem_id" in line:
                prob_out = line.split()[2].split('=')[0]  # get output prob ID

        prob_in = input_file[0].split('.')[-1]  # get input prob ID
        while True:
            print('\n*Athena problem file found: ' + prob_src + '*\n')
            user_input = input(messages['prob_ok'] + '\n')
            if user_input == 'y': break
            elif user_input == 'n':
                getProblemManually()
                break
            else:
                 print(messages['options_err'] + '\n')

    # input file can't be found automatically
    else:
        getProblemManually()



    # ---------------------------------------
    # Get user variables from input as needed
    # ---------------------------------------

    # set flag if Athena currently expects magnetic fields
    if sim or viz:

        make_prob = ''
        make_mag  = ''

        #b = ''  # needed?

        prob_str  = 'PROBLEM_FILE = '
        mag_str   = 'RSOLVER_DIR = '

        makefile  = open('athena/Makefile')
        makelines = [line.strip() for line in makefile]

        for line in makelines:
            if prob_str in line:
                i = len(prob_str)
                while line[i] != '.':
                    make_prob += line[i]
                    i += 1
            if mag_str in line:
                i = len(mag_str)
                while line[i] != '/':
                    make_mag += line[i]
                    i += 1

        mag_chk = True if make_mag == 'mhd' else False

    # magnetic field handling
    if sim:

        # ask for magnetic fields if not already deduced
        if not mag_fields:
            while True:
                user_input = input(messages['input_mag_field'] + '\n')
                if user_input == 'y':
                    mag_fields = True
                    break
                elif user_input == 'n': break
                else: print(messages['yes_no_err'] + '\n')

        # set config flag for later if not set for magnetic fields
        mag_flag = ''
        config_athena = False
        if not (make_prob == prob_src and mag_chk == mag_fields):
            mag_flag = str(mag_fields)
            config_athena = True

    if viz:

        if mag_chk is True: mag_fields = mag_chk

        # get physical quantity to track
        while True:
            for i in range(0,3): print(messages['input_var_'+str(i)])
            if mag_fields: print(messages['input_var_3'])

            user_input = input('')
            try: user_input = int(user_input)
            except: print(messages['num_err'] + '\n')

            if user_input == 1:
                if var_type == 'prim': var = 'rho'
                else: var = 'dens'
                break
            elif user_input == 2:
                var = 'press'
                break
            elif user_input == 3 and mag_fields: 
                var = 'b0'
                break
            else: print(messages['options_err'] + '\n')

        # get minimum of quantity to track
        while True:
            user_input = input('\n' + messages['input_min'])
            try:
                qmin = float(user_input)
                break
            except: print(messages['num_err'] + '\n')

        # get maximum of quantity to track (0=variable max)
        while True:
            user_input = input(messages['input_max'])
            try:
                qmax = float(user_input)
                break
            except: print(messages['num_err'] + '\n')

        print('')



    # ------------------------------------------------
    # Simulation itself with configure first if needed
    # then a call to Athena++ if user wants to run it
    # (may not if output files already exist, in which
    # case skip to processing)
    # ------------------------------------------------

    if sim:

        if force_config: config_athena = True
        if config_athena:
            os.system('cd athena && ./configure.py ' + config_line)
            os.system('cd athena && make clean && make')

            # check if Athena reverted to defaults->issue with config
            makefile = open('athena/Makefile')
            lines = [line.strip() for line in makefile]
            for line in lines:
                if 'shock_tube' in line and prob_src != 'shock_tube':
                    config_err_str = ''
                    for i in range(1,3):
                        config_err_str += messages['config_err'+str(i)] + '\n'
                    sys.exit(config_err_str)

        os.system('bash library/run_athena.sh ' + prob_in)


    # ------------------------------------------
    # Processing and rendering simulation output
    # ------------------------------------------

    if viz:

        print(messages['processing'] + '\n')
        vector = False  # vector quantities currently unsupported
        dims = 2   # 2D only, 3D currently unsupported
        plot_type = 'linear'  # linear only, logarithmic currently unsupported

        vis = Visualizer(var,qmin,qmax,vector,dims,plot_type)

        # get parameters and construct filename
        vis.prob_out  = prob_out
        vis.prob_in   = prob_in
        vis.prefix    = 'output/' + vis.prob_out + '.block0.out2.'
        vis.get_params()
        print(messages['get_data'] + '\n')
        vis.get_data()
        vis.create_csv()
        vis.render_data()
        print(messages['enjoy'] + '\n')

        # Try auto-open video for user
        if (sys.platform == 'darwin'):  # MacOS
            try:
                os.system('open output/render.mp4')
            except:
                pass
        elif (sys.platform == 'linux'):  # Linux
            try:
                os.system('xdg-open output/render.mp4')
            except:
                pass
        elif (sys.platform == 'win32'):  # Windows
            try:
                os.system('output\render.mp4')
            except:
                pass

    print(messages['thanks'])
