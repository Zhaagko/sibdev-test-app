FROM python:3.10

ENV PYTHONUNBUFFERED 1
ENV SECRET_KEY "SECRET_KEY"
ENV DEBUG "False"
ENV FILE_BASED_CACHE_TIMEOUT_SEC 60

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN make migrate

EXPOSE 8000

CMD ["make", "run"]