import typer
import requests
from rich.console import Console
import crypto
import init
import json

err_console = Console(stderr=True)
console = Console()
app = typer.Typer()

action = "add"

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

def rest_post(url: str, path: str, headers: dict, body: dict, status_code: int):
    
    response = requests.post(f"{url}/{path}/", json = body,verify=False, headers=headers)

    if response.status_code == status_code:
        return True
    elif response.status_code == 401:
        print(typer.style(f"ERROR:    you are not authorized to perform this action`", fg=typer.colors.RED))
    elif response.status_code == 403:
        print(typer.style(f"ERROR:    authentication failed`", fg=typer.colors.RED))
    elif response.status_code == 404:
        print(typer.style(f"ERROR:    endpoint not found`", fg=typer.colors.RED))
    elif response.status_code == 500:
        print(typer.style(f"ERROR:    item may already exist, or the server cannot process your request at this time`", fg=typer.colors.RED))
    else:
        print(typer.style(f"ERROR:    something whent wrong.", fg=typer.colors.RED))
        details = response._content.decode("UTF-8")
        print(details)

@app.command()
def secret(
        name: str = typer.Argument(..., help="Name of the secret"),
        value: str = typer.Argument(..., help="Value of the secret"),
        sse: bool = typer.Option(False, help="Server Side Encryption, this will tell the server to encrypt the data using its private key"),
    ):
    """
    Create/add a new secret
    """
    function = "secret"

    if not sse:
        data = crypto.encrypt(public_key, bytes(value, "UTF-8"))
    else:
        data = value

    headers = {
        'api-user': username,
        'api-password': password,
        'server-side-encryption': str(sse).lower()
    }

    body = {
        "name": name,
        "value": f"{data}"
    }

    if rest_post(url=url, path=function, headers=headers, body=body, status_code=201):
        print(typer.style(f"INFO:    {function} {name} {action} success`", fg=typer.colors.GREEN))
    else:
        print(typer.style(f"ERROR:    {function} {name} {action} failed`", fg=typer.colors.RED))
        raise typer.Exit(code=1)
    
@app.command()
def group(
        name: str = typer.Argument(..., help="Name of the secret"),
    ):
    """
    Create/add a new group
    """
    function = "group"

    headers = {
        'api-user': username,
        'api-password': password,
    }

    body = {
        "name": name,
    }

    if rest_post(url=url, path=function, headers=headers, body=body, status_code=201):
        print(typer.style(f"INFO:    {function} {name} {action} success`", fg=typer.colors.GREEN))
    else:
        print(typer.style(f"ERROR:    {function} {name} {action} failed`", fg=typer.colors.RED))
        raise typer.Exit(code=1)
    
@app.command()
def member(
        group_id: int = typer.Argument(..., help="Group ID"),
        user_id: int = typer.Argument(..., help="User ID"),
    ):
    """
    Add an existing users as member to a existing group
    """
    function = "member"

    headers = {
        'api-user': username,
        'api-password': password,
    }

    body = {
        "gid": group_id,
        "uid": user_id,
    }

    if rest_post(url=url, path=function, headers=headers, body=body, status_code=201):
        print(typer.style(f"INFO:    {function} {action} success`", fg=typer.colors.GREEN))
    else:
        print(typer.style(f"ERROR:    {function} {action} failed`", fg=typer.colors.RED))
        raise typer.Exit(code=1)
    
@app.command()
def role(
        name: str = typer.Argument(..., help="Role Name"),
        function_id: int = typer.Argument(..., help="Finction ID"),
        read: bool = typer.Argument(False, help="Allow Read"),
        write: bool = typer.Argument(False, help="Allow write")
    ):
    """
    Create/add a new role
    """
    function = "role"

    headers = {
        'api-user': username,
        'api-password': password,
    }

    body = {
        "name": name,
        "fid": function_id,
        "read": read,
        "write": write,
    }

    if rest_post(url=url, path=function, headers=headers, body=body, status_code=201):
        print(typer.style(f"INFO:    {function} {name} {action} success`", fg=typer.colors.GREEN))
    else:
        print(typer.style(f"ERROR:    {function} {name} {action} failed`", fg=typer.colors.RED))
        raise typer.Exit(code=1)
    
@app.command()
def assign(
        role_id: int = typer.Argument(..., help="Role ID"),
        group_id: int = typer.Argument(..., help="Group ID"),
    ):
    """
    Assign an existing group to an existing role
    """
    function = "assign"

    headers = {
        'api-user': username,
        'api-password': password,
    }

    body = {
        "rid": role_id,
        "gid": group_id,
    }

    if rest_post(url=url, path=function, headers=headers, body=body, status_code=201):
        print(typer.style(f"INFO:    {function} {action} success`", fg=typer.colors.GREEN))
    else:
        print(typer.style(f"ERROR:    {function} {action} failed`", fg=typer.colors.RED))
        raise typer.Exit(code=1)
    
@app.command()
def user(
        name: str = typer.Argument(..., help="Users username"),
        pwd: str = typer.Argument(..., help="Users Password")
    ):
    """
    Create/add a new user
    """
    function = "user"

    headers = {
        'api-user': username,
        'api-password': password,
    }

    body = {
        "name": name,
        "hash": pwd
    }

    if rest_post(url=url, path=function, headers=headers, body=body, status_code=201):
        print(typer.style(f"INFO:    {function} {name} {action} success`", fg=typer.colors.GREEN))
    else:
        print(typer.style(f"ERROR:    {function} {name} {action} failed`", fg=typer.colors.RED))
        raise typer.Exit(code=1)