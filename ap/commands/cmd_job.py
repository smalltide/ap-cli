import click
import os
import time
import boto3
from boto3.dynamodb.conditions import Key, Attr

from invoke import run as run_command
from ap.utils import generate_ap_job, is_ap, is_text_in_file, str_from_timestamp
from ap.cli import pass_context


@click.group()
@click.pass_context
def cli(ctx):
    """Job create, build, run, deploy, info, log"""
    if ctx.invoked_subcommand not in ('create', 'init'):
        is_ap(ctx.obj.configs)


@cli.command()
@click.option('-n', '--name', required=True, help='AP Name or Number')
@click.option('-l', '--language', required=True, help='AP Template Language')
@click.option('-t', '--tag', default='default', help='AP Language Tag')
@pass_context
def create(ctx, name, language, tag):
    """Create a AP Job Template"""
    home, templates = ctx.home, ctx.templates

    target = os.path.join(home, name)
    if os.path.exists(target):
        raise click.ClickException(
            f'Existing {name} directory here, please run create command for another name!'
        )

    template = os.path.join(templates, 'job', language, tag)
    if not os.path.exists(template):
        raise click.ClickException(
            f'The template not exists, please choose right language and tag of template'
        )

    parameters = {'name': name, 'type': 'job'}
    generate_ap_job(target, template, parameters)


@cli.command()
@click.option('-n', '--name', required=True, help='AP Name or Number')
@click.option('-l', '--language', required=True, help='AP Template Language')
@click.option('-t', '--tag', default='default', help='AP Language Tag')
@pass_context
def init(ctx, name, language, tag):
    """Initial a AP Job Template in Existing Folder"""
    home, templates = ctx.home, ctx.templates

    ap_config = os.path.join(home, '.ap.yml')
    if os.path.isfile(ap_config):
        raise click.ClickException(
            f'Existing AP template, please run init command for an empty folder!'
        )

    template = os.path.join(templates, 'job', language, tag)
    if not os.path.exists(template):
        raise click.ClickException(
            f'The template not exists, please choose right language and tag of template'
        )

    parameters = {'name': name, 'type': 'job'}
    generate_ap_job(home, template, parameters)


@cli.command()
@pass_context
def build(ctx):
    """Build AP Job Docker Image"""
    name = ctx.configs["name"]

    cmd = f'docker image rm ap/{name}'
    result = run_command(cmd, warn=True)
    cmd = f'docker build -t ap/{name} .'
    result = run_command(cmd, warn=True)
    if result.ok:
        click.secho(f'Build AP Successful', fg='green', bold=True)
    else:
        click.secho(f'Build AP Failure', fg='red', bold=True)


@cli.command()
@pass_context
def run(ctx):
    """Run AP Job on Local"""
    home, name, app_path, environment = ctx.home, ctx.configs[
        'name'], ctx.configs['app_path'], ctx.configs['environment']
    aws_folder = click.get_app_dir('aws', force_posix=True)

    cmd = f'docker run -e HOME=/home -e AWS_PROFILE={environment} -v {home}/app:{app_path} -v {aws_folder}:/home/.aws --rm ap/{name}'
    result = run_command(cmd, warn=True)
    if result.ok:
        click.secho(f'Run AP Successful', fg='green', bold=True)
    else:
        click.secho(f'Run AP Failure', fg='red', bold=True)


@cli.command()
@click.option(
    '-p', '--auto-push-message', default=None, help='Auto Push with Message')
