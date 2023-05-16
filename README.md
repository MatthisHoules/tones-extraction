# Prosody Pipeline

This project is currently under development, please report bugs to Matthis Houlès - matthis.houles@gmail.com

## How to use
### Prerequisites 
- Python - [Official Download link](https://www.python.org/downloads/)

### Installation
```cmd
    git clone https://github.com/MatthisHoules/prosody.git
    cd ./prosody/
    pip install -r requirements.txt
```

### Caution : You need to create a .env file which the following elements
```env
SPPAS_PATH=<sppas_absolute_path>
PYTHON_CMD=<python_cmd>
```

For PYTHON_CMD : python for windows users and generally python3 for linux users

Tested only on Windows

### Use 
```cmd
    python ./main.py <Absolute_path_inputs>
```
