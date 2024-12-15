
<h1 align="center">
  <br>
   FastAPI MVC Example
  <br>
</h1>

<p align="center">  
<img src="https://badgen.net/badge/language/python/yellow?icon=python">
<img src="https://badgen.net/badge/framework/fastapi/pink?icon=">
<img src="https://badgen.net/badge/orm/sqlalchemy/red?icon=">
<img src="https://badgen.net/badge/database/postgresql/blue?icon=">
<img src="https://badgen.net/badge/tests/pytest/blue?icon=">
</p>
<p align="center">
<a href='https://ko-fi.com/V7V717GRV1' target='_blank'><img height='36' style='border:0px;height:36px;' src='https://storage.ko-fi.com/cdn/kofi2.png?v=6' border='0' alt='Buy Me a Coffee at ko-fi.com' /></a>
</p>

<p align="justify">
A simple and scalable FastAPI project following the MVC (Model-View-Controller) pattern with elements of a microservices architecture. This application demonstrates core functionalities such as database access, model creation, and automated testing.
Below are the steps required to run the database and the application backend
locally.
</p>

<p><strong>Develop with:</strong></p>

<p align="left">
	
  <a href="https://skillicons.dev">
    <img src="https://skillicons.dev/icons?i=python,fastapi,postgres,git,docker,vscode" />
  </a>
</p>
<p align="left">
<strong>Existing Features:</strong> 🚀 

✅ Clean Architecture: Well-organized file structure for easy maintenance and scalability.

✅ Ready-to-Use Configuration: Pre-configured for both development and production environments.

✅ SQLAlchemy Database Management: Robust model handling and database operations.

✅ Well-Defined RESTful APIs: Ready-to-use CRUD and authentication endpoints.

✅ Integrated Documentation: Swagger and Redoc for easy API exploration.

</p>
The proposed structure is described as follows:

```
/app
    __init__.py
    main.py
    /modules
            __init__.py
            /module_1/
                     __init__.py
                     exceptions.py
		     dto.py
		     model.py
		     repository.py
		     service.py
		     views.py
	    /module_2/
                     __init__.py
                     exceptions.py
		     dto.py
		     model.py
		     repository.py
		     service.py
		     views.py
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

## Getting Started:

Follow the steps below to set up and run the database and backend application locally.

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
