# simple_database_py
Client-server simple database

Stable version branch: `1.0_flask_rest_version` (runs on Flask and REST API, using JSON file as storage).

Current version branch:

This database runs on `FastAPI` and `PostgreSQL` with `asyncio`.

You can view contents by HTTP server's link (server side).

Other methods for working with the database can be called by the client from the client application.

- [Quick start](#quick-start)

  - [Required](#required)

  - [Server](#server)

  - [Client](#client)

  - [Autotest](#autotest)

- [Code architecture](#code-architecture)

## Quick start
To use the client application, you must first start the server.

### Required
#### Python 3
Python must be installed to run the application.
The required packages are listed below.
#### Tools
```
pip install fastapi uvicorn asyncpg
```

### Server
Start
```
cd server
python api.py [--host <host>] [--port <port>] [--db <database>] [--db-user <user>] [--db-pass <password>]
```
Stop
```
ctrl + c
```

### Client
Before starting the client, you must first start the server.

The server's `host` and `port` must match the client's `URL`.

Start
```
cd client
python client.py [--url <url>]
```
Stop
```
ctrl + c
```

### Autotest
`test.py` checks server side. `test_validation.py` checks client side (validation).

To run `test_validation.py`, you don't need to start the server.

To run `test.py`, you must first start the server.

The server's `host` and `port` must match the test's `URL`.

Start
```
cd autotest
python test.py [--url <url>]
python -m pytest test_validation.py -v
```
Stop
```
ctrl + c
```

## Code architecture
The `server` folder contains the code files for server operation.

The `client` folder contains the files for client operation.

The `autotest` folder contains tests used to verify the application's correct operation.