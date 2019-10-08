FROM python:3.6.5

RUN apt-get update
RUN apt-get install -y build-essential libatlas-base-dev
RUN apt-get install gcc
RUN apt-get install -y libav-tools

WORKDIR /workshop

COPY requirements.txt /workshop/.

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY complete_pydata_hidden_markov_models_for_chord_recognition.ipynb /workshop/.
COPY presentation_pydata_hidden_markov_models_for_chord_recognition.ipynb /workshop/.
COPY images/ /workshop/images
COPY lab_and_musics/ /workshop/lab_and_musics
COPY sounds/ /workshop/sounds
COPY utils/ /workshop/utils


RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 8888

CMD jupyter notebook --port=8888 --no-browser --ip=0.0.0.0 --allow-root