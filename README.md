## Remote Lab
Remote Lab is an online platform that enables users to remotely access and engage in programming activities. It provides a virtual environment where individuals can write, edit, and execute code without the need for local installation or physical hardware. Remote programming labs offer flexibility, allowing users to work on coding projects from any location with an internet connection. They provide a convenient and efficient way to practice coding, collaborate with others, and gain hands-on experience in software development, regardless of physical constraints or hardware limitations. It provides features such as 'Exercise Creation' for the professors so as to grant the students the exercises to work on.

### Prerequisites
Following are the prerequisites that must be present on the system before deploying Remote Lab:
* Python
* Docker
* PIP - Python's Package Management System
* Shell or Bash Client

### Installing Judge0 Code Execution System Client
#### For Windows
* Install Docker for Desktop
* Go to the dependencies directory and execute the following script:
    ``` ./run.sh ```

#### For Linux
* Install docker and docker-componse on the Linux System
* Go to the dependencies directory and execute the following script:
    ``` ./run-linux.sh ```
* In case of error in connectivity of the app with Judge0 API update the following file and run the commands
sudo nano /etc/default/grub
GRUB_CMDLINE_LINUX="systemd.unified_cgroup_hierarchy=0"
sudo update-grub
sudo reboot

### How to run
* Run command 'pip install -r requirements.txt' to initialize the libraries used for the application
* Run commnad 'python app.py' which will initialize the database and run the app on ``` localhost:5000 ```

## Testing

#### Static Code Testing (PYLINT REPORT)
* Run the following command to generate the Static Code Analysis report:
```pylint <<enter_path_to_the_project_root>>  | pylint-json2html -f jsonextended -o reports/statictest.html```
After running the command, the report will be generated in the reports directory.
#### Dynamic Code Testing (PYTEST REPORT)
* Run the following command to generate the Dynamic Code Analysis report:
```pytest --html=reports/dynamictest.html --self-contained-html```
After running the command, the report will be generated in the reports directory.