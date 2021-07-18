# pull official base image
FROM python:3.9-slim

# set work directory
WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install  dependencies
RUN apt-get update -y \
    && apt-get install -y gcc python3-dev

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# copy entrypoint.sh
#COPY ./entrypoint.sh .

# copy project
COPY . .


# run entrypoint.sh
#ENTRYPOINT ["/app/entrypoint.sh"] #for postgresql
