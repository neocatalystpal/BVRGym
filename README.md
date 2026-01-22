# BVRGym
## Description
This library is based on JSBSim software (https://github.com/JSBSim-Team/jsbsim). 
This library's primary purpose is to allow users to explore Beyond Visual Range (BVR) tactics using Reinforcement learning while utilizing JSBSim high-fidality flight dynamics models.

## Requirments
The following libraries are required to run BVRGym. 
The code has been tested with Python 3.9 

pip install jsbsim pyproj pymap3d torch tensorboard py_trees

## BVR air combat training

To start training an agent for BVR air combat, run the following command

python main.py 



## Understanding BVRGym

BVRGym has a 3 level structure. Level 1 is the lowest level where the python interacts with JSBSim flight dynamics simulator. Examples of the level 1 objects are within BVRGYM/jsb_gym/simObjects directory. Here we have both the aircraft class and the missile class. 

To test these objects in isolated scenario, place yourself in BVRGYM directory and then run following commands:

### To test aircraft (Level 1)

terminal 1:

python -m tests.test_aircraft.py

Vizualize F16 (Flightgear description below if you have not installed it)

terminal 2:

fgfs --fdm=null --native-fdm=socket,in,60,,5550,udp --aircraft=f16-block-52 --airport=ESSA --multiplay=out,10,127.0.0.1,5000 --multiplay=in,10,127.0.0.1,5001


### To test missile (Level 1)

terminal 1:

python -m tests.test_missile.py

terminal 2: 

fgfs --fdm=null --native-fdm=socket,in,60,,5550,udp --aircraft=f16-block-52 --airport=ESSA --multiplay=out,10,127.0.0.1,5000 --multiplay=in,10,127.0.0.1,5001

terminal 3: 

fgfs --fdm=null --native-fdm=socket,in,60,,5551,udp --aircraft=ogel --airport=ESSA --multiplay=out,10,127.0.0.1,5001 --multiplay=in,10,127.0.0.1,5000


### Test Agent

python -m tests.test_agent.py


### Test BVR Environment + Tacview 

python -m tests.test_tacview.py

Tacview data in data_output/tacview



## FlightGear
FlightGear offers an excellent tool for visualizing the units present in BVRGym. 
To install FlightGear (Tested on Ubuntu 20.04.6 LTS)

sudo add-apt-repository ppa:saiarcot895/flightgear

sudo apt update

More details on https://launchpad.net/~saiarcot895/+archive/ubuntu/flightgear

After installing FlightGear, start the program, go to Aircraft tab and download General Dynamics F16 aircraft.

To have a missile model as well, copy the ogel folder from this repo (fg/ogel) to the Flightgears aircraft directory. 
To visualize missile in Flightgear, I used the ogel (1) model within the fgfs, replaced the grapical representations of the ogel with a missile that was available in fgfs (I think it was from (2)) and added a trail from santa claus (3) to see the trajectory. 

1) https://wiki.flightgear.org/Ogel

2) https://forum.flightgear.org/viewtopic.php?t=19930#p183249

3) https://wiki.flightgear.org/Santa_Claus

Given that you have both the f16 and ogel directories in the fgfs directory, you can visualize both units.


## Additional details 
Additional details can be found in the following article

BVR Gym: A Reinforcement Learning Environment for Beyond-Visual-Range Air Combat

https://arxiv.org/abs/2403.17533

Note that this article relates to an older version of the BVRGym, but it is still valid with remarks to understand Behavior Trees and other part of the environments.


## Tacview

Tacview is a flight data analysis tool used to visualize and debrief aerial missions in 2D and 3D, but its not for free. Here are some examples how it looks in tacview for different scenarios. You can find more details on how the flight recording file should look https://www.tacview.net/documentation/csv/en/  
