FROM python:3.10.1-slim-bullseye as builder

COPY poetry.lock pyproject.toml ./

RUN python -m pip install poetry==1.8.2 && \
    poetry export -o requirements.prod.txt --without-hashes 
    # poetry export --with=dev -o requirements.dev.txt --without-hashes

FROM python:3.10.1-slim-bullseye as dev

WORKDIR /src

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
COPY --from=builder requirements.prod.txt /src

RUN apt update -y && \
    apt install -y python3-dev \
    gcc \
    musl-dev && \
    pip install --upgrade pip && pip install --no-cache-dir -r requirements.prod.txt

EXPOSE 8001
