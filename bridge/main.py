import sys
import click

from bridge_init import BInit


@click.group()
def cli():
    pass


@cli.command(name="init", help="Prepare the tables")
def _init():
    """This function makes sure the following
    1. Properties file readability check.
    2. Test connection to the DB.
    3. Bridge funciton args preparation.
    """
    try:
        BInit().prepare_bridge_function_args()
    except Exception as e:
        click.echo("Error wile creating args")
        click.echo(click.style(text=str(e), fg="red"))
        exit(1)  # General error or abnormal termination
    click.echo("You are good to compile")


@cli.command(name="BCompile", help="Compile the bridge code")
@click.option(
    "-s",
    "--source",
    type=str,
    required=True,
    help="Full path including the file name",
)
def _compile(source):
    """This function,
    0. `Check if init`        : Init creates args for the bridge function
    1. `Syntax analysis`      : Bridge syntax analysis
    2. `Semantic analysis`    : Bridge logic validation
    3. `Code generations`     : Prepare a SQL with the function
    """
    click.echo(source)
    click.clear()


if __name__ == "__main__":
    cli()
