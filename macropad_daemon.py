import asyncio
import evdev
import evdev.ecodes as e
import os
import subprocess as sp
import time
import config_loader
import threading
from indicator import indicator as layer_indicator
keep_alive = 1
supported_devs = [{"vendor":4489,"product":34880,"version":513}]
devnames = [{"name":"Acer Communications & Multimedia USB Composite Device","vendor":4489,"product":34880,"version":513}]
selected_device = None
clayer = "0"

# This cannot be changed by user => Translates easy to understand keynames to signal codes emitted by device, used to translate user 
# hardware layout names to emitted signals names see: macroboard_map.png

hwtrans_layer = {
 "KEY_A":"KEY_01",
 "KEY_B":"KEY_02",
 "KEY_C":"KEY_03",
 "KEY_D":"KEY_04",
 "KEY_E":"KEY_05",
 "KEY_F":"KEY_06",
 "KEY_G":"KEY_07",
 "KEY_H":"KEY_08",
 "KEY_I":"KEY_09",
 "KEY_J":"KEY_10",
 "KEY_K":"KEY_11",
 "KEY_L":"KEY_12",
 "KEY_1":"NOB1_LT",
 "KEY_2":"NOB1",
 "KEY_3":"NOB1_RT",
 "KEY_4":"NOB2_LT",
 "KEY_5":"NOB2",
 "KEY_6":"NOB2_RT",
}

def layer_control(virtual_device,arg,key_value):
    global clayers
    global clayer

    if key_value == 0 and arg == "next":
        print("Switching to next layer")
        if clayers.index(clayer)+1 > (len(clayers)-1):
            clayer = clayers[0]
        else:
            clayer=clayers[clayers.index(clayer)+1]

    if key_value == 0 and arg == "prev":
        print("Switching to next layer")
        if clayers.index(clayer)-1 > 0:
            clayer = clayers[len(layers)-1]
        else:
            clayer=clayers[clayers.index(clayer)-1]
    if key_value == 0:
        os.system("./indicator.py "+str(clayer)) 

def load_capabilities(layout_map):
    key_ev_list = [e.BTN_MOUSE]
    mouse_evs = [e.ABS_X]
    print("Loading keyevents...")
    
    for bind in layout_map["global"].keys():
        if layout_map["global"][bind]["type"] == "key":
            if "+" in layout_map["global"][bind]["args"]:
                for key in layout_map["global"][bind]["args"].split("+"):
                    if hasattr(e, key) and getattr(e,key) not in key_ev_list:
                        key_ev_list.append(e.key)
            else:
                if hasattr(e, layout_map["global"][bind]["args"]) and getattr(e,layout_map["global"][bind]["args"]) not in key_ev_list:
                    key_ev_list.append(getattr(e,layout_map["global"][bind]["args"]))

    for layer in layout_map["layers"].keys():
        for bind in layout_map["layers"][layer].keys():
            if layout_map["layers"][layer][bind]["type"] == "key":
                if "+" in layout_map["layers"][layer][bind]["args"]:
                    for key in layout_map["layers"][layer][bind]["args"].split("+"):
                        if hasattr(e, key) and getattr(e,key) not in key_ev_list:
                            key_ev_list.append( getattr(e,key) )
                else:
                    if hasattr(e, layout_map["layers"][layer][bind]["args"]) and getattr(e,layout_map["layers"][layer][bind]["args"]) not in key_ev_list:
                        key_ev_list.append(getattr(e,layout_map["layers"][layer][bind]["args"]))

    print("Key caps:",key_ev_list)
    cap = {e.EV_KEY:key_ev_list}
    print("Capabilities assembled")
    return cap

def trigg_key_event(virtual_device,keys,value):
    # Handles multi key bind
    if "+" in keys:
        needs_update = False
        for key in keys.split("+"):
            if hasattr(e,k):
                needs_update = True
                virtual_device.write(e.EV_KEY,getattr(e,k),value)
        if needs_update:
            virtual_device.syn()
    
    # If single key bound
    else:
        if hasattr(e, keys):
            virtual_device.write(e.EV_KEY,getattr(e,keys),value)
            virtual_device.syn()

def unix_command(virtual_device,arg,key_value):
    if key_value == 0 or key_value == 2:
        #os.spawnve(os.P_NOWAIT,arg.split(" ")[0],arg.split(" ")[1:],os.environ)
        sp.Popen(arg,shell=True,stdout=sp.DEVNULL,start_new_session=True)

EVENT_HANDLER = {"layer_control":layer_control,"key":trigg_key_event, "command":unix_command}
def start_driver():
    global keymap
    global clayers

    # Loads keymapping and all layers from configuration file
    keymap=config_loader.load()
    clayers = list(keymap["layers"].keys()) 
    selected_device = None
    # Repeats until target device is found and selected
    while selected_device == None:
        # Loads available devices
        devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
        # Loops through available devices until it finds 
        for device in devices:
            devinfo = device.info
            # Checks if the device is the targeted by the driver and preloads it into indev
            if {"vendor":devinfo.vendor,"product":devinfo.product,"version":devinfo.version} in supported_devs: 
                indev = evdev.device.InputDevice(device)
                # As the target device has two nodes one with ABS capabilities, the abs supporting device is selected
                if ("EV_ABS",3) in indev.capabilities(verbose=True):
                    selected_device = indev
        # Delays repetition by 3 secs to avoid overload
        time.sleep(3)
    for val in dir(selected_device):
        print(val)

    selected_device.grab() 
    cap = load_capabilities(keymap)
    virtual_device = evdev.UInput(cap, name="Macroboard",version=1)
    print("Virtual device created")
    read_loop(keymap,selected_device, virtual_device)

def read_loop(keymap,selected_device, virtual_device):
    global clayer
    # If the device is valid the driver will enter translating phase
    # Virtual device "Macroboard" is created and the translating starts 
    while True:
        dev_events = None
        try:
            dev_events=selected_device.async_read_loop()
        except Exception as e:
            print("Dev Path:",selected_device.path)
        if dev_events != None:
            for event in dev_events:
                if event != None and event.type == evdev.ecodes.EV_KEY :
                    ev = evdev.categorize(event)
                    if hwtrans_layer[ev.keycode] in keymap["global"]:
                        ev_type = keymap["global"][hwtrans_layer[ev.keycode]]["type"]
                        ev_arg = keymap["global"][hwtrans_layer[ev.keycode]]["args"]
                        EVENT_HANDLER[ev_type](virtual_device,ev_arg,ev.event.value)
                    else:
                        if hwtrans_layer[ev.keycode] in keymap["layers"][clayer]: 
                            ev_type = keymap["layers"][clayer][hwtrans_layer[ev.keycode]]["type"]
                            ev_arg = keymap["layers"][clayer][hwtrans_layer[ev.keycode]]["args"]
                            EVENT_HANDLER[ev_type](virtual_device,ev_arg,ev.event.value)
                 
    
if __name__ == "__main__":
    main()
