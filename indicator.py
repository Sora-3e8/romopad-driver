#!.venv/bin/python
import sys
import tkinter as tk
import time

class indicator:
    @staticmethod
    def show_layer(name):
        global layout
        layout = tk.Tk()
        lbl = tk.Label(layout,bg="#2C2C3B",fg="white", text=name,font="Arial 20")
        lbl.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        layout.configure(bg="#2C2C3B")
        window_width = 250
        window_height = 180
        position_right = int(round(layout.winfo_screenwidth()*0.92,0))
        position_top = int(round(layout.winfo_screenheight()*0.04,0))
        layout.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')
        layout.wm_attributes("-topmost",True)
        layout.wm_attributes("-type", "notification")
        layout.overrideredirect(True)
        layout.wm_attributes("-topmost",True)
        layout.after(800, layout.quit)
        layout.after(800, layout.destroy)
        layout.mainloop()

if __name__ == "__main__":
    indicator.show_layer(sys.argv[1])






