This system protytype was build during the COVID-19 pandemic

# Hardware of the project

<img src="readme_src/sideview-prototype.png">

# Real time system prototype testing

<img src="readme_src/usage-example-1.png">


# Guide how to build this project
1. Create virtual environment ```python -m venv env```
2. Run virtual environment activation script ``` /env/Scripts/activate.bat```
3. Run ```setup.py``` to install required dependencies
4. 3D print required parts. (.stl files can be found at ```03_centigrade_CAD``` directory)

![](readme_src/fixture-1-front.png)
![](readme_src/fixture-1-back.png)


![](readme_src/fixture-2-top.png)
![](readme_src/fixture-2-bottom.png)


__Note that the fixtures are adapted to this no-brand webcam from aliexpress:__

<img src="readme_src/webcam.png">

6.  Using the diagram below, make specified connections
```
Pinout for RFID RC522 
3V3 - 3.3V/VCC
GND - GND
 D9 - RST(RESET)
D10 - SDA(SS)
D11 - MOSI
D12 - MISO
D13 - SCK

Pinout for MLX90614 DCI (Infrared Temperature Sensor)
3V3 - VIN/VCC
GND - GND
A4 - SDA
A5 - SCL


Pinout for HC-SR04 (Ultrasonic)
Gnd - GND
Echo - D2
Trig - D3
Vcc - 5V
```


7. Upload ```main.ino``` file to ```Arduino Nano```
8. Connect ```Arduino``` and USB webcam to your local machine and run ```main.py```
