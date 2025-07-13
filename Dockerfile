FROM ubuntu:latest
LABEL authors="JAAME"

ENTRYPOINT ["top", "-b"]

FROM python:3.12.11-slim


WORKDIR /app


COPY requirements.txt requirements.txt


RUN pip3 install -r requirements.txt


COPY . .


CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

