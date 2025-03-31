#!.venv/bin/python
import socket as sock
import sys
import os
import macropad_daemon
import threading
sock_dir="/tmp/romopadsvc_control.socket"
keep_sock = True

class NoInit(type):
    def __new__(cls, name, bases, dct):
        # Add custom behavior here
        return super().__new__(cls, name, bases, dct)


# Logical section daemon session
class session():

    @staticmethod
    def stop():
        global keep_sock
        print("Stopping service")
        keep_sock = False
    
    handler={"stop":stop}

    @staticmethod
    def start():
        global keep_sock 
        try:
            intsock = sock.socket(sock.AF_UNIX, sock.SOCK_STREAM)
            intsock.bind(sock_dir)
        except Exception as e:
            print("Creating socket failed with Exception:\n",e)
            exit()

        # Session loop, restarts after session ends
        while keep_sock:
            try:
                intsock.listen(1)
                sock_session, clidress = intsock.accept()
            except Exception as e:
                keep_sock = False
                macropad_daemon.keep_alive = False
                print("Starting daemon listener failed with Exception:\n",e)
                break
            # Data loop, closes upon transfer complete
            while True:
                data = sock_session.recv(1024).decode()
                if data in session.handler:
                    session.handler[data]()
                else:
                    if not data: break
        macropad_daemon.keep_alive = False
        sock_session.close()
        os.unlink(sock_dir) if os.path.exists(sock_dir) else next

    @staticmethod
    def check_if_alive():
        try:
            test_sock = sock.socket(sock.AF_UNIX, sock.SOCK_STREAM)
            test_sock.connect(sock_dir)
            test_sock.close()
        except Exception as e:
            # Checks if connection gets refused
            # If so socket is dead and can be closed
            if e.errno == 111:
                os.unlink(sock_dir)
                return False
            else:
                return True
        return False


    # Enables clear exiting and control over svc daemon
    @staticmethod
    def send_command(cmd):
        if os.path.exists(sock_dir):
            try:
                clisock = sock.socket(sock.AF_UNIX, sock.SOCK_STREAM)
                clisock.connect(sock_dir)
                clisock.send(cmd.encode())
                clisock.close()
            except Exception as e:
                if e.errno == 111:
                    print("Unable to connect, session seems to be dead")
                    print("If service not running remove session lock and restart service:\n",sockdir)
                else:
                    print(e)
        else:
            print("No session found. Is service running?")

# Logical section service
class service():
    service_daemon= None
    # Starts service daemon, checks if no other session is running by checking if there's existing socketfile
    @staticmethod
    def start_svc():
        global keep_sock
        global sock_dir
        keep_sock = True 
        print("Instance already running. Please stop the instance.\n If no active remove the session lock:\n"+sock_dir);exit() if os.path.exists(sock_dir) |os.path.exists(sock_dir) and session.check_if_alive() else threading.Thread(target=session.start).start()
        service_daemon = threading.Thread(target=macropad_daemon.start_driver) 
        service_daemon.daemon = True
        service_daemon.start()
    # Stops service daemon
    @staticmethod
    def stop_svc():
        session.send_command("stop")

    # Argument handler, much more efficient than conditions
    args={"start":start_svc,"stop":stop_svc}
 

class program():
    @staticmethod
    def print_help():
        help_string="""Usage: romopad [--option] value

    Romopad is a python user level macropad driver designed for Romoral 12 key macropad.
    It allows you to rebind your Romoral macropad to emit useful keyboard signals and even execute system commands.
    It's meant as supplement for untrustyworthy Chinese driver, which is otherwise only availabled for Windows.

    Config should be saved in '~/.confing/romopad/layout.xml'
        
    Options:
        --svc       Controls service daemon
        --help      This screen


    --svc:
        romopad --svc [start|stop]
            start       Starts service daemon
            stop        Stops service daemon

        """
        print(help_string)
    start_args={"--svc":service.args,"--help":print_help}

    # Extracts method,args from nested dictionaries using given program args
    # More efficient than million ifs 
    @classmethod
    def extract_method(self,args_in):
        method = program.start_args
        method_args = None
        for arg in args_in: 
            if arg in method:
                method=method[arg]
            else:
                method_args.append(key)
        
        
        return (method,method_args)


if __name__ == "__main__":
    if len(sys.argv)>=2:
        inargs=list(sys.argv[1:])
        args = None
        try:
            method, args = program.extract_method(inargs)

        except Exception as e:
             print("Error unknown argument.")
             program.print_help()
             exit()
        method, args = program.extract_method(inargs)
        if args!=None and len(args)>0:
            print("Got here for some reason...")
            method(*args)
        else:
            method()
    else:
        program.print_help()


