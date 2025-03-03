#!.venv/bin/python
import sys
import os
import macroboard_driver

named_pipe="/tmp/tf_pipe"

def main():
    keep_running = True 
    exit() if os.path.exists(named_pipe) else next
    macroboard_driver.start_driver()
    
    os.mkfifo(named_pipe)
    with open(named_pipe) as pipe:
        while True:
            while True:
                if keep_running == False:
                    break
                data = pipe.read() 
                if data.strip() == "end;":
                    keep_running = False
                if len(data) == 0:
                    break
            if keep_running == False:
                break


if __name__ == "__main__":
    main()

