FROM python:3.8.3-slim

WORKDIR /app

# Install Poetry.
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | POETRY_HOME=/opt/poetry python
RUN ln -s /opt/poetry/bin/poetry /usr/local/bin
RUN poetry config virtualenvs.create false

# Copy poetry lock.
COPY pyproject.toml poetry.lock /app/

# Install dependencies.
RUN poetry install --no-dev --no-root

# Copy application.
COPY . /app/

ENTRYPOINT ["gunicorn", "-c", "gunicorn.conf.py", "movieflix.app:create_app()"]
