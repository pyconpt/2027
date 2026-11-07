# PyCon Portugal 2027

Website for PyCon Portugal 2027, 22–24 April 2027 in Leiria, Portugal: <https://2027.pycon.pt>

A small Django site that renders Markdown files. There is no database, no authentication and no
user generated content: Django is only used for templates, URL routing and static files.

## How the site works

- Pages are Markdown files under `pycon_portugal_2027/content/<menu>/<submenu>/`. Every `.md` file in a
  folder is rendered, in alphabetical order, at `/<menu>/<submenu>/`. Each file starts with a front-matter
  block between `---` lines; its `layout:` key selects the wrapper in `templates/modules/layout/`
  (`simple` or `centered`).
- The navigation menu, event links (tickets, CFP) and social links live in
  `pycon_portugal_2027/site/context_processors.py`.
- The home page is a regular template: `templates/pages/home.html`.
- Styles are Sass in `pycon_portugal_2027/static/sass/` (design tokens in `_base.scss`) and are compiled
  into `static/css/project.min.css`; `static/js/project.js` is minified into `project.min.js`. Both
  compiled files are committed, so Python-only setups work without Node.
- Fonts (Boldonse, Cabin) are loaded from [Bunny Fonts](https://fonts.bunny.net/).

## Local development

Without Docker:

    uv sync
    uv run python manage.py runserver

To change styles or scripts:

    npm install
    npm run build        # compile Sass + minify JS once
    npm run watch        # recompile Sass on change

With Docker:

    make up              # or: docker compose -f docker-compose.local.yml up
    make manage check

### Tests, linting and type checks

    uv run pytest
    uv run ruff check .
    uv run mypy pycon_portugal_2027 config

### Dependencies

Python dependencies are pinned in `pyproject.toml` and locked in `uv.lock` (`uv lock`).
Front-end build dependencies are in `package.json` / `package-lock.json`.

## Deployment

Docker Compose production stack (Traefik with Let's Encrypt + Django served by gunicorn and WhiteNoise):
see `docker-compose.production.yml`. Static files are collected at container start.

Create `.envs/.production/.django` (not committed) with:

    DJANGO_SETTINGS_MODULE=config.settings.production
    DJANGO_SECRET_KEY=<long random string>
    DJANGO_ALLOWED_HOSTS=2027.pycon.pt

Then:

    docker compose -f docker-compose.production.yml up --build -d
