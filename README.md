# Connect4-3D
Connect4-3D is an exciting project created by students at Sherbrooke University in Quebec, Canada. The goal of the project is to build a robotic arm that can play Connect 4 in 3D against a human. This README file contains information on how to replicate the project and includes links to all the necessary code, CAD files, and installation procedures.


<a href="https://youtu.be/UQO0S-S_vtE
" target="_blank"><img src="http://img.youtube.com/vi/UQO0S-S_vtE/0.jpg" 
alt="Robot Demonstration" width="240" height="180" border="10" /></a>

# Project Overview
The project is open source and is licensed under the GNU General Public License v3.0 (GPLv3). The main components of the project are:<br>

The OpenCR card code for controlling the robotic arm<br>
The computer code for processing the game board and communicating with the OpenCR board<br>
The CAD files for 3D printing the parts<br>
A Bill of Materials (BOM) listing all the non-printed materials used<br>

1. All the code of the OpenCR card is in the directory: Connect_12_OpenCR
  1.1 The executable code is named stateMachineAutoOnly_copy_20230308124647 in the folder with the same name<br>
  1.2 The file PingMotorsID is pingning all the motors ID connected to the OpenCR board<br>
  1.3 The file named ServoReadLive is monitoring the live position of the first and second joint<br>

2. All the code of the computer is in the directory: Connect_12_PI

3. All the CADS of the 3D printed parts are available directly on OnShape with this link: 
                https://cad.onshape.com/documents/92b82e0c23a4517eca2f38d9/w/46a67cc575363ff8875ca5a8/e/41a671f2d443bbba929bd6fb

4. The list of all material used that is not 3D printed can be found in the file BOM.xlsx

5. Installation procedure for the OpenCR board<br>
  5.1 Install the Arduino IDE<br>
  5.2 Download the Dynaxixel2Arduino library<br>
  5.3 Download the OpenCR board manager<br>
  5.4 Connect the OpenCR board to the computer with a USB cable<br>
  5.5 Upload the executable code to the OpenCR board<br>


6. Installation procedure for the computer
  1.1 Install VS Code IDE<br>
  1.2 Download following libraries: <br>
    1.2.1 OpenCV<br>
    1.2.2 Numpy<br>
    1.2.3 pyzbar<br>
    1.2.4 random<br>
    1.2.5 time<br>
    1.2.6 os<br>
    1.2.7 sys<br>
    1.2.8 PyQt5<br>
    1.2.9 cv2<br>
    1.2.10 struct<br>
    1.2.11 serial<br>
  1.3 Connect the computer to the camera with a USB cable<br>
  1.4 Run the file named main.py<br>
  1.5 Enjoy!<br>


# Conclusion
We hope you find this project exciting and informative. If you have any questions or comments, please feel free to reach out to us. Happy building!


    