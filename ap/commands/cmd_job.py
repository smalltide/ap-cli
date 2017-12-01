import click
import os
from ap.cli import pass_context
from ap.utils import generate_ap


@click.group()
def cli():
    """AP Job, create, build, run, deploy, info, log"""
    pass


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
            'Existing directory here, please run new command for an empty folder!')

    template = os.path.join(ctx.templates, language, tag)
    if not os.path.exists(template):
        raise click.ClickException(
            'The template not exists, please choose right language and tag of template')

    parameters = {'APName': name}
    generate_ap(target, template, parameters)


@cli.command()
@pass_context
def build(ctx):
    """Build AP Job Docker Image"""
    click.echo(f'Build')


@cli.command()
@pass_context
def run(ctx):
    """Run AP Job on Local"""
    click.secho(f'Run!', fg='green', blink=True)
    click.echo(vars(ctx))


@cli.command()
def deploy():
    """Trigger AP Job Travis CI/CD Flow on Cloud"""
    click.echo(f'Deploy')


@cli.command()
def info():
    """Retrieve AP Job Info"""
    click.echo(f'Info')


@cli.command()
def log():
    """Retrieve or Monitor AP Job Log"""
    click.echo(f'Log')
