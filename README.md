# <u>Continuous Control</u>
### Introduction

The aim of this project is to control a double-jointed arm to follow a target moving within reach of the arm. The environment provided by [Unity](https://unity.com/), consists of a vector of 33 variables relating to the observation space and the position, rotation, velocity and angular velocities of the arm. The action space consists of 4 continuous action spaces ranging between [-1:1], which controls the torque of the 2 joints in the arm. A reward of +0.1 is given when the tip of the arm is in the correct location of the target, and a reward of 0.0 when not.

![GIF of Trained Network](Images/ContinuousControl.gif)

### Environment

To solve the environment, an average of +30 points needs to be achieved over 100 episodes.

The environment chosen for this project consists of 20 parallel agents interaction consecutively and independently. This is a more stable environment to learn from and the DDPG algorithm can make good use of the independent experiences. 

### Getting Started

To run this project yourself, you will need to follow the installation instructions listed below:

1. Follow this [Udacity Github link](https://github.com/udacity/deep-reinforcement-learning#dependencies) for instructions to install all the dependencies.

2. Download [this repository](https://github.com/jeroencvlier/DDPG-Continuous-Control) to your local computer.

3. Download and extract the environment inside the "DDPG-Continuous-Control" folder you just downloaded. Use one of the following links. You need only select the environment that matches your operating system:

    - **_Version 1: One (1) Agent_**
        - Linux: [click here](https://s3-us-west-1.amazonaws.com/udacity-drlnd/P2/Reacher/one_agent/Reacher_Linux.zip)
        - Mac OSX: [click here](https://s3-us-west-1.amazonaws.com/udacity-drlnd/P2/Reacher/one_agent/Reacher.app.zip)
        - Windows (32-bit): [click here](https://s3-us-west-1.amazonaws.com/udacity-drlnd/P2/Reacher/one_agent/Reacher_Windows_x86.zip)
        - Windows (64-bit): [click here](https://s3-us-west-1.amazonaws.com/udacity-drlnd/P2/Reacher/one_agent/Reacher_Windows_x86_64.zip)

    - **_Version 2: Twenty (20) Agents_**
        - Linux: [click here](https://s3-us-west-1.amazonaws.com/udacity-drlnd/P2/Reacher/Reacher_Linux.zip)
        - Mac OSX: [click here](https://s3-us-west-1.amazonaws.com/udacity-drlnd/P2/Reacher/Reacher.app.zip)
        - Windows (32-bit): [click here](https://s3-us-west-1.amazonaws.com/udacity-drlnd/P2/Reacher/Reacher_Windows_x86.zip)
        - Windows (64-bit): [click here](https://s3-us-west-1.amazonaws.com/udacity-drlnd/P2/Reacher/Reacher_Windows_x86_64.zip)
    
    (_For Windows users_) Check out [this link](https://support.microsoft.com/en-us/help/827218/how-to-determine-whether-a-computer-is-running-a-32-bit-version-or-64) if you need help with determining if your computer is running a 32-bit version or 64-bit version of the Windows operating system.

    (_For AWS_) If you'd like to train the agent on AWS (and have not [enabled a virtual screen](https://github.com/Unity-Technologies/ml-agents/blob/master/docs/Training-on-Amazon-Web-Service.md)), then please use [this link](https://s3-us-west-1.amazonaws.com/udacity-drlnd/P2/Reacher/one_agent/Reacher_Linux_NoVis.zip) (version 1) or [this link](https://s3-us-west-1.amazonaws.com/udacity-drlnd/P2/Reacher/Reacher_Linux_NoVis.zip) (version 2) to obtain the "headless" version of the environment.  You will **not** be able to watch the agent without enabling a virtual screen, but you will be able to train the agent.  (_To watch the agent, you should follow the instructions to [enable a virtual screen](https://github.com/Unity-Technologies/ml-agents/blob/master/docs/Training-on-Amazon-Web-Service.md), and then download the environment for the **Linux** operating system above._)
