![Header](./macropad_product.png)
Romoral Macropad driver
===============

User-space level driver for remapping of Romoral macropad.
This driver utilizes python evdev module to intercept the device and translate the signals.

Dependencies
---------------
  Python
  python-evdev (automatically fetched by venv)
  make
  pip

🎯 Scope
---------------
- Target device: Romoral factory 12 key macropad
- OS: Linux
- Window servers: Wayland, Xorg (untested)

# ✨ Features
- layout layers
- keyboard signals
- mouse signals
- command execution

# ⚠️  Cautions to Note
- Romoral macropad uses generic id, which may inadvertently remap other generic devices sharing the same id,<br>including some Acer devices
- Under no circumstances should the program be run with root privileges.<br/>

📦 Install
---------------
To install execute following in terminal <strong>[This requires root access]</strong>:

	git clone https://github.com/Sora-3e8/romopad-driver 
	make install
	systemctl --user enable --now romopad.service

# 🔧 Configuration
The configuration uses xml format, where you define in each layer and binds, the parent node is <layout> and is mandatory along side with at least one layer.
Remapping is split into layers where unique identifier is to be used for each layer.

### Layer types:
 - `<layer>` - Defines layer to which you can switch using `layer_control`, mandatory attribute `id`, id can be any text or number
 - `<static-layer>` - Only one should be defined, but if it happens more than one is defined, the last one will be used, this bind layer is static from the name,<br/>the keybinds here will work across layers eg. layer switching action should be defined here

### Bind types:
`<bind>` - Mandatory attribute `keys` and `type`

#### Attributes:
- keys - This attribute binds action to physical key on the device, check reference image in section Device layout
- type - There 3 possible values key|command|layer_control
  - key - Maps key from keys attribute to keycode inside bind tag example: `<bind keys="KEY_01" type="key">KEY_NUMLOCK</bind>`
  - command - Maps key to trigger shell command in inside bind tag exaample:  `<bind keys="KEY_03" type="command">exec notify-send "Macropad" "Hello from your macropad!"</bind>`
  - layer_control - Maps key from keys attribute to switch layers possible values `prev` or `next` example: `<bind keys="NOB2_LT" type="layer_control">prev</bind>`

<strong>Supported keycodes can be found in linux sourcode header: <a href="https://github.com/torvalds/linux/blob/master/include/uapi/linux/input-event-codes.h">Supported signals</a><br></strong>

Config example:

`~/.config/romopad/layout.xml`:</h3>

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

Device layout
---------------
The key map of the physical device to configuration names described in the image below:
<img src="macroboard_map.png" width=720>

Uninstall
---------------
To remove simply execute:
```
systemctl --user disable --now macroboard_driver.service
sudo make uninstall
```


