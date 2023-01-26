FROM python:3.11-alpine
MAINTAINER Rafa Muñoz rafa93m@gmail.com (@rafa93m)

ENV TZ=Europe/Madrid
ENV LOGLEVEL=INFO
ENV PORT=8000

COPY requirements.txt /requirements.txt
RUN apk add --update --no-cache tzdata && \
    pip3 install --no-cache-dir -r /requirements.txt && \
    addgroup -S appuser && adduser -S -s /bin/false -G appuser appuser

USER appuser
COPY src /app
WORKDIR /app

CMD ["python3", "-u", "main.py"]