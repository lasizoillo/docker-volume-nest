import pkg_resources
import sys
import logging

import click
import confight

from docker_volume_nest.defaults import DEFAULTS
from docker_volume_nest.util import exec_command
from .service import serve_app


logger = logging.getLogger(__name__)


def get_version():
    return pkg_resources.get_distribution('docker_volume_nest').version


def cb_load_config(ctx, param, value):
    return confight.load_app(value) or DEFAULTS


app_name_option = click.option(
    "--app-name", "config",
    default="docker_volume_nest", callback=cb_load_config
)

volname = click.argument("volname", nargs=1)


@click.group()
def cli():
    """
    Grouping commands needed
    :return:
    """


@cli.command()
@app_name_option
def serve(config):
    """
    Serve unix socket with plugin service api

    :param: app_name allows reuse driver more than one time in a machine
    :return:
    """
    serve_app(config)


@cli.command()
@app_name_option
def init(config):
    """
    Init real storage

    :return:
    """
    exec_command(config, "init")


@cli.command()
@app_name_option
@volname
def create(config, volname):
    """
    Create a volname exportable via nfs
    :param volname:
    :return:
    """
    exec_command(config, "create", volname)


@cli.command()
@app_name_option
def list(config):
    """
    Return a list of volumes created
    :return:
    """
    exec_command(config, "list")


@cli.command()
@app_name_option
@volname
def path(config, volname):
    """
    Return nfs mount point of a given `volname`
    :return:
    """
    exec_command(config, "path", volname)


@cli.command()
@app_name_option
@volname
def remove(config, volname):
    """
    Destroy a volname and his mounts
    :param volname:
    :return:
    """
    exec_command(config, "remove", volname)


@cli.command()
@app_name_option
@volname
def mount(config, volname):
    """
    Mounts nfs mountpoint of volname
    :param volname:
    :return:
    """
    exec_command(config, "mount", volname)


@cli.command()
@app_name_option
@volname
def unmount(config, volname):
    """
    Unmounts nfs mountpoint of volname
    :param volname:
    :return:
    """
    exec_command(config, "unmount", volname)


@cli.command()
@app_name_option
def scope(config):
    exec_command(config, "scope")


@cli.command()
def version():
    """
    Prints program version
    :return:
    """
    click.echo(get_version())


def main():
    try:
        cli(auto_envvar_prefix="NEST")
    except Exception as e:
        logger.exception("Uncatched exception")
        click.secho(str(e), color="red")
        sys.exit(1)
