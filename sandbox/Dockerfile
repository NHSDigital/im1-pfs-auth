FROM python:3.13

RUN touch __init__.py
RUN ls -a
RUN mkdir sandbox
COPY . /sandbox
RUN ls -a
RUN echo $PWD

RUN pip install uv && uv sync --project=sandbox/pyproject.toml

WORKDIR /sandbox

EXPOSE 9000

CMD ["uv", "run", "gunicorn", "api.app:app", "--bind=0.0.0.0:9000"]
RUN ls -a