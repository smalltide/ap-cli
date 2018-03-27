import os
import click
from ruamel.yaml import YAML, error
from datetime import datetime, timezone


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


def is_text_in_file(text, file):
    result = False

    if not os.path.isfile(file):
        return result

    with open(file, 'r') as stream:
        try:
            if text in stream.read():
                result = True
        except Exception as exc:
            click.echo(exc)

    return result


def str_from_timestamp(timestamp):
    time_string = datetime.fromtimestamp(
        timestamp, timezone.utc).strftime('%Y/%m/%d %H:%M:%S+00:00 (UTC)')

    return time_string
