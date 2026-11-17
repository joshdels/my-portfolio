# syntax=docker/dockerfile:1

FROM python:3.14-slim AS builder

WORKDIR /app

ARG UV_VERSION=0.13.9

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PROJECT_ENVIRONMENT=/opt/venv

RUN pip install --no-cache-dir "uv==${UV_VERSION}"

COPY pyproject.toml uv.lock ./

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev --no-install-project

COPY . .

RUN DJANGO_SETTINGS_MODULE=config.settings.build \
    /opt/venv/bin/python manage.py collectstatic --noinput --clear


FROM python:3.14-slim AS runtime

ARG VCS_REF=local

LABEL org.opencontainers.image.revision="${VCS_REF}"

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/opt/venv/bin:$PATH"

WORKDIR /app

COPY --from=builder /opt/venv /opt/venv
COPY --from=builder /app /app

RUN groupadd --system portfolio \
    && useradd --system --gid portfolio --home-dir /app --shell /usr/sbin/nologin portfolio \
    && chown -R portfolio:portfolio /app

USER portfolio

EXPOSE 8000

CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "2", "--threads", "4", "--worker-class", "gthread", "--timeout", "45", "--graceful-timeout", "30", "--keep-alive", "5", "--max-requests", "1000", "--max-requests-jitter", "100", "--access-logfile", "-", "--error-logfile", "-", "--log-level", "info"]
