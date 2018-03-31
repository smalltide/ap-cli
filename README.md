# ap-cli
This package provides a command line interface to create, build, deploy AWS Batch Job

### Skills
1. click (Python CLI Framework)
2. boto3 (AWS SDK for Python)
3. Jinja2 (Python Template Engine)
4. invoke (Python Call Shell Command)
5. ruamel.yaml (Python Parse Yaml) 

### AP CLI Command
- [x] ap --version
- [x] ap --help
- [x] ap job create [--name] [--language] (for create a new AP template)
- [x] ap job init [--name] [--language] (for generate AP template in existing folder)
- [x] ap job build (for AP local build)
- [x] ap job run (for AP local run)
- [x] ap job deploy (for deploy AP to Cloud workflow)
- [x] ap job info (for get AP info)
- [ ] ap job log [--date?] [--job-id] [--limit] [--tail] (for retrieve AP log)
- [x] ap config aws (for AP AWS CLI config)
- [x] ap config github (for Link AP to GitHub Repository)
- [x] ap notify slack (for create AP notify)
- [x] ap switch env [--name] (for switch target deploy environment)
- [ ] ap resource [subcommand] (for create aws resource, plan?)

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
  > pip install ruamel.yaml (install uamel.yaml in venv, used for parse yaml file)
  > deactivate (if want to leave venv)
```
install developing ap cli package
```
  > pip install --editable .
  > which ap
```
Use ap job create command to create ap template
```
  > ap job create [-n / --name] ap0001 [-l / --language] python [-t / --tag] (default / tag_name)
  > ap job create -n ap0001 -l python [-t default]
  > ap job create --name ap0001 --language python [--tag default]
```
Use ap job init command to generate AP template in existing folder
```
  > cd existing_folder
  > ap job init [-n / --name] ap0001 [-l / --language] python [-t / --tag] (default / tag_name)
  > ap job init -n ap0001 -l python [-t default]
  > ap job init --name ap0001 --language python [--tag default]
```
Use ap job build command to build ap docker image and dependency lib
```
  > cd ap0001
  > ap job build
```
Use ap job run command to run ap locally
```
  > cd ap0001
  > ap job run
```
Use ap job deploy command deploy ap job
```
  > cd ap0001
  > ap job deploy
  > ap job deploy --auto-push-message "ap0001 init" (auto push commit to github)
```
Use ap job info command to get ap information
```
  > cd ap0001
  > ap job info
```
Use ap job log command to get ap logs
```
  > cd ap0001
  > ap job log
  > ap job log [-l / --limit] 3
  > ap job log [-j / --job-id] xxxx-xxxx-xxxx-xxxx
  > ap job log [-j / --job-id] xxxx-xxxx-xxxx-xxxx [-t / --tail] 100
  > ap job log [-l / --limit] 3 [-t / --tail] 100
  > ap job log [-l / --limit] 1 [-t / --tail] 100
```
Use ap config aws command to Set AWS Environment Parameters
```
  > cd ap0001
  > ap config aws [-p / --profile] (dev / stg /prod)
  > ap config aws
  > ap config aws -p dev
  > ap config aws --profile dev
  > ap config aws -p stg
  > ap config aws --profile stg
  > ap config aws -p prod
  > ap config aws --profile prod
```
Use ap config github command to Link AP to GitHub Repository
```
  > cd ap0001
  > ap config github [-a / --account] (github account) [-r / --repository] (repository name)
  > ap config github -r ap0001
  > ap config github --repository ap0001
  > ap config github -a 104corp -r ap0001 
  > ap config github --account 104corp --repository ap0001 
```
Use ap notify slack command to add Slack Notify
```
  > cd ap0001
  > ap notify slack [-s / --source] (trigger source) [-a / --account] (slack account) [-t / --token] (slack travis token) [-c / --channel] (slack channel)
  > ap notify slack --source travis --token access_token --channel ap-build
  > ap notify slack --token access_token --channel ap-build
  > ap notify slack -t access_token -c ap-build
```
Use ap switch env command to switch Target Deploy Environment
```
  > cd ap0001
  > ap switch env [-p / --profile] (dev / stg /prod)
  > ap switch env
  > ap switch env -p dev
  > ap switch env --profile dev
  > ap switch env -p stg
  > ap switch env --profile stg
  > ap switch env -p prod
  > ap switch env --profile prod
```