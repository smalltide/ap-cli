import click
from invoke import run as run_command
from ap.utils import is_ap, get_ap_env
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
