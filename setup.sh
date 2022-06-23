#!/bin/sh
#
#  setup.sh
#
#  ****************************************************
#
#  Created by Christopher Sharp on 5/20/21.
#  Copyright (c) 2021, Christopher Sharp (MIT license)
#
#  Uses Athena++ by Princeton University without changes
#  Copyright (c) 2016, PrincetonUniversity (BSD 3-clause license)
#
#  Uses imagio, MatPlotLib, moviepy, and NumPy modules without changes
#  Copyright (c) 2014-2021, imageio contributors (BSD 2-clause)
#  Copyright (c) 2012-2013 Matplotlib Development Team; All Rights Reserved (MDT)
#  Copyright (c) 2015-2017, Zulko (MIT)
#  Copyright (c) 2005-2021, NumPy Developers (BSD 3-clause)
#
#  ****************************************************
#
#  Downloads dependencies for AVE and configures for use

# check if already installed
if test -f "./__installed__"
then
    printf "The AVE is already installed! :)\n"
    exit 0
fi

printf "\nThe AVE was tested for Python 3.9.5 - if you have problems, consider\n"
printf "   updating to a version of Python at least as new as that.\n"

# install required packages
CHK_REQ='false'
while [ $CHK_REQ = 'false' ]
do
    printf "\nI'd like to check for and automatically install required packages now,\n"
    printf "   including Athena++ the simulation code AVE wraps. Is that okay? (y/n)"
    read PRE_REQS

    if [ $PRE_REQS = 'y' ]
      then
	CHK_REQ='true'
        CHK_REQ_2='false'
	while [ $CHK_REQ_2 = 'false' ]
	do
		printf "\nAre you using an Anaconda or Miniconda environment? (y/n)"
		read CONDA
		if [ $CONDA = 'y' ]
		    then
			CHK_REQ_2='true'
	        	printf "\nGot it. Thank you. Updating dependencies...\n"
			conda config --append channels conda-forge
			conda install --file requirements
		elif [ $CONDA = 'n' ]
		    then
			CHK_REQ_2='true'
			printf "\nGot it. Thank you. Updating dependencies...\n"
        		pip install -r requirements
		else
			printf "\nPlease answer yes or no. Thank you.\n"
		fi
        	printf "Done.\n"
	done
        if [ -d "athena" ]
          then
            printf "\n*Athena++ already installed*"
        else
            printf "\nNow I will check for and install Athena++ as necessary.\nPress any key to continue."
            read -n 1
            printf "\nNow installing Athena++ code...\n"
            git clone https://github.com/PrincetonUniversity/athena/
            printf "\nAthena++ is installed.\n"
            printf "" > athena/src/pgen/dummy.cpp
            cd athena
            ./configure.py --prob dummy
            make
            cd ..
            rm athena/src/pgen/dummy.cpp
        fi
    elif [ $PRE_REQS = 'n' ]
      then
        CHK_REQ='true'
        printf "\nOkay. If you encounter any problems running AVE, you might want\n"
        printf "   to double-check with the documentation to make sure you have all\n"
        printf "   the right Python packages. You'll also need to download Athena++\n"
        printf "   manually.\n"
    else
        printf "\nPlease answer yes or no. Thank you.\n"
    fi
    rm requirements
done

chmod +x ave.py

printf "AVE file can be run from the terminal.\n"

echo "" > __installed__

printf "You're all set to start using the AVE!\n"
exit 0
