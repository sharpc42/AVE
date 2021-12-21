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
    echo "The AVE is already installed! :)"
    exit 0
fi

echo "\nThe AVE was tested for Python 3.9.5 - if you have problems, consider"
echo "   updating to a version of Python at least as new as that.\n"

# install required packages
echo "I'd like to check for and automatically install required packages now,"
echo "   including Athena++ the simulation code AVE wraps. Is that okay? (y/n)"

read PRE_REQS
CHK_REQ=false

while [ $CHK_REQ == 'false' ]
do
    if [[ $PRE_REQS == 'y' ]]
      then
        CHK_REQ=true
        echo "\nGot it. Thank you. Checking for and installing them...\n"
        pip install -r requirements.txt
        echo "Done.\n"
        if [ -d "athena" ]
          then
            echo "*Athena++ already installed*"
        else
            echo "Now I will check for and install Athena++ as necessary.\nPress any key to continue."
            read -n 1
            echo "Now installing Athena++ code...\n"
            git clone https://github.com/PrincetonUniversity/athena/
            echo "\nAthena++ is installed.\n"
            echo "" > athena/src/pgen/dummy.cpp
            cd athena
            ./configure.py --prob dummy
            make
            cd ..
            rm athena/src/pgen/dummy.cpp
        fi
    elif [[ $PRE_REQS == 'n' ]]
      then
        CHK_REQ=true
        echo "\nOkay. If you encounter any problems running AVE, you might want"
        echo "   to double-check with the documentation to make sure you have all"
        echo "   the right Python packages. You'll also need to download Athena++"
        echo "   manually.\n"
    else
        echo "\nPlease answer yes or no. Thank you.\n"
    fi
    rm requirements.txt
done

chmod +x ave.py

echo "AVE file can be run from the terminal.\n"

echo "" > __installed__

echo "You're all set to start using the AVE!\n"
exit 0
