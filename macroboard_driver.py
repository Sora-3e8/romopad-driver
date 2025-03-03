import evdev
import os
import time
import config_loader

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

mouse_controls = ["BTN_LEFT","BTN_RIGHT","BTN_MIDDLE","BTN_SIDE","BTN_EXTRA"]
def start_driver():
    import evdev.ecodes as e
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

    # If the device is valid the driver will enter translating phase
    # Virtual device "Macroboard" is created and the translating starts 
    if selected_device != None:
        selected_device.grab() 
        cap = {e.EV_KEY: [getattr(e,val) for val in layer_map.values() if val not in control_functions ]}
        cap[e.EV_KEY].append(e.BTN_MOUSE)
        virtual_device = evdev.UInput(cap, name="Macroboard",version=1)

        for event in selected_device.read_loop():
            if event.type == evdev.ecodes.EV_KEY:
                ev = evdev.categorize(event)
                if ev.keycode in layer_map: 
                    if layer_map[ev.keycode] in control_functions:
                        if ev.event.value == 1:
                            control_functions[layer_map[ev.keycode]]() 
                    else: 
                        virtual_device.write(e.EV_KEY,getattr(e,layer_map[ev.keycode]),ev.event.value)
                        virtual_device.syn()

            # Breaks the loop if driver gets stopped
            if keep_alive == 0:
                break
                        
    
if __name__ == "__main__":
    main()
