
<h1 align="center">
  <br>
   API MVC example
  <br>
</h1>

<p align="center">  
<img src="https://badgen.net/badge/language/python/yellow?icon=python">
<img src="https://badgen.net/badge/framework/fastapi/pink?icon=">
<img src="https://badgen.net/badge/orm/sqlalchemy/red?icon=">
<img src="https://badgen.net/badge/database/postgresql/blue?icon=">
<img src="https://badgen.net/badge/tests/pytest/blue?icon=">
</p>

<p align="justify">
Simple example of <strong>FastAPI</strong> using <strong>MVC</strong> and microservices elements architecture, the application contained here develops some
functionalities for accessing the database and creating models and tests.
Below are the steps required to run the database and the application backend
locally.
</p>


The proposed structure is described as follows:

```
/app
	__init__.py
	/modules
		__init__.py
		/module_1/
			__init__.py
			dto.py
			model.py
			repository.py
			service.py
			view.py
		/module_2/
			dto.py
			model.py
			repository.py
			service.py
			view.py
		/config
			__init__.py
		/seeds
			seed_module_1.py
			seed_module_2.py
			seeder.py
/tests
.env
.gitignore
docker-compose.yml
Dockerfile
README.md
requirements.txt
```

## Prerequisites

*_**[Docker Desktop](https://www.docker.com/products/docker-desktop/)**_ installed on the environment.* (`Windows`)


*_**[Docker Engine and Compose](https://docs.docker.com/engine/install/ubuntu/)**_ installed on the environment.* (`Linux`)

## Installation

Build project

```sh
$ docker-compose up --build -d
```

## API Documentation
```
http://localhost:4010/api/docs/
```

```
http://localhost:4010/api/redoc/
```

## Run tests (pytest)

```bash
$ docker exec -it api bash
```

```bash
@container $ pytest --capture=no -s -v
```

## Access container database


```bash
$ docker exec -it db bash
```

```bash
@container $ psql -U postgres -p 5432
```

## License

[MIT](LICENSE) - Robson Soares - 2024