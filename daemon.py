#!.venv/bin/python
import sys
import os
import macroboard_driver
import threading
named_pipe="/tmp/tf_pipe"

def main():
    keep_running = True 
    exit() if os.path.exists(named_pipe) else next
    threading.Thread(target=macroboard_driver.start_driver).start()
    os.mkfifo(named_pipe)
    with open(named_pipe) as pipe:
        while True:
            while True:
                if keep_running == False:
                    break
                data = pipe.read() 
                if data.strip() == "end;":
                    keep_running = False
                    macroboard_driver.keep_alive = 0
                if len(data) == 0:
                    break
            if keep_running == False:
                break
    os.system("rm "+named_pipe )


if __name__ == "__main__":
    main()

