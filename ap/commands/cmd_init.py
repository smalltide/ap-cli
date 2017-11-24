import click


@click.group()
def cli():
    """AP Init Command"""
    pass


@cli.command()
@click.option('--name', default='name', help='This is project name')
def create(name):
    click.echo(f'Create {name}')
