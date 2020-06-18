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
