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
    BInit()
    click.echo("Hello")


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


if __name__ == "__main__":
    cli()
