import typer
import requests
from rich.console import Console
import crypto
import init
import json
import os
from rich.console import Console
from rich.table import Table

console = Console()

err_console = Console(stderr=True)
console = Console()
app = typer.Typer()

action = "get"

settings = init.read_settings()

if init.validate_settings():
    private_key = bytes(settings['keys']['private'], "UTF-8")
    url = settings['url']
    username = settings['username']
    password = settings['password']
else:
    public_key = None
    url = None
    username = None
    password = None

def rest_get(url: str, path: str, headers: dict, status_code: int):
    
    response = requests.get(f"{url}/{path}", verify=False, headers=headers)
    if response.status_code == status_code:
        return response.json()
    elif response.status_code == 401:
        print(typer.style(f"ERROR:    you are not authorized to perform this action", fg=typer.colors.RED))
    elif response.status_code == 403:
        print(typer.style(f"ERROR:    authentication failed", fg=typer.colors.RED))
    elif response.status_code == 404:
        print(typer.style(f"ERROR:    endpoint not found", fg=typer.colors.RED))
    elif response.status_code == 500:
        print(typer.style(f"ERROR:    item may not exist, or the server cannot process your request at this time", fg=typer.colors.RED))
    else:
        print(typer.style(f"ERROR:    something whent wrong", fg=typer.colors.RED))
        details = response._content.decode("UTF-8")
        print(details)

    return False

@app.command()
def secret(
        name: str = typer.Argument(..., help="Name of the secret"),
        output: str = typer.Option("value", help="Set output format [value,json,table] value will only output te secret value"),
    ):
    """
    Get/Read Secret by name
    """

    function = "secret"

    headers = {
        'api-user': username,
        'api-password': password,
    }

    response = rest_get(url=url, path=f"{function}/{name}", headers=headers, status_code=200)
    if response:
        data = response
        if data['sse'] == False:
            encrypted_data = data['value']
            output = crypto.decrypt(private_key, encrypted_data)
            result = output.decode("UTF-8")
        else:
            result = data['value']
        
        if output == 'value':
            print(result)

        if output == 'json':
            print(json.dumps(
                {
                    'id': data['id'],
                    'name': data['name'],
                    'value': result,
                    'sse': data['sse'],
                    'modified': data['modified'],
                    'created': data['created']
                },
                indent=2
            ))

        if output == 'table':
            table = Table("ID", "Name", "Value" ,"SSE", "Modified", "Created")
            table.add_row(str(data['id']), data['name'], data['value'], str(data['sse']), data['modified'], data['created'])
            console.print(table)
            
    else:
        print(typer.style(f"ERROR:    {function} {name} {action} failed", fg=typer.colors.RED))
        raise typer.Exit(code=1)
    
@app.command()
def secrets(
        output: str = typer.Option("json", help="Set output format [json,table]"),
    ):
    """
    Get/Read all secrets but the secret value is REDACTED!
    """

    function = "secret"
    
    headers = {
        'api-user': username,
        'api-password': password,
    }

    response = rest_get(url=url, path=f"{function}/", headers=headers, status_code=200)
    if response:
        data = response

        if output == "json":
            print(
                json.dumps(
                    data,
                    indent=2,
            ))
        
        if output == "table":
            table = Table("ID", "Name", "Value" ,"SSE", "Modified", "Created")
            for cell in data:
                table.add_row(str(cell['id']), cell['name'], cell['value'], str(cell['sse']), cell['modified'], cell['created'])
            console.print(table)
    else:
        print(typer.style(f"ERROR:    {function}s {action} failed`", fg=typer.colors.RED))
        raise typer.Exit(code=1)
    
@app.command()
def group(
        id: str = typer.Argument(..., help="ID of the group"),
        output: str = typer.Option("json", help="Set output format [json,table]"),
    ):
    """
    Get/Read group by ID
    """

    function = "group"

    headers = {
        'api-user': username,
        'api-password': password,
    }

    response = rest_get(url=url, path=f"{function}/{id}", headers=headers, status_code=200)
    if response:
        data = response

        if output == 'json':
            print(json.dumps(
                data,
                indent=2
            ))

        if output == 'table':
            table = Table("ID", "Name", "Modified", "Created")
            table.add_row(str(data['id']), data['name'], data['modified'], data['created'])
            console.print(table)
            
    else:
        print(typer.style(f"ERROR:    {function} {id} {action} failed", fg=typer.colors.RED))
        raise typer.Exit(code=1)
    
@app.command()
def groups(
        output: str = typer.Option("json", help="Set output format [json,table]"),
    ):
    """
    Get/Read all groups
    """

    function = "group"
    
    headers = {
        'api-user': username,
        'api-password': password,
    }

    response = rest_get(url=url, path=f"{function}/", headers=headers, status_code=200)
    if response:
        data = response

        if output == "json":
            print(
                json.dumps(
                    data,
                    indent=2,
            ))
        
        if output == "table":
            table = Table("ID", "Name", "Modified", "Created")
            for cell in data:
                table.add_row(str(cell['id']), cell['name'], cell['modified'], cell['created'])
            console.print(table)
    else:
        print(typer.style(f"ERROR:    {function}s {action} failed`", fg=typer.colors.RED))
        raise typer.Exit(code=1)
    
