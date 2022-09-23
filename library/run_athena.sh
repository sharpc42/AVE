#!/bin/bash

#  run_athena.sh
#
#  ****************************************************
#
#  Created by Christopher Sharp on 5/20/21.
#  Copyright (c) 2021, Christopher Sharp (MIT license)
#
#  Uses Athena++ by Princeton University without changes
#  Copyright (c) 2016, PrincetonUniversity (BSD 3-clause)
#
#  ****************************************************

# Run Athena++ overwriting files if user asks (quitting otherwise)
#
# Also checks if Athena++ configured properly, and just "makes" if
# not. This is a niche case for most users, but worth mentioning.

COUNT=`ls -1 output/*.vtk 2>/dev/null | wc -l`
if [ $COUNT != 0 ]
  then
     printf "Warning: Athena files found. This will overwrite files if they're the same simulation."
     FOUND_ATHENA='false'
     while [ $FOUND_ATHENA = 'false' ]
     do
         if [ -f athena/bin/athena ]
           then
             FOUND_ATHENA='true'
             rm output/*.vtk
             printf "\nPress any key to begin. (This may take a while.)"
             read -n 1
             printf "\nRunning Athena...\n"
             cd athena/bin
             ./athena -i athinput.$1
             #mv *.vtk ../../output  # move to visualization.py
             printf "Simulation complete.\n"
             cd ..
         else
             printf "\nCan't run Athena, configuration didn't occur correctly!"
             printf "Trying to reconfig. If this doesn't work, try again while\n"
             printf "    letting original configuation proceed uninterrupted.\n"
             cd athena
             make
             cd ..
         fi
     done
else
    echo "Press any key to begin. (This may take a while.)"
    read -n 1
    echo "Running Athena..."
    cd athena/bin
    ./athena -i athinput.$1
    mv *.vtk ../../output
    echo "Simulation complete.\n"
    cd ..
fi
