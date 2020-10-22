"""
CLI
"""

# Click
import click


@click.group(help='What do you want to do?')
def cli():
    """
    Manage the main cli.
    """

    pass


@cli.command(help='File options.')
@click.option(
    '--encrypt',
    '-e',
    type=(str),
    help='[PATH] file.'
)
@click.option(
    '--decrypt',
    '-d',
    type=(str),
    help='[PATH] file.'
)
def file(encrypt, decrypt):
    """
    Manage files.
    """

    pass


@cli.command(help='Device options.')
@click.option(
    '--encrypt',
    '-e',
    type=(str),
    help='[PATH] device.'
    
)  
@click.option(
    '--decrypt',
    '-d',
    type=(str),
    help='[PATH] device.'
)  
def device(encrypt, decrypt):
    """
    Manage device.
    """

    pass


if __name__ == '__main__':
    cli()
