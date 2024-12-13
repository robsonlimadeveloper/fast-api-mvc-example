
# API MVC example

[![Python](https://badgen.net/badge/language/python/orange?icon=python)]()
[![Fast API](https://badgen.net/badge/framework/fastapi/red?icon=)]()

_**Simple example of Fast API using MVC and  microservices elements architecture, the application contained here develops some
functionalities for accessing the database and creating models and tests.
Below are the steps required to run the database and the application backend
locally._

### Prerequisites

*_**[Docker Desktop](https://www.docker.com/products/docker-desktop/)**_ installed on the environment.* (Windows)

or

*_**[Docker Engine and Compose](https://docs.docker.com/engine/install/ubuntu/)**_ installed on the environment.* (Linux)

### Installation

Build project

```sh
$ docker-compose up --build -d
```

### API Documentation
```
http://localhost:4010/docs/
```

```
http://localhost:4010/redoc/
```

### Run tests (pytest)

```sh
$ docker exec -it api bash

@container $ pytest

```

### Access container database


```sh
$ docker exec -it db bash
```

```sh
@container $ psql -U postgres -p 5432
```