@app.command()
def member(
        id: str = typer.Argument(..., help="ID of the member"),
        output: str = typer.Option("json", help="Set output format [json,table]"),
    ):
    """
    Get/Read member by ID
    """

    function = "member"

    headers = {
        'api-user': username,
        'api-password': password,
    }

    response = rest_get(url=url, path=f"{function}/{id}", headers=headers, status_code=200)
    if response:
        data = response

        if output == 'json':
            print(json.dumps(
                data,
                indent=2
            ))

        if output == 'table':
            table = Table("ID", "Group ID", "User ID", "Modified", "Created")
            table.add_row(str(data['id']), str(data['gid']), str(data['uid']), data['modified'], data['created'])
            console.print(table)
            
    else:
        print(typer.style(f"ERROR:    {function} {id} {action} failed", fg=typer.colors.RED))
        raise typer.Exit(code=1)
    
@app.command()
def members(
        output: str = typer.Option("json", help="Set output format [json,table]"),
    ):
    """
    Get/Read all members
    """

    function = "member"
    
    headers = {
        'api-user': username,
        'api-password': password,
    }

    response = rest_get(url=url, path=f"{function}/", headers=headers, status_code=200)
    if response:
        data = response

        if output == "json":
            print(
                json.dumps(
                    data,
                    indent=2,
            ))
        
        if output == "table":
            table = Table("ID", "Group ID", "User ID", "Modified", "Created")
            for cell in data:
                table.add_row(str(cell['id']), str(cell['gid']), str(cell['uid']), cell['modified'], cell['created'])
            console.print(table)
    else:
        print(typer.style(f"ERROR:    {function}s {action} failed`", fg=typer.colors.RED))
        raise typer.Exit(code=1)
    
@app.command()
def function(
        id: str = typer.Argument(..., help="ID of the function"),
        output: str = typer.Option("json", help="Set output format [json,table]"),
    ):
    """
    Get/Read function by ID
    """

    function = "function"

    headers = {
        'api-user': username,
        'api-password': password,
    }

    response = rest_get(url=url, path=f"{function}/{id}", headers=headers, status_code=200)
    if response:
        data = response

        if output == 'json':
            print(json.dumps(
                data,
                indent=2
            ))

        if output == 'table':
            table = Table("ID", "Name", "Modified", "Created")
            table.add_row(str(data['id']), data['name'], data['modified'], data['created'])
            console.print(table)
            
    else:
        print(typer.style(f"ERROR:    {function} {id} {action} failed", fg=typer.colors.RED))
        raise typer.Exit(code=1)
    
@app.command()
def functions(
        output: str = typer.Option("json", help="Set output format [json,table]"),
    ):
    """
    Get/Read all members
    """

    function = "function"
    
    headers = {
        'api-user': username,
        'api-password': password,
    }

    response = rest_get(url=url, path=f"{function}/", headers=headers, status_code=200)
    if response:
        data = response

        if output == "json":
            print(
                json.dumps(
                    data,
                    indent=2,
            ))
        
        if output == "table":
            table = Table("ID", "Name", "Modified", "Created")
            for cell in data:
                table.add_row(str(cell['id']), cell['name'], cell['modified'], cell['created'])
            console.print(table)
    else:
        print(typer.style(f"ERROR:    {function}s {action} failed`", fg=typer.colors.RED))
        raise typer.Exit(code=1)
    

@app.command()
def server(
        setting: str = typer.Argument("public-key", help="Name of server setting of the group"),
        output: str = typer.Option("json", help="Set output format [json,table]"),
    ):
    """
    Get/Read function by ID
    """

    function = "setting"

    headers = {
        'api-user': username,
        'api-password': password,
    }

    if setting == "public-key":
        response = rest_get(url=url, path="setting/key/public", headers=headers, status_code=200)
    else:
        print(typer.style(f"WARN:    server {function} not found", fg=typer.colors.YELLOW))
        raise typer.Exit(code=0)

    if response:
        data = response

        if output == 'json':
            print(json.dumps(
                data,
                indent=2
            ))

        if output == 'table':
            table = Table("ID", "Name", "Value", "Modified", "Created")
            table.add_row(str(data['id']), data['name'], data['value'], data['modified'], data['created'])
            console.print(table)
            
    else:
        print(typer.style(f"ERROR:    {function} {id} {action} failed", fg=typer.colors.RED))
        raise typer.Exit(code=1)

