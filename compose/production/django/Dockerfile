# Front-end build stage: compiles Sass and minifies JS into pycon_portugal_2027/static
FROM docker.io/node:26-trixie-slim AS client-builder

ARG APP_HOME=/app
WORKDIR ${APP_HOME}

COPY ./package.json ./package-lock.json ${APP_HOME}/
RUN npm ci && npm cache clean --force
COPY ./pycon_portugal_2027/static ${APP_HOME}/pycon_portugal_2027/static
RUN npm run build


# Python build stage: installs the locked dependencies into /app/.venv
FROM ghcr.io/astral-sh/uv:python3.14-trixie-slim AS python-build-stage

ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy UV_PYTHON_DOWNLOADS=0

ARG APP_HOME=/app
WORKDIR ${APP_HOME}

RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-install-project --no-dev

COPY . ${APP_HOME}
COPY --from=client-builder ${APP_HOME}/pycon_portugal_2027/static ${APP_HOME}/pycon_portugal_2027/static

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-dev


# Run stage
FROM docker.io/python:3.14-slim-trixie AS python-run-stage

ARG APP_HOME=/app
WORKDIR ${APP_HOME}

RUN addgroup --system django \
  && adduser --system --ingroup django django

COPY --chown=django:django ./compose/production/django/start /start
RUN sed -i 's/\r$//g' /start && chmod +x /start

# Copy the application (including the virtualenv) from the builder
COPY --from=python-build-stage --chown=django:django ${APP_HOME} ${APP_HOME}
RUN chown django:django ${APP_HOME}

ENV PATH="/app/.venv/bin:$PATH"

USER django

CMD ["/start"]
