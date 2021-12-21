#!/bin/sh

#  getinputfiles.sh
#
#  ****************************************************
#
#  Created by Christopher Sharp on 12/18/21.
#  Copyright (c) 2021, Christopher Sharp (MIT license)
#
#  Uses Athena++ by Princeton University without changes
#  Copyright (c) 2016, PrincetonUniversity (BSD 3-clause)
#
#  ****************************************************

#  Gather up Athena++ input files for parsing by the interface

> hydroinputlist.txt
for filename in athena/inputs/hydro/athinput.*; do
    extension=${filename##*.}
    echo $extension >> hydroinputlist.txt
done

> mhdinputlist.txt
for filename in athena/inputs/mhd/athinput.*; do
    extension=${filename##*.}
    echo $extension >> mhdinputlist.txt
done
