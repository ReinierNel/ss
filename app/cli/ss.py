from typing import Optional
import typer
import init
import create,read, update, delete

app = typer.Typer()

# init commands this boulds settings needed by cli
app.add_typer(init.app, name="init", help="Initialize settings")
app.add_typer(create.app, name="create", help="Adds an entry")
app.add_typer(create.app, name="add", help="Alias for create")
app.add_typer(read.app, name="read", help="Reads and entry")
app.add_typer(read.app, name="get", help="Alias for read")
app.add_typer(update.app, name="update", help="Updates an entry")
app.add_typer(update.app, name="edit", help="Alias for update")
app.add_typer(delete.app, name="delete", help="Delete an Entry")
app.add_typer(delete.app, name="remove", help="Alias for delete")

if __name__ == "__main__":
    app()