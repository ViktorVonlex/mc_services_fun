# syntax=docker/dockerfile:1
FROM python:alpine
WORKDIR /auth
ENV FLASK_APP=auth_service.py
RUN apk add --no-cache gcc musl-dev linux-headers
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
EXPOSE 5000
COPY . .
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]