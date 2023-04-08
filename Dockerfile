FROM python:3.8-slim

WORKDIR /app

RUN pip install poetry

COPY pyproject.toml ./
RUN poetry config virtualenvs.create false && \
    poetry install --no-dev

COPY app app

CMD ["python", "app/main.py"]