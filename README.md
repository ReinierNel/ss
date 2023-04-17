# SS (Simple Secrets)

SS or Simple Secrets is a basic secrets manager with RBAC and user management

Why Create this? Well I needed something small for my home network that could store things securely like WIFI pre shared keys and other sensitive information that gets shared between different network appliances. For example I rotate my wifi password daily and using this I can generate a new pre shared key on the Access Point vai a script and send it to the secrets manager using curl, I can then from my phone or other devices retrieve this pre shared key securlay over HTTPS and my Private Key

Secrets are stored in the database as base64 encoded RSA Encryption strings.

Encryption can happen on the server (server side encryption or sse), the server encrypts the data using its public key and decrypts the data using its private key or the client can encrypt (client side encryption cse) the data  and send it on to the server (this why the server does not know what the secret is only the person with the keys does)

I have also created a basic RBAC (role based access control) system so that you can allow a user to read or write to a specific function based on the role, role assignment and group the user belongs to

for example admin user can read and write on all functions

a reader user with only reader access to the secrets can read secrets but not create them.

## Getting Started with the API

### Docker

Build and run docker image

```bash
cd app/api
docker build . -t ss:local
docker run --rm -d --name ss-api-server -p 8000:8000 ss:local
```

Exec into the docker image to find the temp admin user password

```bash
docker exec ss-api-server cat /app/README.md
```

> TBA

## Usage

> TBA

## Getting Started with the CLI

## Install

> TBA

## Usage

> TBA

## Contribute

### Potential Improvements

- Encrypt user hashes in DB
- Add Terraform Remote State endpoint (store terrform remote state as an encrypted secret basicly)
- Terraform provider
- Option to have the server generate a password for users
- Token based access to specific secret (rbac must be extend for this to work)
- Oauht2 / OpenID Support
- Refactor and Cleanup code (Sorry but I wrote this thing in a day so did not have time to stick to best practises)

## Thanks and Recognition

This API was built ontop of the following technologies, please give the authors of them some love and recognition for there work.

### FastAPI
    
- [Homepage](https://fastapi.tiangolo.com/)
- [Github](https://github.com/tiangolo/fastapi)

### Typer

- [Homepage](https://typer.tiangolo.com/)
- [Github](https://github.com/tiangolo/typer)

### PyCA Cryptography

- [Homepage](https://pypi.org/project/cryptography/)
- [Github](https://github.com/pyca/cryptography)

