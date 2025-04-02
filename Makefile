install:
	@echo "Preparing virtual environment..."
	./venv_install.sh
	@echo "Created app directory '/opt/romopad/'"
	@sudo mkdir /opt/romopad/
	@echo "Copying files..."
	@sudo cp -R * /opt/romopad/
	@sudo cp -R .venv /opt/romopad/
	@sudo rm /opt/romopad/Makefile
	@sudo rm -rf /opt/romopad/__pycache__
	@echo "File copying completed"
	@echo "Adjusting service file"
	@./prepare_service
	@echo "Installing systemd service romopad.service..."
	@sudo mv romopad.service.tmp /etc/systemd/user/romopad.service
	@echo "Installation completed"
uninstall:
	@echo "Checking for files..."
	@if [ -d /opt/romopad ]; then sudo rm -rf /opt/romopad && echo "Files removed"; else echo "No files found"; fi
	@echo "Checking for service..."
	@if [ -f /etc/systemd/user/romopad.service ]; then sudo rm /etc/systemd/user/romopad.service && echo "Removed systemd service"; else echo "No service found"; fi
	@echo "Removal complete."

