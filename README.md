# database-connector-kit

This python module handles any type of databases connection(s) using a yaml configuration file.

It is a fork coming from [fastapi-framework-mvc](https://pypi.org/project/fastapi-framework-mvc/) and [flask-framework-mvc](https://pypi.org/project/flask-framework-mvc/).

Created for better package management in between both projects.

Can be loaded standalone outside its original projects.

> [!NOTE] 
> If using side by side with either [fastapi-framework-mvc](https://pypi.org/project/fastapi-framework-mvc/) or [flask-framework-mvc](https://pypi.org/project/flask-framework-mvc/), it will load Environment from one of this framework accordingly to the one you installed int your python env or python root libs.

### Default database with builtin driver in sqlalchemy 

```yaml
...
DATABASES: 
  default: mysql
  mysql: 
    driver: mysql+pymysql
    user: "replace this with your database user"
    password: "replace this with your database user's password"
    database: "replace this with your database name"
    address: "replace this with your hostname"
    models: "mysql (python module that require to be put under models.persistant module)"
    readonly: false
...
```

### Default database with non builtin driver in sqlalchemy 

```yaml
...
DATABASES:
  informix:
    driver: informix
    user: "replace this with your database user"
    password: "replace this with your database user's password"
    database: "replace this with your database name"
    address: "replace this with your hostname"
    models: "informix (python module that require to be put under models.persistent module)"
    params:
      SERVER: "replace with your server name"
      CLIENT_LOCALE: "replace with your client locale"
      DB_LOCALE: "replace with your server locale"
    dialects:
      informix: 
        module: IfxAlchemy.IfxPy
        class: IfxDialect_IfxPy
      informix.IfxPy: 
        module: IfxAlchemy.IfxPy
        class: IfxDialect_IfxPy
      informix.pyodbc: 
        module: IfxAlchemy.pyodbc
        class: IfxDialect_pyodbc
    readonly: false
...
```

or:

```yaml
...
DATABASES:
  bigquery:
    driver: bigquery
    user: "replace this with your database user"
    password: "replace this with your database user's password"
    database: "replace this with your database name"
    address: "replace this with your hostname"
    models: "bigquery (python module that require to be put under models.persistent module)"
    readonly: false
    engine:
      location: US
      
...
```

__dialects__, __params__ and __engine__ are non mandatory within the yaml config file.

__dialects__ are for registering database dialects base what the python database lib provides.

__params__ are for putting additional params within the database url link used when sqlalchemy create_engine function is called

__engine__ is all other arguments that can be given to the sqlalchemy create_engine function

### Loading configuration

In order to load it you need to create a yaml configuration file with entries as described on sections bellow.
This yaml configuration files can have environment variable within encapsuled in ${ENVIRONMENT_NAME} syntax.

````python
import os
from database_connector_kit.config import Environment
Environment.load('config.yml')
````

### Usage

After loading the configuration file, you can create the database's connection(s) by:

````python
from database_connector_kit import Driver
Driver.register_engines()
Driver.init()
````

There is a __safe__ decorator that enable some sqlalchemy errors to be dealt with and retry reprocessing the function 
that handles database operations.
In order to use it, use de following example:

````python
from database_connector_kit import safe

@safe
def func():
    """
    Function that update, select, insert ot even delete contents from the database
    """
    pass
````

