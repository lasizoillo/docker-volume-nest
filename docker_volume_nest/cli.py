import pkg_resources

import click

from .service import serve_app


def get_version():
    return pkg_resources.get_distribution('docker_volume_nest').version


@click.group()
def cli():
    """
    Grouping commands needed
    :return:
    """


@cli.command()
@click.option("--app-name", default="docker_volume_nest")
def serve(app_name):
    """
    Serve unix socket with plugin service api

    :param: app_name allows reuse driver more than one time in a machine
    :return:
    """
    serve_app(app_name)


@cli.command()
def init():
    """
    Init real storage

    :return:
    """

@cli.command()
def create(volname):
    """
    Create a volname exportable via nfs
    :param volname:
    :return:
    """

@cli.command()
def list():
    """
    Return a list of volumes created
    :return:
    """

@cli.command()
def path(volname):
    """
    Return nfs mount point of a given `volname`
    :return:
    """

@cli.command()
def remove(volname):
    """
    Destroy a volname and his mounts
    :param volname:
    :return:
    """

@cli.command()
def mount(volname):
    """
    Mounts nfs mountpoint of volname
    :param volname:
    :return:
    """

@cli.command()
def unmount(volname):
    """
    Unmounts nfs mountpoint of volname
    :param volname:
    :return:
    """

@cli.command()
def version():
    """
    Prints program version
    :return:
    """
    click.echo(get_version())


def main():
    cli(auto_envvar_prefix="NEST")
