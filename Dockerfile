# base image
FROM python:3.7-slim

# set working directory
WORKDIR /app

# copy current directory contents into container
COPY . /app

# install requirements
RUN pip install -r requirements/test.txt

# make port 80 available outside container
EXPOSE 80

# define flask app environment variables
ENV FLASK_APP manage.py
ENV FLASK_RUN_HOST 0.0.0.0

# run server
CMD ["flask", "run"]