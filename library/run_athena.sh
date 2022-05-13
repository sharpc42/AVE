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
  
    ANSWERED=false
    while [ $ANSWERED = 'false' ]
      do
        echo "Athena files found. Run anyway? This will overwrite files. (y/n)?"
        
        read OVERWRITE && [ $OVERWRITE = [yY] ]

	if [[ $OVERWRITE == [yY] || $OVERWRITE == [yY][eE][sS] ]]
          then
            ANSWERED=true
            
            FOUND_ATHENA='false'
            while [ $FOUND_ATHENA = 'false' ]
              do
                if [ -f athena/bin/athena ]
                  then
                    FOUND_ATHENA='true'
                    rm output/*.vtk
		    
                    
                    echo "\nPress any key to begin. (This may take a while.)"
                    read -n 1

                    echo "Running Athena..."
                    cd athena/bin
                    ./athena -i athinput.$1
                    mv *.vtk ../../output
                    echo "Simulation complete.\n"
                    cd ..
                else
                    echo "\nCan't run Athena, configuration didn't occur correctly!"
                    echo "Trying to reconfig. If this doesn't work, try again while letting original configuation proceed uninterrupted.\n"
                    cd athena
                    make
                    cd ..
                fi
              done
            
        elif [[ $OVERWRITE == [nN] || $OVERWRITE == [nN][oO] ]]
	then
            ANSWERED=true
            echo "Understood. Skipping simulation.\n"
            
        else
            echo "Please answer yes or no. Thank you.\n"

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
