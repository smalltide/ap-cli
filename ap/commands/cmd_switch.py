import os
import click
from ap.utils import is_ap, write_ap_job_config, get_ap_env
from ap.cli import pass_context


@click.group()
@click.pass_context
def cli(ctx):
    """switch target environment"""
    is_ap(ctx.obj.configs)


@cli.command()
@click.option('-p', '--profile', default='dev', type=click.Choice(['dev', 'stg', 'prod']), help='Target Environment Name')
@pass_context
def env(ctx, profile):
    """Set AP Target Environment Name"""
    home, ap_type, ap_name, configs = ctx.home, ctx.configs[
        'type'], ctx.configs['name'], ctx.configs

    if ap_type == 'job':
        config_file = os.path.join(home, '.ap.yml')
        configs['environment'] = get_ap_env(ap_type, ap_name, profile)

        write_ap_job_config(config_file, configs)

        click.secho(f'Switch Target Environment to ',
                    nl=False, fg='green', bold=True)
        click.secho(f'{profile}', fg='red', bold=True)
