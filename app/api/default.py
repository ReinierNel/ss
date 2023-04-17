import crud, models, schemas, crypto
from database import SessionLocal, engine
import random
import string

models.Base.metadata.create_all(bind=engine)

def get_random_string(length: int):
    result = ''.join(random.choice(string.ascii_letters) for i in range(length))
    return result

def init():
    # init defaults data
    finctions_list = [
        "group",
        "member",
        "role",
        "assign",
        "user",
        "secret"
    ]

    server_keys = crypto.generate_keys()

    settings_list = {
        'public_key': server_keys["public"].decode("UTF-8"),
        'private_key': server_keys["private"].decode("UTF-8"),
        'initialized': "true"
    }

    admin_roles = {
        'admin-rw-groups': {
            'fid': 0,
            'create': True,
            'read': True,
            'update': True,
            'delete': True
        },
        'admin-rw-member': {
            'fid': 1,
            'create': True,
            'read': True,
            'update': True,
            'delete': True
        },
        'admin-rw-role': {
            'fid': 2    ,
            'create': True,
            'read': True,
            'update': True,
            'delete': True
        },
        'admin-rw-assign': {
            'fid': 3    ,
            'create': True,
            'read': True,
            'update': True,
            'delete': True
        },
        'admin-rw-user': {
            'fid': 4    ,
            'create': True,
            'read': True,
            'update': True,
            'delete': True
        },
        'admin-rw-secret': {
            'fid': 5    ,
            'create': True,
            'read': True,
            'update': True,
            'delete': True
        }
    }

    db = SessionLocal()
    check = False
    try:
        initialized = crud.read_setting_by_name(db, name="initialized")
        if initialized.value == "true":
            check = True
    except:
        check = False

    if check:
        print("default settings already initialized")
    else:
        print("initializing default settings")
        # add settings
        for setting in settings_list:
            try:
                crud.create_setting(db, setting, settings_list[setting])
            except:
                pass
        
        # add functions
        for id, function in enumerate(finctions_list):
            try:
                crud.create_function(db, id, function)
            except:
                pass
        
        # add admin roles
        for role in admin_roles:
            crud.create_role(
                db,
                schemas.Role(
                    name=role,
                    fid=admin_roles[role]["fid"],
                    create=admin_roles[role]["create"],
                    read=admin_roles[role]["read"],
                    update=admin_roles[role]["update"],
                    delete=admin_roles[role]["delete"],
                )
            )

        # add admin group
        try:
            crud.create_group(db, schemas.Group(name="admins"))
        except:
            pass

        # add admin user
        rand_pwd = get_random_string(32)
        rand_pwd_file = open("README.md", "a")
        curl_body = '{ "id": 1, "name": "admin", "hash": "[SS_API_SERVER_ADMIN_NEW_PASSWORD]" }'
        rand_pwd_file.write(f"""
# First Start Readme

## Admin credential

- username: admin
- password: {rand_pwd}

## Authentication headers

- 'api-user': username,
- 'api-password': password,

## !!! Important !!!

Fist thing to do before anyting elase is to reset the admin users password

### Using Curl

replace `[SS_API_SERVER_DOMAIN_NAME]` with your domain name or IP address

replace `[SS_API_SERVER_PORT_NUMBER]` with your port number

replace `[SS_API_SERVER_ADMIN_NEW_PASSWORD]` with your won new password recommend 32 characters in length

Strongly recommended you use TLS if not update the protocol to http:// instead of https://

```bash
curl -X 'PUT' \\
'https://[SS_API_SERVER_DOMAIN_NAME]:[SS_API_SERVER_PORT_NUMBER]/user/' \\
-H 'accept: application/json' \\
-H 'api-user: admin' \\
-H 'api-password: {rand_pwd}' \\
-H 'Content-Type: application/json' \\
-d '{curl_body}'
```

""")
        rand_pwd_file.close()
        crud.create_user(db, schemas.User(name="admin", hash=rand_pwd))

        # member admin user to admins group
        try:
            crud.create_member(db, schemas.Member(gid=1, uid=1))
        except:
            pass
        try:
            crud.create_assign(db, schemas.Assign(rid=1, gid=1))
            crud.create_assign(db, schemas.Assign(rid=2, gid=1))
            crud.create_assign(db, schemas.Assign(rid=3, gid=1))
            crud.create_assign(db, schemas.Assign(rid=4, gid=1))
            crud.create_assign(db, schemas.Assign(rid=5, gid=1))
            crud.create_assign(db, schemas.Assign(rid=6, gid=1))
        except:
            pass

    db.close()
