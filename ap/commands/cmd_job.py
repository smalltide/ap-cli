import click
from ap.cli import pass_context


@click.group()
def cli():
    """AP Job, create, build, run, deploy, info, log"""
    pass


@cli.command()
@click.option('-n', '--name', help='AP Name or Number')
@click.option('-l', '--language', help='AP Template Language')
def create(name, language):
    """Create a AP Job Template"""
    click.echo(f'Create')


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
