## Remote Lab
Remote Laboratory

#### Prerequisites
You should have python and pip installed on the system.

#### How to run
* Run command 'pip install -r requirements.txt' to initialize the libraries used for these scripts
* Run commnad 'python app.py' which will initialize the database and run the app on ``` localhost:5000 ```

## PYLINT REPORT (STATIC)
pylint C:\Users\PreritJ\Desktop\University\ResearchProject\remote-laboratory  | pylint-json2html -f jsonextended -o reports/statictest.html

# PYTEST REPORT (DYNAMIC)
pytest --html=reports/dynamictest.html --self-contained-html

# In case of error in connectivity of the app with Judge0 API update the following file and run the commands
sudo nano /etc/default/grub
GRUB_CMDLINE_LINUX="systemd.unified_cgroup_hierarchy=0"
sudo update-grub
sudo reboot