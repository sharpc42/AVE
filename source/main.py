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

import os
import sys

from .visualization import Visualizer

def main():
    
    problem   = ''
    
    user_input = 0
    
    mag_fields   = False
    move_on      = False
    sim          = False
    viz          = False
    
    
    
    # ---------------------------------
    # Get messages and ask for use case
    # ---------------------------------
    
    msg_file = open('library/messages.txt','r')
    msg_list = msg_file.read().splitlines()
    messages = {msg.split(":")[0]: msg.split(":")[1] for msg in msg_list}
    
    while not move_on:
        move_on = True
        
        print('')
        for i in range(0,4): print(messages['input_ave_'+str(i)])
        user_input = input('')
        try: user_input = int(user_input)
        except: print(messages['num_err'] + '\n')
        
        if user_input == 1: sim = True
        elif user_input == 2: viz = True
        elif user_input == 3:
            sim = True
            viz = True
        else:
            move_on = False
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
    
    os.system('sh library/getprobfiles.sh')  # using source pgen files
    p = open('problist.txt','r')
    problist = p.read().splitlines()
    os.system('rm problist.txt')
    
    # found input file automatically
    if input_file:
    
        paraminput = open('athena/bin/' + input_file[0])
        paramlines = [line.strip() for line in paraminput]
        
        for i in  range(0,len(paramlines)):
            line = paramlines[i]
            if "problem_id" in line:
                config_line = line.split()
                problem = config_line[2].split('=')[0]
        file_ext = input_file[0].split('.')[-1]  # get input file extension
        print('\n*Athena problem file found: ' + problem + '*\n')
        
        # check if appropriate source file exists using problist
        # (fatal error if not as sim needs this file)
        if not problem.lower() in problist:
            pgen_fail_str = ""
            for i in range(1,8):
                pgen_fail_str += messages['pgen_fail_'+str(i)] + '\n'
            sys.exit(pgen_fail_str)
    
    # input file can't be found automatically
    else:
    
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
        move_on = False
        while not move_on:
            move_on = True
            user_input = input('\n' + messages['input_prob'] + '\n')
            if user_input in problist: 
                problem = user_input
            else:
                print(messages['prob_err'] + '\n')
                print('Hydro')
                for hydro in hydrolist: print('   ' + hydro)
                print('MHD')
                for mhd in mhdlist: print('   ' + mhd)
                move_on = False
                
        # go ahead and get magnetic fields from user choice
        if problem.lower() in mhdlist and problem.lower() not in hydrolist:
            mag_fields = True   # since user selected from mhd exclusively
        elif problem.lower() in mhdlist and problem.lower() in hydrolist:
            move_on = False
            while not move_on:
                move_on = True
                user_input = input(messages['input_mag_field'] + '\n')
                if user_input == 'y': mag_fields = True
                elif user_input == 'n': pass
                else:
                    move_on = False
                    print(messages['yes_no_err'])
        
        if mag_fields:
            os.system('cp ' + input_mhd_path + problem.lower() + ' ' + dest_folder_path)
        else:
            os.system('cp ' + input_hydro_path + problem.lower() + ' ' + dest_folder_path)
        for i in range(1,8): print(messages['path_warn_'+str(i)])
        file_ext = problem
        print('')
        
        
        
    # ---------------------------------------
    # Get user variables from input as needed
    # ---------------------------------------
    
    # set flag if Athena currently expects magnetic fields
    if sim or viz:
    
        make_prob = ''
        make_mag  = ''
        
        b = ''
        
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
        move_on = False
        
        # ask for magnetic fields if not already deduced
        if not mag_fields:
            while not move_on:
                move_on = True
                user_input = input(messages['input_mag_field'] + '\n')
                if user_input == 'y':
                    mag_fields = True
                elif user_input == 'n':
                    pass
                else:
                    move_on = False
                    print(messages['yes_no_err'] + '\n')
                
        # set config flag for later if not set for magnetic fields
        mag_flag = ''
        config_athena = False
        if not (make_prob == problem and mag_chk == mag_fields):
            mag_flag = str(mag_fields)
            config_athena = True
        
    if viz:
        
        move_on = False
        if mag_chk is True: mag_fields = mag_chk
        
        # get physical quantities
        while not move_on:
            move_on = True
            
            for i in range(0,3): print(messages['input_var_'+str(i)])
            if mag_fields: print(messages['input_var_3'])
            
            user_input = input('')
            try: user_input = int(user_input)
            except: print(messages['num_err'] + '\n')
                
            if user_input == 1: var = 'rho'
            elif user_input == 2: var = 'press'
            elif user_input == 3 and mag_fields: var = 'b0'
            else:
                move_on = False
                print(messages['options_err'] + '\n')
        
        move_on = False
        while not move_on:
            user_input = input('\n' + messages['input_min'])
            try:
                qmin = float(user_input)
                move_on = True
            except: print(messages['num_err'] + '\n')
                
        move_on = False
        while not move_on:
            user_input = input(messages['input_max'])
            try:
                qmax = float(user_input)
                move_on = True
            except: print(messages['num_err'] + '\n')
            
        print('')
    
    

    # ------------------------------------------------
    # Simulation itself with configure first if needed
    # then a call to Athena++ if user wants to run it
    # (may not if output files already exist, in which
    # case skip to processing)
    # ------------------------------------------------
    
    if sim:
    
        if config_athena:
            os.system('sh library/config_athena.sh ' + problem.lower() + ' ' + mag_flag)

        os.system('bash library/run_athena.sh ' + file_ext)
        
        
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
        vis.problem  = problem
        vis.file_ext = file_ext
        vis.prefix   = 'output/' + vis.problem + '.block0.out2.'
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
