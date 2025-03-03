import os
import configparser
CONFIG_PATH = "/etc/macroboard/"
CONF_FNAME = "layout.conf"

default_config=
""" 
[LAYER0]
KEY_01=NUM_LOCK
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
NOB_RT=layer_up
NOB_LT=layer_down
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
             "NOB1_PR": "KEY_2",
             "NOB1": "KEY_3",
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
    except Exception e:
        print(str(e))
        print("Could not write ...")
        print("Loading hardcoded preconf")            


    
def translate(config, transl):
    translated_map={}
    for key in config.keys():
        for subkey in key.keys():
            translated_map[key][transl[subkey]]=config[key][subkey]

    

def load():
    config_obj=configparser.ConfigParser()
    if os.path.isfile(CONFIG_PATH+CONF_FNAME):
        try:
            config.read("")
        except Exception e:
            print("Loading config encountered error:")
            print(str(e))
            exit()
    else:
        print("Could not load configuration, generating default...")
        generate_default()
        config_obj.read_string(default_config)

    translated_map = translate(config_obj._dict,hwtrans_layer)

return translated_map 


