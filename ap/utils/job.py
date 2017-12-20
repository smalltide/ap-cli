import os
import click
from ruamel.yaml import YAML, error
from jinja2 import Environment, FileSystemLoader


def generate_ap_job(target_folder, template_folder, parameters):
    click.secho(
        f'Creating AP Job Template in {target_folder}.', fg='green', bold=True)

    env = Environment(
        loader=FileSystemLoader(template_folder)
    )
    for template in env.list_templates():
        template_path = os.path.join(target_folder, template)
        os.makedirs(os.path.dirname(template_path), exist_ok=True)
        env.get_template(template).stream(parameters).dump(template_path)

        if template_path.endswith('.sh'):
            os.chmod(template_path, 0o755)

        click.secho(f'  Create  ', nl=False, fg='green')
        click.echo(template)


def write_ap_job_config(config_file, configs):
    result = False

    if not os.path.isfile(config_file):
        return result

    with open(config_file, 'w') as stream:
        try:
            yaml = YAML()
            yaml.dump(configs, stream)
            result = True
        except error.YAMLError as exc:
            click.echo(exc)

    return result
