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

### fill config files
* accounts.json: credential information for test user accounts. you can get more info in AWS/S3/tw-jive-config/streamonce-automation-test
* env.json: environment configuration file. you can get more info in AWS/S3/tw-jive-config/streamonce-automation-test
* streamonce-testing-c911366674f7.json: google api authorization private key file. you can get more info in AWS/S3/tw-jive-config/streamonce-automation-test

### how to debug test
download jupyter;
run:
```jupyter-notebook .```
