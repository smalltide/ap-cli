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
- [x] ap job build (for AP local build)
- [x] ap job run (for AP local run)
- [ ] ap job deploy (for deploy AP to Cloud workflow)
- [x] ap job info (for get AP info)
- [ ] ap job log [--watch] (for retrieve AP log)
- [ ] ap config [subcommand] (for AP CLI config)
- [ ] ap notify [subcommand] (for create AP notify)
- [ ] ap resource [subcommand] (for create aws resource)
- [ ] ap switch env [--name] (for switch env)


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
  > pip install PyYAML (install PyYAML in venv, used for parse yaml file)
  > deactivate (if want to leave venv)
```
install developing ap cli package
```
  > pip install --editable .
  > which ap
```
Use ap job create command to create ap template
```
  > ap job create [-n / --name] ap0001 [-l / --language] python -t [default / tag_name]
  > ap job create -n ap0001 -l python [-t default]
  > ap job create --name ap0001 --language python [--tag default]
```
Use ap job build command to build ap docker image and dependency lib
```
  > cd ap0001
  > ap job build (in ap project folder)
```
Use ap job run command to run ap locally
```
  > cd ap0001
  > ap job run (in ap project folder)
```
Use ap job info command to get ap information
```
  > cd ap0001
  > ap job info (in ap project folder)
```