#Streamonce Inergation Test

This repo is use to test if the streamonce worked about sync discussion between jive and gmail.

### How to run it

```
bash testRunner.sh
```

### Requirements

This Repo is running in python3, can use [ANACONDA](https://www.continuum.io/ managed the python version

After download ANACONDA, should install it with command

```
bash Anaconda3-4.2.0-MacOSX-x86_64.sh
```

use pip to install all the dependency

```
pip install --upgrade selenium requests oauth2client apiclient google-api-python-client imapclient bs4

```

### P.S.

CnCTester1 is group admin

Only CnCTester4 can use alias to send email

### P.P.S.

open Navigator ( installed with anaconda ), create an new virtual env ( eg. so-testing )

activate virtual env using command, and import requirements

```
source activate so-testing
cd $PROJECT_DIR
pip install -r requirements.txt
```
### add config files
accounts.json: it need add accounts.json file, you can download it from team AWS and replace current file.
env.js: the env.js file in team AWS. You need download it and add in project root folder.

### how to debug test
downlaod jupyter;
run: jupyter-notebook .
