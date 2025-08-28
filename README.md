# MRSGEN
---
A simple morse code generator for translating from english to morse. Uses pygame to generate tones from an array representing a sine wave and PyGObject Gtk 4 bindings for the ui. A simple python dictionary is used for the translation from the input text buffer to the output text buffer.  

The Following install guide assumes you are running linux (either arch or a debian/ubuntu distro) and have python installed already. If you are running another linux distro it will likely work just by substituting in your package manager and modifying commands but do so at your own peril.    

![MRSGEN](image/mrsgen.png)

---
# Dependencies
*Versions are based on my setup, your mileage may vary*
- python 3.13+ 
- PyGObject 3.52.3+
- pygame 2.6.1+
- numpy 2.3.2+
- pycairo 1.28+ --> Not directly used but included to be safe. 
- Gtk 4 introspection packages 
---
# Install with uv
### Install uv
If not already installed use the following to install uv for python so you can keep the dependencies from polluting your system. 
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Verify installation
This should print `uv <version_number date of version>` if the installation was succesful. If this fails simply retry the curl command above and retry.  
```bash
uv self version
```

### Move to directory
Move into the directory you want to clone the repo into.
```bash
cd path/to/directory
```

### Clone the repo
This will create a 'mrsgen' directory in your current directory
```bash
git clone https://github.com/jdfincher/mrsgen
```

Move into mrsgen directory
```bash
cd mrsgen
```

### Initialize uv venv
This will create the virtual environment in your current directory
```bash
uv venv
```

Then activate the venv with the following
```bash
source .venv/bin/activate
```

### Include System Packages
Include your already installed system packages in the venv by navigating to the **.venv** directory and edit the **pyvenv.cfg** file in a text editor like nvim or whatever you prefer.
```bash
cd .venv
nvim pyvenv.cfg
```

Change the below line 
```cfg
include-system-site-packages = false 
```

to the following and save/close the file. 
```cfg
include-system-site-packages = true
```
### Check sys packages
Now you need to verify the needed gtk4 introspection packages are present. It is important to do this before syncing the python dependencies to ensure a proper build of the venv. In another terminal window run the following command for your distro. 
#### Arch 
```bash
pacman -Qs '^gtk4$|^gobject-introspection$|^python(-|)gobject' >/dev/null \
&& echo "GTK4 introspection packages are installed." \
|| echo "GTK4 introspection packages are NOT installed."
```
#### Debian/Ubuntu
```bash
dpkg -s libgtk-4-dev gir1.2-gtk-4.0 python3-gi python3-gi-cairo >/dev/null 2>&1 \
&& echo "GTK4 introspection packages are installed." \
|| echo "GTK4 introspection packages are NOT installed."
```

If the command returned NOT installed update your package list and install the Gtk4 introspection packages with the following command. After installation rerun the above command to ensure the installation worked successfully. 
#### Arch
```bash
sudo pacman -Syu --needed gtk4 gobject-introspection python-gobject
```
#### Debian/Ubuntu
```bash
sudo apt update
sudo apt install -y libgtk-4-dev gir1.2-gtk-4.0 python3-gi python3-gi-cairo
```

### Sync dependencies
The last step is syncing the uv venv dependencies. Move back to the terminal window you initialized the venv in and run the following to download the packages into the venv.
```bash
uv sync
```

### Run the App
Run the application with the following from mrsgen directory inside the venv. 
```bash
./main.sh
```

To rerun the app after you have closed the venv you will need to reactivate the venv by running the following command inside the mrsgen directory and then the above command. 
```bash
source .venv/bin/activate
```

If you get a permission error when running the `./main.sh` command simple run the below to change the files permissions. 
```bash
chmod 751 main.sh
```

*Thanks for checking out my silly app!*
