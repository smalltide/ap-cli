# ap-cli
This package provides a command line interface to create, build, deploy AWS Batch Job

### Skills
1. click (Python CLI Framework)
2. boto3 (AWS SDK for Python)

### AP CLI Command
- [x] ap --version
- [x] ap --help
- [ ] ap job create [--name] [--language] (for create a new AP template)
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
  > pip install Click (install Click, Python CLI Framework in venv)
  > pip install boto3 (install boto3, AWS Python SDK in venv)
  > pip install Jinja2 (install Jinja2, Python template Engine in venv)
  > deactivate (if want to leave venv)
```
install developing ap cli package
```
  > pip install --editable .
  > which ap
```

