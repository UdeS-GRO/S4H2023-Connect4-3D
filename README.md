# Connect4-3D
Connect4-3D is an exciting project created by students at Sherbrooke University in Quebec, Canada. The goal of the project is to build a robotic arm that can play Connect 4 in 3D against a human. This README file contains information on how to replicate the project and includes links to all the necessary code, CAD files, and installation procedures.

<div style="display:flex; justify-content:center;">
  <a href="https://youtu.be/UQO0S-S_vtE" target="_blank"><img src="http://img.youtube.com/vi/UQO0S-S_vtE/0.jpg" alt="Robot Demonstration" width="720" height="540" border="10" /></a>
</div>


# Project Overview
The project is open source and is licensed under the GNU General Public License v3.0 (GPLv3). The main components of the project are:
<ol>
  <li>The OpenCR board code for controlling the robotic arm </li>
  <li>The computer code for processing the game board and communicating with the OpenCR board </li>
  <li>The CAD files for 3D printing the parts </li>
  <li>A Bill of Materials (BOM) listing all the non-printed materials used </li>
</ol>


### Location of OpenCR Code:
<ol>
  <li>The executable code is named stateMachineAutoOnly_copy_20230308124647 in the folder with the same name</li>
  <li>The file PingMotorsID is pingning all the motors ID connected to the OpenCR board</li>
  <li>The file named ServoReadLive is monitoring the live position of the first and second joint</li>
</ol>

### Location of computer Code:
  <li>Connect_12_PI </li>


### OnShape Link for 3D Printed CADs:
<li>https://cad.onshape.com/documents/92b82e0c23a4517eca2f38d9/w/46a67cc575363ff8875ca5a8/e/41a671f2d443bbba929bd6fb</li>

### List of Non-3D Printed Materials:
  <li>BOM.xlsx</li>

### Installation procedure for the OpenCR board

<ol>
  <li>Install the Arduino IDE</li>
  <li>Download the Dynaxixel2Arduino library</li>
  <li>Download the OpenCR board manager</li>
  <li>Connect the OpenCR board to the computer with a USB cable</li>
  <li>Upload the executable code to the OpenCR board</li>
</ol>



### Installation procedure for the computer
<ol>
  <li>Install VS Code IDE</li>
  <li>Download following libraries: </li>
    <ol>
      <li>OpenCV</li>
      <li>Numpy</li>
      <li>pyzbar</li>
      <li>random</li>
      <li>time</li>
      <li>os</li>
      <li>sys</li>
      <li>PyQt5</li>
      <li>cv2</li>
      <li>struct</li>
      <li>serial</li>
    </ol>
  </li>
  <li>Connect the computer to the camera with a USB cable</li>
  <li>Run the file named main.py</li>
  <li>Enjoy!</li>
</ol>



# Conclusion
We hope you find this project exciting and informative. If you have any questions or comments, please feel free to reach out to us. Happy building!
