# Connect4-3D
Connect4-3D is an exciting project created by students at Sherbrooke University in Quebec, Canada. The goal of the project is to build a robotic arm that can play Connect 4 in 3D against a human. This README file contains information on how to replicate the project and includes links to all the necessary code, CAD files, and installation procedures.


<a href="https://youtu.be/UQO0S-S_vtE
" target="_blank"><img src="http://img.youtube.com/vi/UQO0S-S_vtE/0.jpg" 
alt="Robot Demonstration" width="240" height="180" border="10" /></a>

# Project Overview
The project is open source and is licensed under the GNU General Public License v3.0 (GPLv3). The main components of the project are:

The OpenCR card code for controlling the robotic arm
The computer code for processing the game board and communicating with the OpenCR board
The CAD files for 3D printing the parts
A Bill of Materials (BOM) listing all the non-printed materials used

1. All the code of the OpenCR card is in the directory: Connect_12_OpenCR
  1.1 The executable code is named stateMachineAutoOnly_copy_20230308124647 in the folder with the same name
  1.2 The file PingMotorsID is pingning all the motors ID connected to the OpenCR board
  1.3 The file named ServoReadLive is monitoring the live position of the first and second joint

2. All the code of the computer is in the directory: Connect_12_PI

3. All the CADS of the 3D printed parts are available directly on OnShape with this link: 
                https://cad.onshape.com/documents/92b82e0c23a4517eca2f38d9/w/46a67cc575363ff8875ca5a8/e/41a671f2d443bbba929bd6fb

4. The list of all material used that is not 3D printed can be found in the file BOM.xlsx

5. Installation procedure for the OpenCR board
  5.1 Install the Arduino IDE
  5.2 Download the Dynaxixel2Arduino library
  5.3 Download the OpenCR board manager
  5.4 Connect the OpenCR board to the computer with a USB cable
  5.5 Upload the executable code to the OpenCR board


6. Installation procedure for the computer
  1.1 Install VS Code IDE
  1.2 Download following libraries: 
    1.2.1 OpenCV
    1.2.2 Numpy
    1.2.3 pyzbar
    1.2.4 random
    1.2.5 time
    1.2.6 os
    1.2.7 sys
    1.2.8 PyQt5
    1.2.9 cv2
    1.2.10 struct
    1.2.11 serial
  1.3 Connect the computer to the camera with a USB cable
  1.4 Run the file named main.py
  1.5 Enjoy!


# Conclusion
We hope you find this project exciting and informative. If you have any questions or comments, please feel free to reach out to us. Happy building!


    