@pass_context
def deploy(ctx, auto_push_message):
    """Trigger AP Job Travis CI/CD Flow on Cloud"""
    name, environment = ctx.configs['name'], ctx.configs['environment']
    job_env = environment.split('-')[-1]

    aws_folder = click.get_app_dir('aws', force_posix=True)
    aws_config = os.path.join(aws_folder, 'config')

    is_environment_config = is_text_in_file(environment, aws_config)

    if not is_environment_config:
        click.secho(
            f'Profile {environment} not exists in AWS CLI Config File',
            fg='green',
            bold=True)
        click.secho(
            f'You can use [ap config aws] command to add {environment} Profile in Config',
            fg='green',
            bold=True)
    else:
        session = boto3.Session(profile_name=environment)
        region = session.region_name
        access_key = session.get_credentials().access_key
        secret_key = session.get_credentials().secret_key

        cmd = f'travis encrypt AP_NAME={name} AWS_ACCOUNT_ID={ctx.job_env[job_env]} AWS_DEFAULT_REGION={region} AWS_ACCESS_KEY_ID={access_key} AWS_SECRET_ACCESS_KEY={secret_key} --override --add'
        result = run_command(cmd, warn=True)

        if result.ok:
            click.secho(
                f'Add Travis Environment in Travis Config Successful',
                fg='green',
                bold=True)
        else:
            click.secho(
                f'Add Travis Environment in Travis Config Failure',
                fg='red',
                bold=True)

        if auto_push_message:
            cmd = f'git add .'
            result = run_command(cmd, warn=True)
            cmd = f'git commit -m "{auto_push_message}"'
            result = run_command(cmd, warn=True)
            cmd = f'git push'
            result = run_command(cmd, warn=True)
            if result.ok:
                click.secho(
                    f'Push Commit to GitHub Successful', fg='green', bold=True)
            else:
                click.secho(
                    f'Push Commit to GitHub Failure', fg='red', bold=True)


@cli.command()
@pass_context
def info(ctx):
    """Retrieve AP Job Info"""
    name, environment, app_path = ctx.configs['name'], ctx.configs[
        'environment'], ctx.configs['app_path']

    click.secho(f'AP Job Info:', fg='green', bold=True)
    click.secho(f'  Name: {name}', fg='green')
    click.secho(f'  Type: AP Job', fg='green')
    click.secho(f'  Environment: {environment}', fg='green')
    click.secho(f'  APP Path: {app_path}', fg='green')


@cli.command()
# @click.option(
#     '-d',
#     '--date',
#     default='2018/03/14',
#     help='The date of log events returned')
@click.option(
    '-j',
    '--job-id',
    default='UNKNOWN',
    help='Specify the AP jod id to retrieve log')
@click.option(
    '-l',
    '--limit',
    default=5,
    help='The maximum number of job logs returned, up to 50 logs')
@click.option(
    '-t',
    '--tail',
    default=100,
    help='The maximum number of log lines returned, up to 10,000 log lines')
@pass_context
def log(ctx, job_id, limit, tail):
    """Retrieve or Monitor AP Job Log"""
    previous_timestamp = 0
    limit = 50 if limit > 50 else limit
    tail = 10000 if tail > 10000 else tail

    name, environment = ctx.configs['name'], ctx.configs['environment']

    log_group_name = '/aws/batch/job'
    log_stream = 'UNKNOWN'
    job_status = 'UNKNOWN'

    try:
        session = boto3.Session(profile_name=environment)

        if job_id == 'UNKNOWN':
            dynamodb = session.resource('dynamodb')
            ap_jobs = dynamodb.Table('ap_jobs')

            response = ap_jobs.query(
                KeyConditionExpression=Key('name').eq(name),
                ScanIndexForward=False,
                Limit=limit)

            jobs = response['Items']
            for job in jobs[::-1]:
                timestamp_str = str_from_timestamp(job['timestamp'])
                jid = job['id']
                status = job['status']
                click.secho(f'{timestamp_str}:', fg='green', bold=True)
                click.echo(f'ID: {jid}, Status: {status}')

            job_id = jobs[0]['id'] if len(jobs) > 0 else 'UNKNOWN'

        if job_id != 'UNKNOWN':
            batch = session.client('batch')
            response = batch.describe_jobs(jobs=[job_id])
            jobs = response['jobs']

            job = jobs[0] if len(jobs) > 0 else jobs

            if job['status'] in ('RUNNING', 'SUCCEEDED', 'FAILED'):
                log_stream = job['container']['logStreamName']
            job_status = job['status']

        if log_stream != 'UNKNOWN':
            logs = session.client('logs')
            response = logs.get_log_events(
                logGroupName=log_group_name,
                logStreamName=log_stream,
                limit=tail)

            for event in response['events']:
                timestamp = int(event['timestamp'] / 1000)
                if timestamp > previous_timestamp:
                    previous_timestamp = timestamp
                    click.secho(
                        f'{str_from_timestamp(timestamp)}:',
                        fg='green',
                        bold=True)

                click.echo(event['message'].rstrip())

    except Exception as exc:
        print(exc)
        click.secho(
            f'AP log not exists, job status: {job_status}',
            fg='red',
            bold=True)
