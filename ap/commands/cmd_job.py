import click
import os
from invoke import run as run_command
from ap.cli import pass_context
from ap.utils import generate_ap, is_ap


@click.group()
@click.pass_context
def cli(ctx):
    """AP Job, create, build, run, deploy, info, log"""
    if ctx.invoked_subcommand not in ('create',):
        is_ap(ctx.obj.configs)


@cli.command()
@click.option('-n', '--name', required=True, help='AP Name or Number')
@click.option('-l', '--language', required=True, help='AP Template Language')
@click.option('-t', '--tag', default='default', help='AP Language Tag')
@pass_context
def create(ctx, name, language, tag):
    """Create a AP Job Template"""
    target = os.path.join(ctx.home, name)
    if os.path.exists(target):
        raise click.ClickException(
            'Existing directory here, please run create command for an empty folder!')

    template = os.path.join(ctx.templates, 'job', language, tag)
    if not os.path.exists(template):
        raise click.ClickException(
            'The template not exists, please choose right language and tag of template')

    parameters = {'name': name, 'type': 'job'}
    generate_ap(target, template, parameters)


@cli.command()
@pass_context
def build(ctx):
    """Build AP Job Docker Image"""
    cmd = f'docker image rm ap/{ctx.configs["name"]}'
    result = run_command(cmd, warn=True)
    cmd = f'docker build -t ap/{ctx.configs["name"]} .'
    result = run_command(cmd, warn=True)
    if result.ok:
        click.secho(f'Build AP Successful', fg='green', bold=True)
    else:
        click.secho(f'Build AP Failure', fg='red', bold=True)


@cli.command()
@pass_context
def run(ctx):
    """Run AP Job on Local"""
    aws_folder = click.get_app_dir('aws', force_posix=True)
    cmd = f'docker run -e HOME=/home -v {ctx.home}/app:{ctx.configs["app_path"]} -v {aws_folder}:/home/.aws --rm ap/{ctx.configs["name"]}'
    result = run_command(cmd, warn=True)
    if result.ok:
        click.secho(f'Run AP Successful', fg='green', bold=True)
    else:
        click.secho(f'Run AP Failure', fg='red', bold=True)


@cli.command()
def deploy():
    """Trigger AP Job Travis CI/CD Flow on Cloud"""
    click.echo(f'Deploy')
    click.echo(click.get_app_dir('aws', force_posix=True))


@cli.command()
def info():
    """Retrieve AP Job Info"""
    click.echo(f'Info')


@cli.command()
def log():
    """Retrieve or Monitor AP Job Log"""
    click.echo(f'Log')
