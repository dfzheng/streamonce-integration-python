#Streamonce Inergation Test

This repo is use to test if the streamonce worked about sync discussion between jive and gmail.

### How to run it

```
bash testRunner.sh
```

### Requirements

### Install pyenv

```
curl -L https://github.com/pyenv/pyenv-installer | bash
```

And the followings to `~/.zshrc`

```
export PATH="~/.pyenv/bin:$PATH"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"
```

And then re-open the terminal.

### Install Python-2.7.13

```
pyenv install 2.7.13
```

### Install virtualenv
```
pip install virtualenv
```

### Create and activate virtual environment

```
virtualenv venv
source venv/bin/activate
```

Then every time when open a new terminal, virtualenv should be activated by
```
source venv/bin/activate
```

Install dependencies in virtual environment
```
pip install -r requirements.txt
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
