A task management API built with (https://fastapi.tiangolo.com/)[FastAPI] and (https://www.sqlalchemy.org/)[SQLALchemy] toolkit on Postgresql database

Implements CRUD operation for User, Events, Tickets Sponsors and Sponsorships

Features custom authentication and database migrations with (https://alembic.sqlalchemy.org/en/latest/tutorial.html)[Alembic]

## Getting started
To experiment with the code open a Linux terminal and follow the following steps.

### Clone repo
```
git clone 
```

### Create and activate a environment using (https://github.com/astral-sh/uv)[uv]
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

### Initialize a Postgresql database
Start a postgres and adjust the connections strings in _.env_ file accordingly

### Start app
```
cd app
```

### Then run
```
uvicorn main:app --reload
```

Visit *https://localhost:8000/docs* to integrate with the API using (https://swagger.io/tools/swagger-ui/)[Swagger]

