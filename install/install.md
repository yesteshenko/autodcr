# Installation

## Manual Installation

In order to manually install AutoDCR you'll need [Python] installed on your
system, as well as the Python package manager, [pip]. You can check if you have
these already installed from the command line:

```bash
$ python --version
Python 2.7.14
$ pip --version
pip 18.1 from /usr/local/lib/python2.7/site-packages/pip (python 2.7)
```
### Installing Python

Install [Python] by downloading an installer appropriate for your system from
[python.org] and running it.

!!! Note

    If you are installing Python on Windows, be sure to check the box to have
    Python added to your PATH if the installer offers such an option (it's
    normally off by default).

    ![Add Python to PATH](img/win-py-install.png)

[python.org]: https://www.python.org/downloads/

### Installing pip

If you're using a recent version of Python, the Python package manager, [pip],
is most likely installed by default. However, you may need to upgrade pip to the
lasted version:

```bash
pip install --upgrade pip
```

If you need to install [pip] for the first time, download [get-pip.py].
Then run the following command to install it:

```bash
python get-pip.py
```

### Installing git

```bash
yum install git
```

## Getting Started

### Work in virtualenv

create virtualenv
```mkvirtualenv AutoDCR```

enter to virtualenv
```workon AutoDCR```

exit from virtualenv
```deactivate```

### Installing AutoDCR

Using GIT:

```
bash
cd /opt
git clone https://github.com/yesteshenko/autodcr.git
```

Only download:

```
svn checkout https://github.com/yesteshenko/autodcr/trunk
```

Or manual copy project to directory

```
bash
cd /opt
mkdir autodcr
```

Install TextFSM templates

```
cd /opt/autodcr
svn checkout https://github.com/networktocode/ntc-templates/trunk/templates
```

#### Install additional lib (in system or virtualenv):

Complex:

```pip install -r install/requirements.txt```

Separetly:

```
pip install netmiko
pip install tabulate
pip install ConfigParser
pip install python-docx
pip install openpyxl
pip install PyYAML
pip install Flask
```

Change the access permissions, exec in directory of installations AutoDCR
```
chmod -R 755 *.py
chmod -R 755 ./utils/*.py
```

#### optional (sometimes need):

```
pip install --upgrade pip setuptools
yum install libxslt-devel libxml2-devel
```
----
    
[Home](../README.md)

[Python]: https://www.python.org/
[get-pip.py]: https://bootstrap.pypa.io/get-pip.py
[pip]: https://pip.readthedocs.io/en/stable/installing/