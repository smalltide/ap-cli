import click


@click.group()
def cli():
    """This package provides a command line interface to create, build, deploy AWS Batch Job"""
    pass


@cli.command()
@click.option('--name', default='name', help='This is name option')
@click.option('--repeat', default=1, help='This is hello repeat option')
@click.argument('out', type=click.File('w'), default='-', required=False)
def hello(name, repeat, out):
    """This is hello command"""
    for _ in range(repeat):
        click.echo(f'Hello {name}', file=out)
