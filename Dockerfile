FROM python:3.11-alpine

RUN apk update --no-check-certificate \
    && apk add --no-cache --no-check-certificate --virtual \
    .build-deps libffi-dev gcc libc-dev make curl \
    && apk upgrade --no-check-certificate

WORKDIR /srv

COPY certs.crt /usr/local/share/ca-certificates/
RUN update-ca-certificates
ENV REQUESTS_CA_BUNDLE="/usr/local/share/ca-certificates/certs.crt"


RUN python3 -m pip install -q --upgrade \
    --index-url=https://pypi.python.org/simple/ \
    --trusted-host=pypi.org \
    --trusted-host=pypi.python.org \
    --trusted-host=files.pythonhosted.org \
    pip \
    && pip install \
    --index-url=https://pypi.python.org/simple/ \
    --trusted-host=pypi.org \
    --trusted-host=pypi.python.org \
    --trusted-host=files.pythonhosted.org \
    -v poetry

ENV PATH="/root/.local/bin:$PATH"
ENV PYTHONPATH=/srv

COPY poetry.lock .
COPY pyproject.toml .

RUN poetry config virtualenvs.create false \
  && poetry install

COPY . .

CMD ["python", "-m", "src.main"]
