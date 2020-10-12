FROM python:3.8-slim as base

LABEL maintainer="leonid@shestera.com"
LABEL securitytxt="https://openapi.finex.plus/.well-known/security.txt"

ENV PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    PIPENV_HIDE_EMOJIS=true \
    PIPENV_COLORBLIND=true \
    PIPENV_NOSPIN=true \
    PIPENV_DOTENV_LOCATION=.env

# hadolint ignore=DL3008, DL3013
RUN set -ex && \
    groupadd -r app && \
    useradd -r -s /bin/false -g app app && \
    apt-get update && \
    rm -rf /var/lib/apt/lists/*

COPY Pipfile Pipfile.lock ./

ARG ENV=PROD

# hadolint ignore=SC2046,DL3013
RUN python -m pip install --upgrade pip && \
    pip install pipenv && \
    pipenv install --deploy --system --ignore-pipfile $([ "$ENV" = "PROD" ] || echo "--dev")

WORKDIR /src

COPY . /src

FROM base

RUN chown -R app:app /src

USER app

EXPOSE 8000

CMD ["uvicorn", "main:app"]
