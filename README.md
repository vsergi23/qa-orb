# qa-orb
Regression test for Orb Project

Used frameworks / libraries:
- pytest
- BDD
- playwright
- Allure Report

# How to use tests
The project use `pytest` as a test runner, and Allure as a report. It uses python version 3.8. The tests use BDD framework
and all tests are described in *.feature files in Gherkin language. To recognize test cases in feature files the project
uses `pytest-bdd` module.
### Local run
It requires a few steps:
- clone from git
- create a virtual environment for python project with python 3.8 and activate it
```commandline
python3 -m venv /path/to/new/virtual/environment
source /path/to/new/virtual/environment/bin/activate
```
- install dependencies (in a folder with the project with the activated virtual environment)
```commandline
pip install -r requirements.txt
```
- run tests
```commandline
pytest -s -v -m "smoke and not login" --browser=chromium --env=dev1 --alluredir=allure_report
```
Where `smoke` and `login` are tags (in pytest it is called marks)  
chromium - browser where tests will be executed, allowed: [chromium, firefox, webkit]  
`dev1` - environment, allowed [`dev1`, `prod`]  
`allure_report` - the name of a folder where will be saved report assets

For playwright debug mode we run tests with the prefix `PWDEBUG=1`
```commandline
PWDEBUG=1 pytest -s -v -m "smoke and not login" --env=dev1 --alluredir=allure_report
```

### To run tests inside Docker container
The project includes folder `ci` with `Dockerfile` and `run.sh`. With these files, there is a possibility to build 
an image and run tests in a container. Steps:
- build a docker container (the command should be executed from the root project folder)
```commandline
docker build -t image-name -f qa-orb/ci/Dockerfile .
```
- run tests
```commandline
docker run --ipc=host image-name -m "smoke" --env=dev1 --browser=chromium --alluredir=allure_report
```