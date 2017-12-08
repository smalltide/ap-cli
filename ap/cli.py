import os
import sys
import click
from ap.utils import read_parameters

CONTEXT_SETTINGS = dict(auto_envvar_prefix='AP')


class Context(object):

    def __init__(self):
        self.home = os.getcwd()
        self.templates = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                      'templates'))
        self.ap_name = None

        parameters_file = os.path.join(self.home, 'parameters.json')
        parameters = read_parameters(parameters_file)

        if parameters:
            self.ap_name = parameters[0]['ParameterValue']


cmd_folder = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                          'commands'))
pass_context = click.make_pass_decorator(Context, ensure=True)


class APCLI(click.MultiCommand):

    def list_commands(self, ctx):
        rv = []
        for filename in os.listdir(cmd_folder):
            if filename.endswith('.py') and filename.startswith('cmd_'):
                rv.append(filename[4:-3])
        rv.sort()
        return rv

    def get_command(self, ctx, name):
        try:
            if sys.version_info[0] == 2:
                name = name.encode('ascii', 'replace')
            mod = __import__('ap.commands.cmd_' + name, None, None, ['cli'])
        except ImportError:
            return
        return mod.cli


@click.command(cls=APCLI, context_settings=CONTEXT_SETTINGS)
@click.version_option()
@pass_context
def cli(ctx):
    """This package provides a command line interface to use the create, build, deploy, log, notify and resource manager feature of AP2.0"""
    pass
