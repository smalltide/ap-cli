import click
import os
from invoke import run as run_command
from ap.utils import generate_ap_job, is_ap, is_text_in_file
from ap.cli import pass_context


@click.group()
@click.pass_context
def cli(ctx):
    """Job create, build, run, deploy, info, log"""
    if ctx.invoked_subcommand not in ('create', ):
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
            'Existing directory here, please run create command for an empty folder!'
        )

    template = os.path.join(templates, 'job', language, tag)
    if not os.path.exists(template):
        raise click.ClickException(
            'The template not exists, please choose right language and tag of template'
        )

    parameters = {'name': name, 'type': 'job'}
    generate_ap_job(target, template, parameters)


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
        region = run_command(
            f'aws configure get region --profile {environment}',
            warn=True,
            hide='out').stdout.strip()
        key_id = run_command(
            f'aws configure get aws_access_key_id --profile {environment}',
            warn=True,
            hide='out').stdout.strip()
        access_key = run_command(
            f'aws configure get aws_secret_access_key --profile {environment}',
            warn=True,
            hide='out').stdout.strip()

        cmd = f'travis encrypt AP_NAME={name} AWS_ACCOUNT_ID={ctx.job_env[job_env]} AWS_DEFAULT_REGION={region} AWS_ACCESS_KEY_ID={key_id} AWS_SECRET_ACCESS_KEY={access_key} --override --add'
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
def log():
    """Retrieve or Monitor AP Job Log"""
    click.echo(f'Log')
