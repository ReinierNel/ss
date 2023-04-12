import typer
import requests
from rich.console import Console
import crypto
import init
import json

err_console = Console(stderr=True)
console = Console()
app = typer.Typer()

action = "update"

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

def rest_put(url: str, path: str, headers: dict, body: dict, status_code: int):
    
    response = requests.put(f"{url}/{path}/", json=body, verify=False, headers=headers)

    if response.status_code == status_code:
        return True
    elif response.status_code == 401:
        print(typer.style(f"ERROR:    you are not authorized to perform this action`", fg=typer.colors.RED))
    elif response.status_code == 403:
        print(typer.style(f"ERROR:    authentication failed`", fg=typer.colors.RED))
    elif response.status_code == 404:
        print(typer.style(f"ERROR:    endpoint not found`", fg=typer.colors.RED))
    elif response.status_code == 500:
        print(typer.style(f"ERROR:    unable to update item, {response.reason}`", fg=typer.colors.RED))
    else:
        print(typer.style(f"ERROR:    something whent wrong.", fg=typer.colors.RED))
        print(response._content.decode("UTF-8"))

@app.command()
def secret(
        id : int = typer.Argument(..., help="ID of secret to update"),
        name: str = typer.Option(None, help="Name of the secret"),
        value: str = typer.Option(None, help="Value of the secret"),
        sse: bool = typer.Option(False, help="Server Side Encryption, this will tell the server to encrypt the data using its private key"),
    ):
    """
    Update a secret
    """
    function = "secret"

    if sse:
        data = value
    else:
        data = crypto.encrypt(public_key, bytes(value, "UTF-8"))     

    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
        'api-user': username,
        'api-password': password,
        'server-side-encryption': str(sse).lower()
    }


    body = {
        'sse': sse,
        'id': id,
        'name': name,
        'value': data,
    }

    if rest_put(url=url, path=function, headers=headers, body=body, status_code=201):
        print(typer.style(f"INFO:    {function} {name} {action} success`", fg=typer.colors.GREEN))
    else:
        print(typer.style(f"ERRPR:    {function} {name} {action} failed`", fg=typer.colors.RED))
        raise typer.Exit(code=1)
    
@app.command()
def group(
        id : int = typer.Argument(..., help="ID of group to update"),
        name: str = typer.Option(..., help="Name of the secret"),
    ):
    """
    Update a group
    """
    function = "group"

    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
        'api-user': username,
        'api-password': password,
    }


    body = {
        'id': id,
        'name': name,
    }

    if rest_put(url=url, path=function, headers=headers, body=body, status_code=201):
        print(typer.style(f"INFO:    {function} {name} {action} success`", fg=typer.colors.GREEN))
    else:
        print(typer.style(f"ERRPR:    {function} {name} {action} failed`", fg=typer.colors.RED))
        raise typer.Exit(code=1)
    
@app.command()
def member(
        id : int = typer.Argument(..., help="ID of member to update"),
        group_id: int = typer.Option(..., help="ID of group"),
        user_id: int = typer.Option(..., help="ID of user"),
    ):
    """
    Update a member
    """
    function = "member"

    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
        'api-user': username,
        'api-password': password,
    }


    body = {
        "id": id,
        "gid": group_id,
        "uid": user_id,
    }

    if rest_put(url=url, path=function, headers=headers, body=body, status_code=201):
        print(typer.style(f"INFO:    {function} {id} {action} success`", fg=typer.colors.GREEN))
    else:
        print(typer.style(f"ERRPR:    {function} {id} {action} failed`", fg=typer.colors.RED))
        raise typer.Exit(code=1)
    
@app.command()
def role(
        id : int = typer.Argument(..., help="ID of role to update"),
        name: str = typer.Option(..., help="Name of role"),
        function_id: int = typer.Option(..., help="ID of function"),
        read: bool = typer.Option(False, help="This role has read Access read access"),
        write: bool = typer.Option(False, help="This role has write access")
    ):
    """
    Update a role
    """
    function = "role"

    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
        'api-user': username,
        'api-password': password,
    }


    body = {
        "id": 0,
        "name": "string",
        "fid": function_id,
        "read": read,
        "write": write,
    }

    if rest_put(url=url, path=function, headers=headers, body=body, status_code=201):
        print(typer.style(f"INFO:    {function} {name} {action} success`", fg=typer.colors.GREEN))
    else:
        print(typer.style(f"ERRPR:    {function} {name} {action} failed`", fg=typer.colors.RED))
        raise typer.Exit(code=1)
    
@app.command()
def assign(
        id : int = typer.Argument(..., help="ID of assign to update"),
        role_id: int = typer.Option(..., help="ID of role"),
        group_id: int = typer.Option(..., help="ID of group"),

    ):
    """
    Update a role
    """
    function = "role"

    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
        'api-user': username,
        'api-password': password,
    }


    body = {
        "id": id,
        "rid": role_id,
        "gid": group_id,
    }

    if rest_put(url=url, path=function, headers=headers, body=body, status_code=201):
        print(typer.style(f"INFO:    {function} {id} {action} success`", fg=typer.colors.GREEN))
    else:
        print(typer.style(f"ERRPR:    {function} {id} {action} failed`", fg=typer.colors.RED))
        raise typer.Exit(code=1)
    
@app.command()
def user(
        id : int = typer.Argument(..., help="ID of user to update"),
        name: int = typer.Option(..., help="New name for user"),
        pwd: int = typer.Option(..., help="New Password for user"),

    ):
    """
    Update a user
    """
    function = "user"

    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
        'api-user': username,
        'api-password': password,
    }


    body = {
        "id": id,
        "name": name,
        "hash": pwd,
    }

    if rest_put(url=url, path=function, headers=headers, body=body, status_code=201):
        print(typer.style(f"INFO:    {function} {name} {action} success`", fg=typer.colors.GREEN))
    else:
        print(typer.style(f"ERRPR:    {function} {name} {action} failed`", fg=typer.colors.RED))
        raise typer.Exit(code=1)