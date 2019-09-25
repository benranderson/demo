# base image
FROM python:3.7-alpine

# create and select non-root user
# RUN adduser -D demo
# USER demo

# install dependencies
RUN apk update && \
    apk add --virtual build-deps gcc python-dev musl-dev && \
    apk add postgresql-dev && \
    apk add netcat-openbsd

# set working directory
WORKDIR /app

# add and install requirements
COPY requirements /app/requirements
RUN pip install --no-cache-dir -r requirements/test.txt

# add entrypoint.sh
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# copy current directory contents into container
COPY . .

# define flask app environment variables
ENV FLASK_APP manage.py
ENV FLASK_RUN_HOST 0.0.0.0

# run server
CMD ["/app/entrypoint.sh"]