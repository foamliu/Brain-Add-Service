FROM ubuntu:16.04
MAINTAINER Yang Liu <foamliu@yeah.net>
RUN apt-get update -y
RUN apt-get -y install python3-pip
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app/
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . /usr/src/app

# Expose the Flask port
EXPOSE 5001

CMD [ "python3", "./app.py" ]
