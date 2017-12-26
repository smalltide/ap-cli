import os
import click
from invoke import run as run_command
from ap.utils import is_ap, get_ap_env, is_text_in_file
from ap.cli import pass_context


@click.group()
@click.pass_context
def cli(ctx):
    """AP Notify Configure, Travis, Slack, etc."""
    is_ap(ctx.obj.configs)


@cli.command()
@click.option('-s', '--source', default='travis', help='Trigger Source Name')
@click.option('-a', '--account', default='104corp', help='Slack Account Name')
@click.option('-t', '--token', required=True, help='Slack Access Token')
@click.option('-c', '--channel', required=True, help='Slack Channel Name')
@pass_context
def slack(ctx, source, account, token, channel):
    """Slack Notify Provider"""
    if source == 'travis':
        cmd = f'travis encrypt {account}:{token}#{channel} --append --add notifications.slack.rooms'
        result = run_command(cmd, warn=True)

        if result.ok:
            click.secho(
                f'Add Slack Notify in Travis Config Successful',
                fg='green',
                bold=True)
        else:
            click.secho(
                f'Add Slack Notify in Travis Config Failure',
                fg='red',
                bold=True)
    else:
        click.secho(
            f'No Support This Trigger Source: {source}', fg='red', bold=True)
