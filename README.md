# ap-cli
This package provides a command line interface to create, build, deploy AWS Batch Job

### Skills
1. click (Python CLI Framework)
2. boto3 (AWS SDK for Python)


install virtualenv (if need)
```
  > cd ap-cli
  > pip3 install virtualenv
  > virtualenv venv
  > . venv/bin/activate (activate venv)
  > pip install Click (install Click in venv)
  > deactivate (if want to leave venv)
```
install developing ap cli package
```
  > pip install --editable .
  > which ap
  > ap hello --name ice --repeat 5
  > ap hello --name ice --repeat 5 out.txt
```
