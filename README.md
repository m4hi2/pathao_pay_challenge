# Pathao Pay Challenge

A simple API to manage small digital wallet.

Challenge details can be found [here](https://hackmd.io/@1MIwEmEqR4-Xr_2ikkvoLQ/BJecoIMNi#Backend-Developer-Challenge)

## How to run?

The application is fully dockerized, with infrastucture(db). To run simply run:

```shell
docker compose up -d
```

Please make sure, port `8000` and `5438` are not occupied.

The api base should be accessible at [localhost:8000](http://127.0.0.1:8000) once the containers have been started.

## Where is the API documentation?

API documentation is generated with Swagger. Those are accessible at [Swagger Documentation](http://127.0.0.1:8000/docs) or [Redocly](http://127.0.0.1:8000/redoc) once the docker containers are running.

## Important Notes about authentication

For the authentication form, the default FastAPI OAuth form is used, this has caused some trouble in terminology.
`username` -> `email` in our system.
`password` -> `pin` in out sysmte.

## Some decisions

- All balance in system is stored as integers
  - This is done to prevent floating point arithmetic and rounding erros

## Things to improve

- For some reason api docekr container starts before db container, even after using depends
- User.transaction relationship doesn't work, gathering user transactions directly from transaction table
- For system wallet, the sum is done in python code, should do it using sql sum fucntion
- Proper logging
- Exceptions and crash monitoring with service like sentry.io
- Have to write tests
- The HTTPExceptions raised didn't make to Swagger documentation, have to look into that

## Chosen Techstack

- Language: Python
- Web Framework: FastAPI + SQLAlchemy
- Database: PostgreSQL
- Containerization: Docker
- Container Orchestration: Docker Compose

### Reason behind chosen stack

- Language (Python): Familiarity
- Web Framework (FastAPI): Type support + Auto OpenAPI documentation generation + Easy OAuth2 workflow
- Database (PostgreSQL): ACID complient, Relational Databse management system (to satisfy challenge requirement)
- Containerization (Docker): To satisfy challenge requirement
- Container Orchestration (Docker Compose): Ease of use, my current laptop is too slow to run a local cluster of minicube.
