FROM python:3.8-slim as base

LABEL maintainer="leonid@shestera.com"
LABEL securitytxt="https://openapi.finex.plus/.well-known/security.txt"

ARG HOMEDIR=/app

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
    useradd -r -s /bin/false -d ${HOMEDIR} -g app app

COPY Pipfile Pipfile.lock ./

# hadolint ignore=SC2046,DL3013
RUN pip install pipenv && \
    pipenv install --deploy --system --ignore-pipfile --dev

WORKDIR ${HOMEDIR}
RUN chown -R app:app ${HOMEDIR}
ADD --chown=app:app https://storage.yandexcloud.net/cloud-certs/CA.pem .postgresql/root.crt

COPY --chown=app:app . ${HOMEDIR}

USER app

EXPOSE 8080

CMD ["uvicorn", "main:app", "--host", "0.0.0.0"]
