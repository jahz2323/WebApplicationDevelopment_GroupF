FROM python:3.13

RUN mkdir /app /app/storage
WORKDIR /app

COPY requirements.txt  /app/
RUN pip install --no-cache-dir -r requirements.txt
COPY . /app/

CMD ["sh", "/app/docker_entrypoint.sh"]
