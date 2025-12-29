FROM python:latest
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY code/requirements.txt /code/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
