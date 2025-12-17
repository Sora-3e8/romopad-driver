![Header](./macropad_product.png)

Romoral Macropad driver
===============

User-space level driver for remapping of Romoral macropad.<br/>
This driver utilizes python evdev module to intercept the device and translate the signals.

>[!NOTE]
> Romoral macropad uses generic Acer dev id, which may remap other devices with the same id</br>
> This may affect some Acer and generic devices</br>

## 🎯 Scope
- Target device: Romoral factory 12 key macropad
- OS: Linux
- Window servers: Wayland, Xorg (untested)

## Dependencies
 - Python
 - Pip
 - python-evdev (automatically fetched by venv)
 - make

## ✨ Features
- layout layers
- layout layer indicator
- keyboard signals
- mouse signals
- command execution

  
## 📦 Installation
> [!CAUTION]
> Under no circumtances should this program be run with root privileges</br>
> Failing to do so opens you to privilege escalation threat</br>

> [!IMPORTANT]
> Make sure you're in the "input" user group, otherwise the driver won't work.</br></br>
> You can add yourself using following commands:
> - [Arch,Fedora,rhel]: `sudo usermod -aG input $USER`</br>
> - Debian: `sudo useradd -a G input $USER`

To install execute following commands:

```bash
$ git clone https://github.com/Sora-3e8/romopad-driver
$ cd romopad-driver
$ sudo make install
$ systemctl --user daemon-reload
$ systemctl --user enable --now romopad.service
```

## 🐞 Known issues
- In some environments the layer indicator may not show up, this is an issue caused by systemd not being able to pass the display variable as it was not set yet
- This occurs for example in wm managers as it's impossible to tell if session has already started
- The usual quick fix is to restart the service after logging into session:<br/>
  ```bash
  $ systemctl --user restart romopad.service
  ```
- For this reason it's highly recommended for wm manager sessions, to start the service using the wm itself
- Example Hyprland: `exec-once = systemctl --user start romopad.service`

- The indicator now depends on the Xorg due to Tkinter being dependent, currently there're plans to replace it with Gtk4
  however that's still a bit far, but it will be needed to be done as Xorg is being phased out
- This may affect users on Niri which does not directly use XWayland, but the xwayland-satellite 


## 🔧 Configuration
The configuration uses xml format, where you define in each layer and binds, the parent node is <layout> and is mandatory along side with at least one layer.
Remapping is split into layers where unique identifier is to be used for each layer.


### Layer types:
 - `<layer>` - Defines layer to which you can switch using `layer_control`, mandatory attribute `id`, id can be any text or number
 - `<static-layer>` - Only one should be defined, but if it happens more than one is defined, the last one will be used, this bind layer is static from the name,<br/>the keybinds here will work across layers eg. layer switching action should be defined here

### Bind types:
`<bind>` - Mandatory attribute `keys` and `type`

#### Attributes:
- keys - This attribute binds action to physical key on the device, check reference image in section Device layout<br/>
- type - There are 3 possible values `key|command|layer_control`<br/>
  - key - Maps key from keys attribute to keycode inside bind tag example:<br/> `<bind keys="KEY_01" type="key">KEY_NUMLOCK</bind>`<br/>
  - command - Maps key to trigger shell command in inside bind tag example:<br/>  `<bind keys="KEY_03" type="command">exec notify-send "Macropad" "Hello from your macropad!"</bind>`<br/>
  - layer_control - Maps key from keys attribute to switch layers possible values `prev|next` example:<br/> `<bind keys="NOB2_LT" type="layer_control">prev</bind>`<br/>

<strong>Supported keycodes can be found in linux sourcode header: <a href="https://github.com/torvalds/linux/blob/master/include/uapi/linux/input-event-codes.h">Supported signals</a><br></strong>

#### Configuration

Configuration path: `~/.config/romopad/layout.xml`
On install the initial configuration as a numpad is copied into current user's config path.

Example configuration `layout.xml`:
```xml
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

## Device layout
  <img src="macroboard_map.png" width=720>

## Uninstall
To remove execute as root:
```bash
$ systemctl --user disable --now macroboard_driver.service
$ sudo make uninstall
```
