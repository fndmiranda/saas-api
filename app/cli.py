import typer

from app.core.commands import route as route_core

cli = typer.Typer()

cli.add_typer(
    route_core,
    name="route",
    help="Manager for all application route commands.",
)

if __name__ == "__main__":
    cli()
