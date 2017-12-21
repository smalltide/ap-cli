import click
import os
from invoke import run as run_command
from ap.utils import generate_ap_job, is_ap
from ap.cli import pass_context


@click.group()
@click.pass_context
def cli(ctx):
    """Job create, build, run, deploy, info, log"""
    if ctx.invoked_subcommand not in ('create',):
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
            'Existing directory here, please run create command for an empty folder!')

    template = os.path.join(templates, 'job', language, tag)
    if not os.path.exists(template):
        raise click.ClickException(
            'The template not exists, please choose right language and tag of template')

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
def deploy():
    """Trigger AP Job Travis CI/CD Flow on Cloud"""
    click.echo(f'Deploy')


@cli.command()
@pass_context
def info(ctx):
    """Retrieve AP Job Info"""
    name, environment, app_path = ctx.configs['name'], ctx.configs['environment'], ctx.configs['app_path']

    click.secho(f'AP Job Info:', fg='green', bold=True)
    click.secho(f'  Name: {name}', fg='green')
    click.secho(f'  Type: AP Job', fg='green')
    click.secho(f'  Environment: {environment}', fg='green')
    click.secho(f'  APP Path: {app_path}', fg='green')


@cli.command()
def log():
    """Retrieve or Monitor AP Job Log"""
    click.echo(f'Log')
