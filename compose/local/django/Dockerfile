FROM ghcr.io/astral-sh/uv:python3.14-trixie-slim

ARG APP_HOME=/app
WORKDIR ${APP_HOME}

# The virtualenv lives in /app/.venv and is masked from the bind mount by docker compose.
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy UV_PYTHON_DOWNLOADS=0

# Requirements are installed here to ensure they will be cached.
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    uv sync --locked --no-install-project

COPY . ${APP_HOME}

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked

ENV PATH="${APP_HOME}/.venv/bin:$PATH"

COPY ./compose/local/django/start /start
RUN sed -i 's/\r$//g' /start && chmod +x /start
