import os
import click
from ruamel.yaml import YAML, error


def read_ap_config(file):
    configs = None

    if not os.path.isfile(file):
        return configs

    with open(file, 'r') as stream:
        try:
            yaml = YAML()
            configs = yaml.load(stream)
        except error.YAMLError as exc:
            click.echo(exc)

    return configs


def is_ap(config):
    if not config:
        raise click.ClickException('Not in AP Folder or AP Config Error!')


def get_ap_env(ap_type, ap_name, env):
    return f'ap-{ap_type}-{ap_name}-{env}'
