# simple_database_py
Client-server simple database

- [Quick start]((#Quick-start))

  - [Required]((##Required))

  - [Server]((##Server))

  - [Client]((##Client))

  - [Autotest]((##Autotest))

- [Code architecture]((##Code-architecture))

## Quick start
To use the client application, you must first start the server. To run automated tests, you must first start the server.

### Required
#### Python 3
Python must be installed to run the application.
The required packages are listed below.
#### Flask
```
pip install flask
```

### Server
Start
```
cd server
python api.py
```
Stop
```
ctrl + c
```

### Client
Start
```
cd client
python client.py
```
Stop
```
ctrl + c
```

### Autotest
Start
```
cd autotest
python test.py
```
Stop
```
ctrl + c
```

## Code architecture
The `server` folder contains the code files for server operation and the database itself in JSON format.

The `client` folder contains the files for client operation.

The `autotest` folder contains tests used to verify the application's correct operation.