import os
import configparser
CONFIG_PATH = "/etc/macroboard/"
CONF_FNAME = "layout.conf"

default_config=""" 
[LAYER0]
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
"""

# This cannot be changed by user => Translates easy to understand keynames to signal codes emitted by device, used to translate user 
# hardware layout names to emitted signals names see: macroboard_map.png
hwtrans_layer = { 
             "KEY_01": "KEY_A",
             "KEY_02": "KEY_B",
             "KEY_03": "KEY_C",
             "KEY_04": "KEY_D",
             "KEY_05": "KEY_E",
             "KEY_06": "KEY_F",
             "KEY_07": "KEY_G",
             "KEY_08": "KEY_H",
             "KEY_09": "KEY_I",
             "KEY_10": "KEY_J",
             "KEY_11": "KEY_K",
             "KEY_12": "KEY_L",
             "NOB1_LT": "KEY_1",
             "NOB1": "KEY_2",
             "NOB1_RT": "KEY_3",
             "NOB2_LT": "KEY_4",
             "NOB2": "KEY_5",
             "NOB2_RT": "KEY_6",
             }

# Can be set by user, but this is default
# NOB_1 left, right by default controls layer

# Writes default config if it does not exist for some reason
def generate_default():
    try:
        if not os.path.exists(CONFIG_PATH):
            os.makedirs(CONFIG_PATH)
        with open(CONFIG_PATH+CONF_FNAME,"w") as f:
            f.write(default_config)
    
    # Mainly catches permissions issue
    except Exception as e:
        print(str(e))
        print("Could not write ...")
        print("Loading hardcoded preconf")            


    
def translate(config, transl):
    translated_map={}
    for layer in list(config.keys()):
        if layer == "DEFAULT":
            next
        translated_map[layer.upper()]={}
        print("Translation keys:",list(config[layer].keys()))
        for key in list(config[layer].keys()):
            translated_map[ layer.upper() ][ transl[key.upper()] ] = config[layer][key]
    return translated_map

    

def load():
    config_obj=configparser.ConfigParser()
    if os.path.isfile(CONFIG_PATH+CONF_FNAME):
        try:
            config_obj.read(CONFIG_PATH+CONF_FNAME)
        except Exception as e:
            print("Loading config encountered error:")
            print(str(e))
            exit()
    else:
        print("Could not load configuration, generating default...")
        generate_default()
        config_obj.read_string(default_config)
        print("Dict: ",list(dict(config_obj)["LAYER0"].keys()))
    print(list(config_obj["LAYER0"].keys()))
    translated_map = translate(dict(config_obj),hwtrans_layer)
    return translated_map 


