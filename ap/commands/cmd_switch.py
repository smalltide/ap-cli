import os
import click
from ap.utils import is_ap, write_ap_job_config
from ap.cli import pass_context


@click.group()
@click.pass_context
def cli(ctx):
    """switch target environment"""
    is_ap(ctx.obj.configs)


@cli.command()
@click.option('-n', '--name', default='dev', type=click.Choice(['dev', 'stg', 'prod']), help='Target Environment Name')
@pass_context
def env(ctx, name):
    """Set AP Target Environment Name"""
    configs = ctx.configs

    if configs['type'] == 'job':
        config_file = os.path.join(ctx.home, '.ap.yml')
        configs['environment'] = f'ap-{ctx.configs["type"]}-{ctx.configs["name"]}-{name}'
        write_ap_job_config(config_file, configs)
        click.secho(f'Switch Target Environment to ',
                    nl=False, fg='green', bold=True)
        click.secho(f'{name}', fg='red', bold=True)
