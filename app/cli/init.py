import typer
import requests
import json
from rich.console import Console
import os
import crypto

err_console = Console(stderr=True)
console = Console()
app = typer.Typer()

def validate_settings():
    if not os.path.isfile("./settings.json"):
        err_console.print(typer.style("Error:    ./settings.json not found please run `python ss.py init settings`", fg=typer.colors.RED))
        return False
    return True

def read_settings():
    if validate_settings():
        file = open('settings.json')  
        data = json.load(file)
        file.close()
        return data
    else:
        return False

@app.command()
def settings():
    settings = {"keys":{}}
    settings["url"] = os.environ.get('SS_SERVER_URL') if os.environ.get('SS_SERVER_URL') != None else input("Enter Simple Secret Server URL: ")
    settings["keys"]["private"] = os.environ.get('SS_RSA_PRIVATE_KEY_FILE') if os.environ.get('SS_RSA_PRIVATE_KEY_FILE') != None else input("Path to RSA Private Key (leave blank to generate): ")
    settings["keys"]["public"] = os.environ.get('SS_RSA_PUBLIC_KEY_FILE') if os.environ.get('SS_RSA_PUBLIC_KEY_FILE') != None else input("Path to RSA Public Key (leave blank to generate): ")
    settings["username"] = os.environ.get('SS_USERNAME') if os.environ.get('SS_USERNAME') != None else input("Enter Simple Secret Server Username: ")
    settings["password"] = os.environ.get('SS_PASSWORD') if os.environ.get('SS_PASSWORD') != None else input("Enter Simple Secret Server Password: ")

    if settings["keys"]["private"] == "":
        keys = crypto.generate_keys()
        settings["keys"]["private"] = keys["private"].decode(encoding="UTF-8")
        settings["keys"]["public"] = keys["public"].decode(encoding="UTF-8")

    # Serializing json
    json_object = json.dumps(settings, indent=4)
 
    # Writing to sample.json
    with open("settings.json", "w") as outfile:
        outfile.write(json_object)
