FROM tiangolo/uvicorn-gunicorn:python3.8-alpine3.10

WORKDIR /musicoop

# Install GCC
RUN apk add --no-cache --virtual .build-deps postgresql-dev \
    gcc libc-dev libffi-dev libpq build-base

# Copy using poetry.lock* in case it doesn't exist yet
COPY ./requirements.txt /musicoop/

RUN pip install --no-cache-dir -r /musicoop/requirements.txt

RUN apk del .build-deps postgresql-dev gcc libc-dev libffi-dev libpq \
    build-base

RUN apk add --no-cache libpq

COPY . /musicoop

RUN cd musicoop

CMD ["uvicorn", "musicoop.app:app","--host", "0.0.0.0", "--port", "8000"]