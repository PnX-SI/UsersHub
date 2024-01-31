# syntax=docker/dockerfile:1.2

ARG DEPS=build

FROM python:3.9-bullseye AS build

ENV PIP_ROOT_USER_ACTION=ignore
RUN --mount=type=cache,target=/root/.cache \
    pip install --upgrade pip setuptools wheel


FROM build AS build-usershub-auth-module

WORKDIR /build/
COPY /dependencies/UsersHub-authentification-module .
RUN python setup.py bdist_wheel


FROM build AS build-usershub

WORKDIR /build/
COPY /setup.py .
COPY /requirements-common.in .
COPY /requirements-dependencies.in .
COPY /VERSION .
COPY /MANIFEST.in .
COPY /README.rst .
COPY /LICENSE .
COPY /app ./app
COPY /config/docker_config.py ./app/config.py
RUN python setup.py bdist_wheel


FROM node:alpine AS node

WORKDIR /dist/
COPY /app/static/package*.json .
RUN --mount=type=cache,target=/root/.npm \
    npm ci --omit=dev


FROM python:3.9-bullseye AS dev

WORKDIR /dist/

RUN python -m venv /dist/venv
ENV PATH="/dist/venv/bin:$PATH"

RUN --mount=type=cache,target=/root/.cache \
    pip install --upgrade pip setuptools wheel

COPY /setup.py .
COPY /requirements-common.in .
COPY /requirements-dependencies.in .
COPY /VERSION .
COPY /MANIFEST.in .
COPY /README.rst .
COPY /LICENSE .
COPY /dependencies/ ./dependencies/
COPY /requirements-dev.txt .
RUN --mount=type=cache,target=/root/.cache \
    pip install -e . -r requirements-dev.txt

COPY ./config/docker_config.py ./config.py
ENV USERSHUB_SETTINGS=/dist/config.py

ENV FLASK_APP=app.app:create_app
CMD ["flask", "run", "--host", "0.0.0.0", "--port", "5001"]


FROM python:3.9-bullseye AS app
RUN --mount=type=cache,target=/root/.cache \
    pip install --upgrade pip setuptools wheel

WORKDIR /dist/

ENV PIP_ROOT_USER_ACTION=ignore
RUN --mount=type=cache,target=/root/.cache \
    pip install --upgrade pip setuptools wheel

COPY --from=node /dist/node_modules ./static/node_modules

COPY /app/static ./static

FROM app AS app-build

COPY /requirements-dev.txt .
RUN sed -i 's/^-e .*/# &/' requirements-dev.txt
RUN --mount=type=cache,target=/root/.cache \
    pip install -r requirements-dev.txt

COPY --from=build-usershub-auth-module /build/dist/*.whl .
COPY --from=build-usershub /build/dist/*.whl .
RUN --mount=type=cache,target=/root/.cache \
    pip install *.whl


FROM app AS app-pypi

COPY /requirements.txt .
RUN --mount=type=cache,target=/root/.cache \
    pip install -r requirements.txt

COPY --from=build-usershub /build/dist/*.whl .
RUN --mount=type=cache,target=/root/.cache \
    pip install *.whl


FROM app-${DEPS} AS prod

ENV FLASK_APP=app.app:create_app
ENV PYTHONPATH=/dist/config/
ENV USERSHUB_SETTINGS=config.py
ENV USERSHUB_STATIC_FOLDER=/dist/static

EXPOSE 5001

CMD ["gunicorn", "app.app:create_app()", "--bind=0.0.0.0:5001", "--access-logfile=-", "--error-logfile=-", "--reload", "--reload-extra-file=config/config.py"]
