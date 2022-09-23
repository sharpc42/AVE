# Athena Virtual Environment

Welcome to the AVE! This is a Python wrapper for the Athena++ astrophysics code. 

Currently this is mainly tested for MacOS, but as of May 13, 2022 it should play
nice with WSL for Windows (see Windows-specific instructions below) and likely
Linux as well, but the latter has not been explicitly tested outside of WSL.

## If You Already Have Athena++

The AVE currently looks for the Athena++ directory to be in the same `AVE` folder as 
this. So you'll need to move it or a copy of it here. Once there, you should be able 
to move an input file of your choice into the `athena/bin` folder, then feel free to 
skip to General Use below. 

The AVE can generally take care of configuration if you don't want to, but for first 
use it may be good to do one manually to fully avoid errors. (The automatic setup does 
a dummy configuration for this reason.)

There should be better file path support soon because obviously the above is crude and 
inflexible.

## Automatic Setup

Run the setup script by typing

    bash setup.sh

into the terminal while in the AVE top directory. This should get Athena++ for you as 
well as all necessary missing Python modules. If you have Anaconda or Miniconda, make
sure you are in the environment you'll be using before running and answer "y(es)" when
prompted, since they have their own conda install command to be run in the environment.

(If you have an error you can try `sh setup.sh` instead but this tends to have errors
of its own, at least in Linux environments.)

## Manual Setup

These are more or less just the steps taken by the `setup.sh` script recommended above.

- Make sure you are in a good Python environment like Anaconda, otherwise Python won't 
execute.
- Update your Python environment with the necessary modules; if you don't use `setup.sh` 
then these will be in the `requirements.txt` (which setup deletes when finished to avoid 
messiness). The documentation will also have these, and the licensing because we give 
credit here at the AVE.
- Download Athena++ to this directory as `athena` via the link to its 
[Git repo](https://github.com/PrincetonUniversity/athena/).
- Make sure you're in your OS terminal and `cd` to this `AVE` directory, wherever you 
downloaded it.
- Type in `chmod +x ave.py` to make the main AVE file executable. This has to be done 
locally on the computer in question.

## Starting AVE

To run the AVE is simple enough. Type in `./ave.py` and follow the on-screen instructions.

## Windows-specific Advice

To run on Windows currently, you'll need to use a Linux emulator of some sort. Cygwin is 
a popular option but I like [Windows Subsystem for Linux (WSL)](https://docs.microsoft.com/en-us/windows/wsl/install) better. Here's my process,
good for "Windows 10 version 2004 and higher (Build 19041 and higher) or Windows 11":

- Install Python3 via the Windows store
- Run Powershell as administrator (needs privileges)
- Type `wsl --install` to install WSL or Windows Subsystem for Linux, basically a CLI Ubuntu emulator
- Restart computer to complete installation process
- Create UNIX account when prompted (basically equivalent to local user account)
- Enter command `sudo apt update`
- Enter password when prompted (the one from two steps ago)
- Enter command `sudo apt install python3-pip`
- Enter command `sudo apt install python-is-python3`
- Git clone AVE like above
- Run through setup.sh same as above
- Use "python ave.py" to start AVE

But as long as you're in a Linux emulator, if you're a fan of Cygwin or something, then more or less following the original setup instructions should work. There should be no additional difficulties or issues with visualizing output so long as your machine can do .png and .mp4 files.

## General Use

Alright, now you're ready to rock n' roll (an underpressurized cloud into a supporting 
magnetic field). 

First you'll be prompted to say if you're looking to run the simulation, visualize the 
output, or both at once. Just simulating saves time, while visualizing the output alone 
is good is you already have simulation data to render; perhaps you want to iterate through 
different min/max values.

### Running a Simulation

The idea of the current AVE is that half of the user interaction is just manipulating a 
parameter input file; the other half is running the AVE itself. This parameter input file 
contains the many variables needed by the corresponding simulation dedicated to it. (The 
input file specifies its particular "problem file" inside.) The ideal workflow of the AVE 
is this: once downloaded, move the input file of the simulation desired to the `bin` folder 
within the Athena++ installation, make the edits you need, and run the AVE. It's smart 
enough to check for an input in that `bin` folder to deduce which corresponding problem 
file you'll need to run.

After that, the AVE will ask you if you want magnetic fields or not as this affects how 
Athena++ configures. If configuration ends up being needed, the AVE will handle that before 
trying to run the simulation.

### Visualizing Output

If you're visualizing output data per time step, the AVE will prompt you for which variable 
you want to render -- as several are in the output files generated -- as well as minimum 
and maximum quantities for the image data range. (These correspond to the expected range of 
physical values in whatever code units you choose; see documentation.) 

It then renders and saves 2D images and an animation of the simulation data for that 
physical quantity. In the near future 3D rendering via cross-sectional slices will be 
supported. (*NOTE: Right now the AVE only supports `.vtk` output files; `.ahdf` files will 
be supported in the near future. Anything else in the input file will generate an error; 
see documentation.*) A `.csv` table file is also created for each time step for personal
data analysis.

You're all set! Make us proud.
