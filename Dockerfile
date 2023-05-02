FROM python:3

ENV POETRY_HOME=/opt/poetry \
    POETRY_VIRTUALENVS_CREATE=false \
    \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    \
    PYSETUP_PATH="/opt/pysetup"

ENV PATH="$POETRY_HOME/bin:$PATH"

RUN apt-get update && \
    apt-get install --no-install-recommends -y curl && \
    apt-get clean && \
    curl -sSL https://install.python-poetry.org/ | python - && \ 
    mkdir /app && \
    echo /app/src > $(python -c 'import sys; print(sys.path)' | grep -o "[^']*/site-packages")/app.pth

WORKDIR /app
COPY ./pyproject.toml /app/pyproject.toml
RUN poetry self update && \
    poetry install