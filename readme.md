Romoral Macropad driver
===============
<img src="macropad_product.png" width=720 height=480>


Introduction
---------------
So you bought Chinese macropad?
Figured out that not only you have actually no leds, layer functionality and driver is some suspicious sofware, which definitely isn't windows only available chinese spyware, but that it emits useless keys by default? 
Well if so this driver might be for you.
	
This driver utilizes python evdev module to intercept the device and translate the signals.

Scope
---------------
Target device: Romoral factory 12 key macropad<br>
This driver is primarily designed for Linux with platform wayland.

Possible caveats
---------------
This driver hooks device based on vendor,product and version ids.<br>
Romoral macropad seems to use identification of <strong>Acer Communications & Multimedia USB Composite Device</strong>.   
Which is quite generic. Some Acer or other devices may share the same ids as this macropad.<br>
So if you have an Acer usb device bear in mind this can conflict with it, if it would happen to have the same ids.

Install
---------------
To install execute following in terminal <strong>[This requires root access]</strong>:

	git clone 
	make
	make install
	sudo systemctl enable --now macroboard_driver.service


Requirements
---------------
	make
	Python
	pip 

Device layout
---------------
The key map of the physical device to configuration names described in the image below:

<img src="macroboard_map.png" width=720>

Configuration
---------------
<h3>/etc/macroboard/layout.conf:</h3>

```
#This layer will imitate numpad now 
KEY_01=KEY_NUMLOCK
KEY_05=KEY_KPDOT
KEY_09=KEY_KP0
KEY_10=KEY_KP1
KEY_11=KEY_KP2
KEY_12=KEY_KP3
KEY_06=KEY_KP4
KEY_07=KEY_KP5
KEY_08=KEY_KP6
KEY_02=KEY_KP7
KEY_03=KEY_KP8
KEY_04=KEY_KP9
NOB1_RT=layer_up
NOB1_LT=layer_down
```


Capabilities
---------------
Translating key signals coming from the macropad to usable output.
Reimplements layer functionality on software layer with 
following capabilities:
1. Keyboard signals press;release;hold
2. Mouse emulation rel_movement;buttons press;release;hold
3. Executing system commands and starting apps

Supported signals
---------------
<strong>Supported signals can be found in linux sourcode header: <a href="https://github.com/torvalds/linux/blob/master/include/uapi/linux/input-event-codes.h">Supported signals</a><br></strong>
Please be reasonable, don't expect some weird signals to work. The keyboard and mouse signals should all work.<br>
It could also be possible to include joystick or gamepad signals, but mapping there is much more complicated due to layout shifting when some features get included,<br> also detection is dependent on hid identification so it does not really make sense to include support for those as many games would not recognize them anyway.

Uninstall
---------------
To remove simply execute:
```
sudo systemctl disable --now macroboard_driver.service
make uninstall
```


