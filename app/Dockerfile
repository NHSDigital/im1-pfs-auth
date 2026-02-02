FROM python:3.14.0-alpine

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

COPY . /app/
RUN find /app -type d -name "test*" -exec rm -rf {} + && \
    find /app -type f -name "test*" -exec rm -f {} + && \
    find /app -type f \( -name "*cache*" -o -name "*.cache*" -o -name ".pytest_cache*" -o -name ".ruff_cache*" \) -exec rm -f {} + && \
    find /app -type d \( -name ".pytest_cache" -o -name ".ruff_cache" \) -exec rm -rf {} +

ARG EMIS_BASE_URL
ARG TPP_BASE_URL

ENV EMIS_BASE_URL=${EMIS_BASE_URL}
ENV TPP_BASE_URL=${TPP_BASE_URL}

WORKDIR /app
ENV PYTHONPATH="/app:/"

RUN uv sync --project=app/pyproject.toml --only-group=app
RUN rm pyproject.toml uv.lock Dockerfile

EXPOSE 9000

CMD ["uv", "run", "gunicorn", "app.api.app:app", "--bind=0.0.0.0:9000"]
