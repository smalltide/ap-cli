import os
import click
import yaml


def read_ap_config(file):
    configs = None

    if not os.path.isfile(file):
        return configs

    with open(file, 'r') as stream:
        try:
            configs = yaml.load(stream)
        except yaml.YAMLError as exc:
            click.echo(exc)

    return configs


def is_ap(config):
    if not config:
        raise click.ClickException('Not in AP Folder or AP Config Error!')
