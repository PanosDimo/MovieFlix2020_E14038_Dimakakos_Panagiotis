# MovieFlix

## Run Setup

### Requirements

- [docker](https://docs.docker.com/engine/)
- [docker-compose](https://docs.docker.com/compose/)

### Configure

```bash
cp .docker.env.example .docker.env
```

You can edit `.docker.env` to your liking.

### Start

```bash
docker-compose --env-file=.docker.env up -d
```

### Logs

```bash
docker-compose logs -f [mongodb/application]
```

### Stop

```bash
docker-compose down
```

## Documentation

If you follow the steps above, then the next will be setup:

- Mongo database listening on port 27017 (initialized with some data).
- Flask application listening on port 5000.

### Enter MongoDB

```bash
docker-compose exec mongodb mongo -u admin -p admin
```

The database contains 4 collections:

- users
- movies
- comments (used as a helper)
- ratings (used as a helper)

### Use Application

By default an administrator is created automatically for the application. The default credentials
are:

- email: admin@movieflix.com
- password: admin

### API

#### Authenticate

- Endpoint: `/users/authenticate`
- Type: POST
- JSON Request:
  - email: string
  - password: string
- JSON Response:
  - id: string
  - name: string
  - token: string
  - category: "ADMIN" | "USER"

The token is a standard `JWT` Bearer token, which must be used in the Authorization header of all
subsequent requests in order for the system to understand which user makes the request.

##### Example

```bash
curl --location --request GET '/movies' \
--header 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1OTM4MDc1NDksImlhdCI6MTU5MzgwMzk0OSwicGF5bG9hZCI6eyJfaWQiOiIyODlmMWMyOC05ZGMxLTRiY2YtYWY0YS1iOWU5ODc5NGY4NzUifX0.I8pau0q9OT_AeZRRsrfYsYDSr6INsEZWfhSsGFmnL9c'
```

#### Register

- Endpoint: `/users/register`
- Type: POST
- JSON Request:
  - email: string
  - name: string
  - password: string
- JSON Response:
  - id: string
  - email: string
  - name: string
  - category: "USER"

#### Search Movies

- Endpoint: `/movies`
- Type: GET
- Query Parameters:
  - title: string
  - year: int
  - actors: comma delimited list
- JSON Response:
  - movies: Object[]
    - movies.id: string
    - movies.title: string
    - movies.year: int
    - movies.rating: float

#### Get Movie

- Endpoint: `/movies/:id`
- Type: GET
- JSON Response:
  - title: string
  - year: int
  - rating: float
  - description: string
  - actors: string[]

#### Get Movie Comments

- Endpoint: `/movies/:id/comments`
- Type: GET
- JSON Response:
  - comments: Object[]
    - comments.comment: string
    - comments.user: string

#### Comment Movie

- Endpoint: `/movies/:id/comment`
- Type: POST
- JSON Request:
  - comment: string

#### Rate Movie

- Endpoint: `/movies/:id/rate`
- Type: POST
- JSON Request:
  - rating: float

#### Remove My Movie Rating

- Endpoint: `/movies/:id/rate`
- Type: DELETE

#### Get My Comments

- Endpoint: `/users/my/comments`
- Type: GET
- JSON Response:
  - comments: Object[]
    - comments.id: string
    - comments.comment: string
    - comments.movie: string

#### Delete My Comment

- Endpoint: `/users/my/comments/:id`
- Type: DELETE

#### Get My Ratings

- Endpoint: `/users/my/ratings`
- Type: GET
- JSON Response:
  - ratings: Object[]
    - ratings.id: string
    - ratings.rating: float
    - ratings.movie: string

#### Delete My Account

- Endpoint: `/users/my/account`
- Type: DELETE

**The following endpoints can only be used by admin users.**

#### Create Movie

- Endpoint: `/movies`
- Type: POST
- JSON Request:
  - title: string
  - year: int
  - description: string
  - actors: string[]

#### Update Movie

- Endpoint: `/movies/:id`
- Type: PUT
- JSON Request:
  - title: string [optional]
  - year: int [optional]
  - description: string [optional]
  - actors: string[][optional]

#### Delete Movie

- Endpoint: `/movies/:id`
- Type: DELETE

#### Get Users

- Endpoint: `/users`
- Type: GET
- JSON Response:
  - users: Object[]
    - users.id: string
    - users.name: string
    - users.email: string
    - users.category: "ADMIN" | "USER"

#### Get Comments

- Endpoint: `/users/comments`
- Type: GET
- JSON Response:
  - comments: Object[]
    - comments.id: string
    - comments.comment: string
    - comments.user: string
    - comments.movie: string

#### Delete Comment

- Endpoint: `/users/comments/:id`
- Type: DELETE

#### Make Admin

- Endpoint: `/users/:id/admin`
- Type: POST

#### Delete User

- Endpoint: `/users/:id`
- Type: DELETE

## Development Setup

### Requirements

- [python](https://www.python.org/downloads/) >= 3.8
- [pyenv](https://github.com/pyenv/pyenv) >= 1.2
- [poetry](https://github.com/python-poetry/poetry) >= 1.0
- [virtualenv](https://github.com/pypa/virtualenv) >= 20.0

### Install Python

```bash
pyenv install 3.8.3
```

### Set Python

```bash
pyenv local 3.8.3
```

### Create Virtual Environment

```bash
virtualenv .venv
```

### Activate Environment

```bash
source .venv/bin/activate
```

### Install Dependencies

```bash
poetry install
```

### Deactivate Environment

```bash
deactivate
```
