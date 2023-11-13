# syntax=docker/dockerfile:1
FROM python:alpine
WORKDIR /server
ENV FLASK_APP=better_server.py
RUN apk add --no-cache gcc musl-dev linux-headers
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
EXPOSE 8082
COPY . .
CMD ["flask", "run", "--host=0.0.0.0", "--port=8082"]
