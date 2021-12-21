#!/bin/sh

#  getprobfiles.sh
#
#  ****************************************************
#
#  Created by Christopher Sharp on 09/11/21.
#  Copyright (c) 2021, Christopher Sharp (MIT license)
#
#  Uses Athena++ by Princeton University without changes
#  Copyright (c) 2016, PrincetonUniversity (BSD 3-clause)
#
#  ****************************************************

#  Gather up boundary-condition problem files
#  for Athena++ for parsing by the interface

> problist.txt
for filename in athena/src/pgen/*.cpp; do
    file=${filename##*/}
    base=${file%%.*}
    echo $base >> problist.txt
done