@app.command()
def role(
        id: str = typer.Argument(..., help="ID of the group"),
        output: str = typer.Option("json", help="Set output format [json,table]"),
    ):
    """
    Get/Read role by ID
    """

    function = "role"

    headers = {
        'api-user': username,
        'api-password': password,
    }

    response = rest_get(url=url, path=f"{function}/{id}", headers=headers, status_code=200)
    if response:
        data = response

        if output == 'json':
            print(json.dumps(
                data,
                indent=2
            ))

        if output == 'table':
            table = Table("ID", "Name", "Function ID", "Read", "Write", "Modified", "Created")
            table.add_row(str(data['id']), data['name'], str(data['fid']), str(data['read']), str(data['write']), data['modified'], data['created'])
            console.print(table)
            
    else:
        print(typer.style(f"ERROR:    {function} {id} {action} failed", fg=typer.colors.RED))
        raise typer.Exit(code=1)
    
@app.command()
def roles(
        output: str = typer.Option("json", help="Set output format [json,table]"),
    ):
    """
    Get/Read all roles
    """

    function = "role"
    
    headers = {
        'api-user': username,
        'api-password': password,
    }

    response = rest_get(url=url, path=f"{function}/", headers=headers, status_code=200)
    if response:
        data = response

        if output == "json":
            print(
                json.dumps(
                    data,
                    indent=2,
            ))
        
        if output == "table":
            table = Table("ID", "Name", "Function ID", "Read", "Write", "Modified", "Created")
            for cell in data:
                table.add_row(str(cell['id']), cell['name'], str(cell['fid']), str(cell['read']), str(cell['write']), cell['modified'], cell['created'])
            console.print(table)
    else:
        print(typer.style(f"ERROR:    {function}s {action} failed`", fg=typer.colors.RED))
        raise typer.Exit(code=1)

@app.command()
def assign(
        id: str = typer.Argument(..., help="ID of the assignment"),
        output: str = typer.Option("json", help="Set output format [json,table]"),
    ):
    """
    Get/Read assign by ID
    """

    function = "assign"

    headers = {
        'api-user': username,
        'api-password': password,
    }

    response = rest_get(url=url, path=f"{function}/{id}", headers=headers, status_code=200)
    if response:
        data = response

        if output == 'json':
            print(json.dumps(
                data,
                indent=2
            ))

        if output == 'table':
            table = Table("ID", "Role ID", "Group ID", "Modified", "Created")
            table.add_row(str(data['id']), str(data['rid']), str(data['gif']), data['modified'], data['created'])
            console.print(table)
            
    else:
        print(typer.style(f"ERROR:    {function} {id} {action} failed", fg=typer.colors.RED))
        raise typer.Exit(code=1)
    
@app.command()
def assignments(
        output: str = typer.Option("json", help="Set output format [json,table]"),
    ):
    """
    Get/Read all assignments
    """

    function = "assign"
    
    headers = {
        'api-user': username,
        'api-password': password,
    }

    response = rest_get(url=url, path=f"{function}/", headers=headers, status_code=200)
    if response:
        data = response

        if output == "json":
            print(
                json.dumps(
                    data,
                    indent=2,
            ))
        
        if output == "table":
            table = Table("ID", "Role ID", "Group ID", "Modified", "Created")
            for cell in data:
                table.add_row(str(cell['id']), str(cell['rid']), str(cell['gid']), cell['modified'], cell['created'])
            console.print(table)
    else:
        print(typer.style(f"ERROR:    {function}s {action} failed`", fg=typer.colors.RED))
        raise typer.Exit(code=1)
    
@app.command()
def user(
        id: str = typer.Argument(..., help="ID of the user"),
        output: str = typer.Option("json", help="Set output format [json,table]"),
    ):
    """
    Get/Read assign by ID
    """

    function = "user"

    headers = {
        'api-user': username,
        'api-password': password,
    }

    response = rest_get(url=url, path=f"{function}/{id}", headers=headers, status_code=200)
    if response:
        data = response

        if output == 'json':
            print(json.dumps(
                data,
                indent=2
            ))

        if output == 'table':
            table = Table("ID", "Name", "Modified", "Created")
            table.add_row(str(data['id']), data['name'], data['modified'], data['created'])
            console.print(table)
            
    else:
        print(typer.style(f"ERROR:    {function} {id} {action} failed", fg=typer.colors.RED))
        raise typer.Exit(code=1)
    
@app.command()
def users(
        output: str = typer.Option("json", help="Set output format [json,table]"),
    ):
    """
    Get/Read all assignments
    """

    function = "user"
    
    headers = {
        'api-user': username,
        'api-password': password,
    }

    response = rest_get(url=url, path=f"{function}/", headers=headers, status_code=200)
    if response:
        data = response

        if output == "json":
            print(
                json.dumps(
                    data,
                    indent=2,
            ))
        
        if output == "table":
            table = Table("ID", "Name", "Modified", "Created")
            for cell in data:
                table.add_row(str(cell['id']), cell['name'], cell['modified'], cell['created'])
            console.print(table)
    else:
        print(typer.style(f"ERROR:    {function}s {action} failed`", fg=typer.colors.RED))
        raise typer.Exit(code=1)