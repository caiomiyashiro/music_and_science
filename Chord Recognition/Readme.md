# Workshop - Hidden Markov Models for Chord Recognition - Intuition and Applications  

Link - [https://de.pycon.org/program/pydata-yxndb9-hidden-markov-models-for-chord-recognition-intuition-and-applications-caio-miyashiro/](https://de.pycon.org/program/pydata-yxndb9-hidden-markov-models-for-chord-recognition-intuition-and-applications-caio-miyashiro/)

---
### The idea of the workshop:

In machine learning, traditional mathematical models are still a good choice when dealing with small to medium datasets. However, the theory behind some of them is still hidden under heavy mathematical jargon, making it difficult for a broader application of them in science and in business.

This tutorial's objective is to introduce you to the concept of Hidden Markov Models (HMM), which is a probabilistic framework to work with sequence data, such as speech and language processing and GPS positions. The main idea is to show everyone What is a HMM and provide them with sufficient basis so you can use it in your next projects. The concept will be presented with a specific story and application in music:

> "Given an input music signal, can we identify which chords were played and in which sequence?"  

---
### Execution Requirements

- make sure you have make build system (Linux and Mac should have it by default)
- make sure you have docker

---
### Setup
1. (starting script) in your terminal run: `make setup` after it's done run `make get-url` - you will get a url. Paste it in your browser
2. (manual) in your terminal run:

`docker build . -t workshop && docker run -p 8888:8888 --name caio_workshop workshop`

copy the last link from the output into your browser

### Stop everything
1. (script) run `make clean`
2. (manual) run `docker stop caio_workshop && docker rm caio_workshop && docker rmi workshop`
