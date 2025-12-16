import gi
import time
import threading
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk
layer_indicator = None
layer_label = None

def show(layer):
    print(layer_label)
    layer_label.set_text(layer)
    layer_indicator.show_all()
    print("Mouse?: " + Gdk.device.get_position())
    time.sleep(0.25)

def handle():
    return True
def initialize_indicator():
    global layer_label
    global layer_indicator
    layer_indicator = Gtk.Window()
    layer_indicator.set_resizable(False)
    layer_indicator.set_modal(True)
    layer_indicator.set_accept_focus(False)
    layer_indicator.set_skip_taskbar_hint(True)
    layer_indicator.set_has_window(False)
    layer_indicator.movable=False
    layer_indicator.set_type_hint(Gdk.WindowTypeHint.TOOLTIP)
    layer_indicator.set_default_size(250,180)
    layer_indicator.set_decorated(False)
    container = Gtk.Box()
    layer_label = Gtk.Label()
    container.set_center_widget(layer_label)
    layer_indicator.add(container)


if __name__ == "__main__":
    initialize_indicator()
    t=threading.Thread(target=Gtk.main)
    time.sleep(3)
    show("Test")
    t.daemon= True
    t.start()
    time.sleep(3)
    layer_indicator.hide()


