FROM debian:latest

MAINTAINER Arturo Escudero <darkturo@gmail.com>

LABEL Description="Chat Service" Version="0.0.1"

RUN apt-get update && apt-get -y install python-pip

RUN apt-get install -y python-nose

RUN pip install jsonschema 

RUN pip install flask flask-bootstrap flask-wtf flask-nav Flask-SQLAlchemy
