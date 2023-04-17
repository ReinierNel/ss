import typer
import requests
from rich.console import Console
import crypto
import init

err_console = Console(stderr=True)
console = Console()
app = typer.Typer()

action = "delete"

settings = init.read_settings()

if init.validate_settings():
    public_key = bytes(settings['keys']['public'], "UTF-8")
    url = settings['url']
    username = settings['username']
    password = settings['password']
else:
    public_key = None
    url = None
    username = None
    password = None

def rest_delete(url: str, path: str, id: str, headers: dict, body: dict, status_code: int):
    
    response = requests.delete(f"{url}/{path}/{id}", json=body, verify=False, headers=headers)

    if response.status_code == status_code:
        return True
    elif response.status_code == 401:
        print(typer.style(f"ERROR:    authentication failed`", fg=typer.colors.RED))
    elif response.status_code == 403:
        print(typer.style(f"ERROR:    you are not authorized to perform this action`", fg=typer.colors.RED))
    elif response.status_code == 404:
        print(typer.style(f"ERROR:    endpoint not found`", fg=typer.colors.RED))
    elif response.status_code == 500:
        print(typer.style(f"ERROR:    unable to delete item, {response.reason}`", fg=typer.colors.RED))
    else:
        print(typer.style(f"ERROR:    something whent wrong.", fg=typer.colors.RED))
        print(response._content)

@app.command()
def secret(
        id: int = typer.Argument(..., help="ID of secret to delete"),
    ):
    """
    Delete/remove a secret
    """
    function = "secret"

    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
        'api-user': username,
        'api-password': password,
    }

    if rest_delete(url=url, path=function, id=str(id), headers=headers, body={}, status_code=202):
        print(typer.style(f"info:    {function} {id} {action} success`", fg=typer.colors.GREEN))
    else:
        print(typer.style(f"error:    {function} {id} {action} failed`", fg=typer.colors.RED))
        raise typer.Exit(code=1)

@app.command()
def group(
        id: int = typer.Argument(..., help="ID of group to delete"),
    ):
    """
    Delete/remove a secret
    """
    function = "group"

    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
        'api-user': username,
        'api-password': password,
    }

    if rest_delete(url=url, path=function, id=str(id), headers=headers, body={}, status_code=202):
        print(typer.style(f"info:    {function} {id} {action} success`", fg=typer.colors.GREEN))
    else:
        print(typer.style(f"error:    {function} {id} {action} failed`", fg=typer.colors.RED))
        raise typer.Exit(code=1)
    
@app.command()
def member(
        id: int = typer.Argument(..., help="ID of member to delete"),
    ):
    """
    Delete/remove a member
    """
    function = "member"

    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
        'api-user': username,
        'api-password': password,
    }

    if rest_delete(url=url, path=function, id=str(id), headers=headers, body={}, status_code=202):
        print(typer.style(f"info:    {function} {id} {action} success`", fg=typer.colors.GREEN))
    else:
        print(typer.style(f"error:    {function} {id} {action} failed`", fg=typer.colors.RED))
        raise typer.Exit(code=1)
    
@app.command()
def role(
        id: int = typer.Argument(..., help="ID of role to delete"),
    ):
    """
    Delete/remove a role
    """
    function = "role"

    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
        'api-user': username,
        'api-password': password,
    }

    if rest_delete(url=url, path=function, id=str(id), headers=headers, body={}, status_code=202):
        print(typer.style(f"info:    {function} {id} {action} success`", fg=typer.colors.GREEN))
    else:
        print(typer.style(f"error:    {function} {id} {action} failed`", fg=typer.colors.RED))
        raise typer.Exit(code=1)
    
@app.command()
def assign(
        id: int = typer.Argument(..., help="ID of assign to delete"),
    ):
    """
    Delete/remove a assign
    """
    function = "assign"

    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
        'api-user': username,
        'api-password': password,
    }

    if rest_delete(url=url, path=function, id=str(id), headers=headers, body={}, status_code=202):
        print(typer.style(f"info:    {function} {id} {action} success`", fg=typer.colors.GREEN))
    else:
        print(typer.style(f"error:    {function} {id} {action} failed`", fg=typer.colors.RED))
        raise typer.Exit(code=1)
    
@app.command()
def user(
        id: int = typer.Argument(..., help="ID of user to delete"),
    ):
    """
    Delete/remove a user
    """
    function = "user    "

    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
        'api-user': username,
        'api-password': password,
    }

    if rest_delete(url=url, path=function, id=str(id), headers=headers, body={}, status_code=202):
        print(typer.style(f"info:    {function} {id} {action} success`", fg=typer.colors.GREEN))
    else:
        print(typer.style(f"error:    {function} {id} {action} failed`", fg=typer.colors.RED))
        raise typer.Exit(code=1)