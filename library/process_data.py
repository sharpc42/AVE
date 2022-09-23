#  ****************************************************
#
#  Created by Christopher Sharp in 2021
#  Copyright (c) 2021, Christopher Sharp (MIT license)
#
#  Uses Athena++ by Princeton University without changes
#  Copyright (c) 2016, PrincetonUniversity (BSD 3-clause)
#
#  ****************************************************

import os

import athena.vis.python.athena_read as athena

from . import get_filename as fnm

def file_data(var,prefix,suffix,num,vector):

    data = []
    cwd  = os.getcwd()

    for n in range(int(num) + 1):
        file = fnm.create_filename(prefix,suffix,n)

        print("TEST:",n)
        # scalar case; vector support later
        if vector is False:
            x,y,z,q = athena.vtk(file)  # only vtk support now
            data.append(q[var][0])

    return data
