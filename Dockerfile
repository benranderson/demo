# base image
FROM python:3.7.4-alpine

# install dependencies
RUN apk update && \
    apk add --virtual build-deps gcc python-dev musl-dev && \
    apk add postgresql-dev && \
    apk add netcat-openbsd

# prevent Python from writing pyc files to disc 
ENV PYTHONDONTWRITEBYTECODE 1
# prevent Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED 1

# set working directory
WORKDIR /app

# add and install requirements
COPY requirements /app/requirements
RUN pip install --no-cache-dir -r requirements/test.txt

# add entrypoint.sh
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# copy current directory contents into container
COPY . /app

# define flask app environment variables
ENV FLASK_APP manage.py
ENV FLASK_RUN_HOST 0.0.0.0

# run server
CMD ["/app/entrypoint.sh"]