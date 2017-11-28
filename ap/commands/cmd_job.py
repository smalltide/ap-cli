import click


@click.group()
def cli():
    """AP Job, create, build, run, deploy, info and log"""
    pass


@cli.command()
@click.option('-n', '--name', help='AP Name or Number')
@click.option('-l', '--language', help='AP Template Language')
def create(name, language):
    """Create a AP Job Template"""
    click.echo(f'Create')


@cli.command()
def build():
    """Build AP Job Docker Image"""
    click.echo(f'Build')


@cli.command()
def run():
    """Run AP Job on Local"""
    click.echo(f'Run')


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
