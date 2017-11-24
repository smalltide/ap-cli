import click


@click.group()
def cli():
    """AP Status Command"""
    pass


@cli.command()
@click.option('--name', default='name', help='This is Status name')
def show(name):
    """Show AP Status"""
    click.echo(f'Status {name}')
