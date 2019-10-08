FROM python:3.6.5

RUN apt-get update
RUN apt-get install -y build-essential libatlas-base-dev
RUN apt-get install gcc

ENV PIP_CONFIG_FILE=.pip/pip.conf
COPY requirements.txt /tmp/

RUN pip install --upgrade pip
RUN pip install -r /tmp/requirements.txt


COPY . /tmp/

EXPOSE 8888

CMD jupyter notebook --port=8888 --no-browser --ip=0.0.0.0 --allow-root
