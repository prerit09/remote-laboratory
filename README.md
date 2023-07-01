## Remote Lab
Remote Laboratory

#### Prerequisites
You should have python installed on the system.

#### How to run
* Run command 'pip install -r requirements.txt' to initialize the libraries used for these scripts
* Run commnad 'python app.py' which will initialize the database and run the app on ``` localhost:5000 ```

## PYLINT REPORT (STATIC)
pylint C:\Users\PreritJ\Desktop\University\ResearchProject\remote-laboratory  | pylint-json2html -f jsonextended -o reports/statictest.html

# PYTEST REPORT (DYNAMIC)
pytest --html=reports/dynamictest.html --self-contained-html