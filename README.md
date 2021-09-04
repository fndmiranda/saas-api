# Python SaaS application boilerplate (asynchronous)

This project simplifies the creation of a Python SaaS api with the FastAPI framework and SQLAlchemy.

* FastAPI framework
* SQLAlchemy (asynchronous) SQL toolkit and Object Relational Mapper
  * PostgreSQL
  * MySQL
  * Oracle
  * Microsoft SQL Server
  * SQLite
* Alembic database migration tool
* Authentication with OAuth2
* Account
  * User Account Crud
  * Email password recovery feature
  * Registration email verification
* Notification
  * Strategy for notifications
* Store
  * Permissions control for owner
  * Store segment
* Address
  * Address with a so-called "generic foreign key" to accounts and stores
                                                                                                                        
## Installation

### Virtualenv

Create a Python version 3.9 environment and activate it.

### Install dependencies

Execute the following commands to install dependencies:

```terminal
$ make requirements-dev
```

in production

```terminal
$ make requirements
```

### Configure the application environment

Copy and edit the .env file as needed.

```terminal
$ cp .env.example .env
```

### Run migrations

Execute the following command to create a migration:

```terminal
$ alembic revision -m "Create catalog_products table"
```

The migrations will be created in the `alembic/versions` folder.

Execute the following command to upgrade to last revision:

```terminal
$ alembic upgrade head
```

Execute the following command to downgrade version:

```terminal
$ alembic downgrade -1
```

Execute the following command to display the current revision for a database.

```terminal
$ alembic current
```

Execute the following command to list the history of migrations:

```terminal
$ alembic history
```

### Run application

Execute the following command to run the application in a development environment:

```terminal
$ make runserver-dev
```

Execute the following command to run the application with gunicorn:

```terminal
$ make runserver
```

## Display registered routes.

Execute the following command to list all registered routes:

```terminal
$ make show-routes
