FROM ubuntu:16.04
MAINTAINER Yang Liu <foamliu@yeah.net>
RUN apt-get update && apt-get install -y \
    python3-pip \
    libopencv-dev \
  && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app/
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . /usr/src/app

# Expose the Flask port
EXPOSE 5001

CMD [ "python3", "./app.py" ]
