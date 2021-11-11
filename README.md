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
  * Email password recovery
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
```

## Pagination with dynamic filter and sorting.

Pass the `filter` field in query string, as in the example:

`[{"field":"foo", "op":"ilike", "value":"%bar%"}]`

Operators options are:

`is_null, is_not_null, eq, ne, gt, lt, ge, le, like, ilike, not_ilike, in, not_in, any, not_any`

Pass the `sort` field in query string, as in the example:

`[{"field":"foo", "direction":"asc"}]`

## Api documentation

The base address of RESTful API is [http://localhost:8000](http://localhost:8000)
and Swagger documentation is [http://localhost:8000/docs](http://localhost:8000/docs)

## Display registered routes.

Execute the following command to list all registered routes:

```terminal
$ make show-routes
```

## Outdated packages

Execute the following command to list outdated packages:

```terminal
$ make outdated
```

## Celery

Execute the following command to run celery task queues:

```terminal
$ make runcelery
```

Execute the following command to run flower:
Flower is a web based tool for monitoring and administrating Celery clusters

```terminal
$ make runflower
```

## Testing

### Unit tests

Execute the following command to run all tests:

```terminal
$ make test
```

Execute the following command to run test with name match, example:

```terminal
$ make test-matching test=test_store_view_should_get_segments
```

Execute the following command to run celery task queues in tenting mode:

```terminal
$ make runcelery-test
```

Execute the following command to run test with coverage reports, example:

```terminal
$ make coverage
```

## Lint

Execute the following command to check lint:

```terminal
$ make check-lint
```

Execute the following command to try fix lint:

```terminal
$ make lint
```

## Security

Execute the following command to check security vulnerabilities in packages:

```terminal
$ make check-safety
```

If you discover any security related issues, please email fndmiranda@gmail.com instead of using the issue tracker.

## License

The MIT License (MIT). Please see [License File](LICENSE.md) for more information.