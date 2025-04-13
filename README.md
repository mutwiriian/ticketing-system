A task management API built with [FastAPI](https://fastapi.tiangolo.com/) and [SQLALchemy](https://www.sqlalchemy.org/) toolkit on Postgresql database

Implements async CRUD operations for User, Events, Tickets Sponsors and Sponsorships

Features custom authentication and database migrations with [Alembic](https://alembic.sqlalchemy.org/en/latest/tutorial.html)

## Getting started
To experiment with the code open a Linux terminal and follow the following steps.

### Clone repo
```
git clone https://github.com/mutwiriian/ticketing-system.git
```

### Create and activate a environment using [uv](https://github.com/astral-sh/uv)
```
uv init
```

```
source .venv/bin/activate
```

### Install required packages
```
uv pip install -r requirements.txt
```

### Initialize a [PostgreSQL](https://www.postgresql.org/) database
Set up and start a PostgreSQL database server and adjust the connections strings in _.env_ file accordingly

### Start app
```
cd app
```

### Then run
```
uvicorn main:app --reload
```

Visit *https://localhost:8000/docs* to interact with the API using (https://swagger.io/tools/swagger-ui/)[Swagger]

