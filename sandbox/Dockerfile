FROM python:3.13.5-alpine

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

COPY . /app/
RUN find /app -type d -name "test*" -exec rm -rf {} + && \
    find /app -type f -name "test*" -exec rm -f {} +

WORKDIR /app

RUN uv sync --project=app/pyproject.toml --only-group=sandbox
RUN rm pyproject.toml uv.lock

EXPOSE 9000

CMD ["uv", "run", "gunicorn", "api.app:app", "--bind=0.0.0.0:9000"]
