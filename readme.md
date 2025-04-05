Romoral Macropad driver
===============
<img src="macropad_product.png" width="100%">


Introduction
---------------
So you bought Chinese macropad?
Figured out that not only you have actually no leds, layer functionality and driver is some suspicious sofware, which definitely isn't windows only available chinese spyware, but that it emits useless keys by default? 
Well if so this driver might be for you.
	
This driver utilizes python evdev module to intercept the device and translate the signals.

Scope
---------------
Target device: Romoral factory 12 key macropad<br>
This driver is primarily designed for Linux with platform wayland in mind.
Xorg is untested! This driver may work on Xorg, but was never tested on the Xorg as it's obsolete and will be phased gradually phased out.

Possible caveats
---------------
This driver hooks device based on vendor,product and version ids.<br>
Romoral macropad seems to use identification of <strong>Acer Communications & Multimedia USB Composite Device</strong>.   
Which is quite generic. Some Acer or other devices may share the same ids as this macropad.<br>
So if you have an Acer usb device bear in mind this can conflict with it, if it would happen to have the same ids.

Install
---------------
To install execute following in terminal <strong>[This requires root access]</strong>:

	git clone https://github.com/Sora-3e8/romopad-driver 
	make install
	systemctl --user enable --now romopad.service

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
<h3>/home/$USER/romopad/layout.xml:</h3>

```
<?xml version="1.0" encoding="UTF-8"?>
<layout>
  <static-layer>
      <bind keys="NOB1" type="key">KEY_MUTE</bind>
      <bind keys="NOB1_LT" type="key">KEY_VOLUMEDOWN</bind>
      <bind keys="NOB1_RT" type="key">KEY_VOLUMEUP</bind> 
      <bind keys="NOB2_LT" type="layer_control">prev</bind>
      <bind keys="NOB2_RT" type="layer_control">next</bind>
  </static-layer>
  <!--This layer behaves like numpad-->
  <layer id="0">
      <bind keys="KEY_01" type="key">KEY_NUMLOCK</bind>
      <bind keys="KEY_05" type="key">KEY_KPDOT</bind>
      <bind keys="KEY_09" type="key">KEY_KP0</bind>
      <bind keys="KEY_10" type="key">KEY_KP1</bind>
      <bind keys="KEY_11" type="key">KEY_KP2</bind>
      <bind keys="KEY_12" type="key">KEY_KP3</bind>
      <bind keys="KEY_06" type="key">KEY_KP4</bind>
      <bind keys="KEY_07" type="key">KEY_KP5</bind>
      <bind keys="KEY_08" type="key">KEY_KP6</bind>
      <bind keys="KEY_02" type="key">KEY_KP7</bind>
      <bind keys="KEY_03" type="key">KEY_KP8</bind>
      <bind keys="KEY_04" type="key">KEY_KP9</bind>
  </layer>
  <layer id="AppLauncher">
    <bind keys="KEY_01" type="command">exec nautilus</bind>
    <bind keys="KEY_02" type="command">exec $BROWSER</bind>
    <bind keys="KEY_03" type="command">exec notify-send "Macropad" "$(cowsay 'Moo from your macropad.')"</bind> 
  </layer>
</layout>
```


Capabilities
---------------
Translating key signals coming from the macropad to usable output.
Reimplements layer functionality on software layer with 
following capabilities:
1. Keyboard signals press;release;hold
2. Mouse emulation rel_movement;buttons press;release;hold
3. Executing system commands and starting apps

Security concerns
---------------
Under no circumstances do not run any of the binaries as root.
If you fail to do so layer indicator may crash whole service because it won't be able to access display and you will open your self to pontential privilege escalation vulnerability

Supported signals
---------------
<strong>Supported signals can be found in linux sourcode header: <a href="https://github.com/torvalds/linux/blob/master/include/uapi/linux/input-event-codes.h">Supported signals</a><br></strong>
Please be reasonable, don't expect some weird signals to work. The keyboard and mouse signals shnavoidable issue which comes from the command execution feature.>
It could also be possible to include joystick or gamepad signals, but mapping there is much more complicated due to layout shifting when some features get included,<br> also detection is dependent on hid identification so it does not really make sense to include support for those as many games would not recognize them anyway.

Uninstall
---------------
To remove simply execute:
```
systemctl --user disable --now macroboard_driver.service
sudo make uninstall
```


