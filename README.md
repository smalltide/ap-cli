# ap-cli
This package provides a command line interface to create, build, deploy AWS Batch Job

### Skills
1. click (Python CLI Framework)
2. boto3 (AWS SDK for Python)

### AP CLI Command
- [x] ap --version
- [x] ap --help
- [x] ap job create [--name] [--language] (for create a new AP template)
- [ ] ap job lint (plan?)
- [ ] ap job build (for AP local build)
- [ ] ap job run (for AP local run)
- [ ] ap job push (plan?)
- [ ] ap job deploy (for deploy AP to Cloud workflow)
- [ ] ap job info (for get AP info)
- [ ] ap job log [--watch] (for retrieve AP log)
- [ ] ap config [subcommand] (for AP CLI config)
- [ ] ap notify [subcommand] (for create AP notify)
- [ ] ap resource [subcommand] (for create aws resource)
- [ ] ap switch [subcommand] (for switch env)


install virtualenv (if need)
```
  > cd ap-cli
  > pip3 install virtualenv
  > virtualenv venv
  > . venv/bin/activate (activate venv)
  > pip install Click (install Click in venv, Python CLI Framework)
  > pip install boto3 (install boto3 in venv, AWS Python SDK)
  > pip install Jinja2 (install Jinja2 in venv, Python template Engine)
  > pip install invoke (install invoke in venv, used for call shell command)
  > deactivate (if want to leave venv)
```
install developing ap cli package
```
  > pip install --editable .
  > which ap
```
install developing ap cli package
```
  > ap job create [-n / --name] ap0001 [-l / --language] python -t [default / tag_name]
  > ap job create -n ap0001 -l python [-t default]
  > ap job create --name ap0001 --language python [--tag default]
```