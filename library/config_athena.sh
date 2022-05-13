`#!/bin/sh`

#  config_athena.sh
#
#  ****************************************************
#
#  Created by Christopher Sharp on 9/25/21.
#  Copyright (c) 2021, Christopher Sharp (MIT license)
#
#  Uses Athena++ by Princeton University without changes
#  Copyright (c) 2016, PrincetonUniversity (BSD 3-clause)
#
#  ****************************************************

#  Config Athena with separate shell script

cd athena
echo "./configure.py --prob $1"
MAKE='True'

if [ $2 = 'True' ]
  then
    ./configure.py --prob $1 -b
elif [ $2 = 'False' ]
  then
    ./configure.py --prob $1
else
    echo "ERROR: Must pass 'True' or 'False' for 2nd argmt incl magnetic fields"
    MAKE='False'
fi

if [ $MAKE = 'True' ]
  then
    make clean
    make
fi
