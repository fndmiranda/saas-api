import typer
from tabulate import tabulate

cli = typer.Typer()

route = typer.Typer()
cli.add_typer(
    route, name="route", help="Manager for all application route commands."
)


@route.command(help="Prints all available routes.")
def show():
    from app.main import api_router

    table = []
    for r in api_router.routes:
        auth = False
        for d in r.dependencies:
            if (
                d.dependency.__name__ == "get_current_user"
            ):  # TODO this is fragile
                auth = True
        table.append([r.name, r.path, auth, ",".join(r.methods)])

    typer.secho(
        tabulate(table, headers=["Name", "Path", "Authenticated", "Methods"])
    )


if __name__ == "__main__":
    cli()
