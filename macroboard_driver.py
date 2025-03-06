import asyncio
import evdev
import evdev.ecodes as e
import os
import time
import config_loader

keep_alive = 1
supported_devs = [{"vendor":4489,"product":34880,"version":513}]
devnames = [{"name":"Acer Communications & Multimedia USB Composite Device","vendor":4489,"product":34880,"version":513}]
selected_device = None
clayer = 0


def layer_up():
    global clayer
    clayer = clayer + 1
    print(clayer)

def layer_down():
    global clayer
    clayer = clayer - 1
    print(clayer)

commands = {"layer_up":layer_up,"layer_down":layer_down}

def load_capabilities(layout_map):
    key_ev_list = [e.BTN_MOUSE]
    mouse_evs = [e.ABS_X]
    print("Loading keyevents...")
    for layer in layout_map.keys():
        for actions in list(layout_map[layer].values()):
            for key_ev in actions.split("+"):
                if hasattr(e,key_ev):
                    key_ev_list.append( getattr(e,key_ev) )
    print("Key caps:",key_ev_list)
    cap = {e.EV_KEY:key_ev_list}
    print("Capabilities assembled")
    return cap

def start_driver():
    
    # Loads keymapping and all layers from configuration file
    keymap=config_loader.load()

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

    selected_device.grab() 
    cap = load_capabilities(keymap)
    virtual_device = evdev.UInput(cap, name="Macroboard",version=1)
    print("Virtual device created")
    read_loop(keymap,selected_device, virtual_device)

def read_loop(keymap,selected_device, virtual_device):
    # If the device is valid the driver will enter translating phase
    # Virtual device "Macroboard" is created and the translating starts 
    while keep_alive==1:
        event = selected_device.read_one()
        if event != None and event.type == evdev.ecodes.EV_KEY :
            ev = evdev.categorize(event)
            # Checks if any action is defined in keymap 
            print("KEY: ",ev.keycode)
            if ev.keycode in keymap["LAYER"+str(clayer)].keys():
                print("Existing passed")
                for action in keymap["LAYER"+str(clayer)][ev.keycode].split("+"):
                    if action in commands:
                        if ev.event.value == 1:
                            commands[action]() 
                    else: 
                        virtual_device.write(e.EV_KEY,getattr(e,action),ev.event.value)
                        print("Emitting: ",getattr(e,action))
                virtual_device.syn()
                print("Dev sync")
            # Breaks the loop if driver gets stopped
            #if keep_alive == 0:
                #break


                        
    
if __name__ == "__main__":
    main()
