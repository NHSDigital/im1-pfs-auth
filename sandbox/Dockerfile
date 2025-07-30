FROM python:3.13.5-alpine

RUN apk update && \
    apk upgrade && \
    apk add --no-cache python3 && \
    apk add --no-cache curl build-base

COPY . /sandbox

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /sandbox

RUN uv sync --project=sandbox/pyproject.toml

EXPOSE 9000

CMD ["uv", "run", "gunicorn", "api.app:app", "--bind=0.0.0.0:9000"]
