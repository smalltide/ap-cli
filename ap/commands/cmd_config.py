import os
import click
from invoke import run as run_command
from ap.utils import is_ap, get_ap_env, is_text_in_file
from ap.cli import pass_context


@click.group()
@click.pass_context
def cli(ctx):
    """Configure for Cloud Provider, Resource, ToolChain, etc."""
    is_ap(ctx.obj.configs)


@cli.command()
@click.option('-p', '--profile', default='dev', type=click.Choice(['dev', 'stg', 'prod']), help='Target Environment Name')
@pass_context
def aws(ctx, profile):
    """Set AWS Environment Parameters"""
    ap_type, ap_name = ctx.configs['type'], ctx.configs['name']
    profile = get_ap_env(ap_type, ap_name, profile)

    cmd = f'aws configure --profile {profile}'
    result = run_command(cmd, warn=True)
    if result.ok:
        click.secho(f'Add AP AWS Profile and Credential Successful: ',
                    nl=False, fg='green', bold=True)
        click.secho(f'{profile}', fg='red', bold=True)
    else:
        click.secho(f'Add AP AWS Profile and Credential Failure',
                    fg='red', bold=True)


@cli.command()
@click.option('-a', '--account', default='104corp', help='GitHub User Account')
@click.option('-r', '--repository', required=True, help='GitHub Repository Name')
@pass_context
def github(ctx, account, repository):
    """Link AP to GitHub Repository"""
    github_config = os.path.join(ctx.home, '.git', 'config')
    is_linked = is_text_in_file(
        'github', github_config) and is_text_in_file(account, github_config)

    if is_linked:
        click.secho(f'AP and GitHub Already Linked', fg='green', bold=True)
    else:
        if not os.path.isfile(github_config):
            cmd = f'git init'
            result = run_command(cmd, warn=True)

        cmd = f'git remote add origin git@github.com:{account}/{repository}.git'
        result = run_command(cmd, warn=True)
        cmd = f'git add .'
        result = run_command(cmd, warn=True)
        cmd = f'git commit -m "init project"'
        result = run_command(cmd, warn=True)
        cmd = f'git push --set-upstream origin master'
        result = run_command(cmd, warn=True)

        if result.ok:
            click.secho(f'AP Link GitHub Repository Successful',
                        fg='green', bold=True)
        else:
            click.secho(f'AP Link GitHub Repository Failure',
                        fg='red', bold=True)
