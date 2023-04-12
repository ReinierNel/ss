from typing import Optional
import typer
import init
import add, update, get, delete

app = typer.Typer()

# init commands this boulds settings needed by cli
app.add_typer(init.app, name="init")
app.add_typer(add.app, name="add")
app.add_typer(get.app, name="get")
app.add_typer(update.app, name="update")
app.add_typer(delete.app, name="delete")

if __name__ == "__main__":
    app()