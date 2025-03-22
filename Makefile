install:
	./venv_install.sh
	sudo mkdir /opt/romopad/
	sudo cp -r .venv /opt/romopad/
	sudo cp *.py /opt/romopad/
	sudo cp romopad.service /etc/systemd/user/

unistall:
	rm -rf /opt/romopad
	rm /etc/systemd/user/romopad.service

