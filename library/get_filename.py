#  ****************************************************
#
#  Created by Christopher Sharp in 2021
#  Copyright (c) 2021, Christopher Sharp (MIT license)
#
#  ****************************************************

# returns order of magnitude for number of zeroes
def return_omag(amt,ord):
    if amt / 10 < 1.0: return ord
    else: return return_omag(amt / 10,ord + 1)

# filename is assumed prefix plus zeroes plus
# output file number plus suffix
def create_filename(prefix,suffix,num):
    mag = return_omag(num,0)
    filename = prefix + ('0' * (4 - mag)) + str(num) + suffix
    return filename
