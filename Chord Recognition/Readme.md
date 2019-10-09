# Workshop - Hidden Markov Models for Chord Recognition - Intuition and Applications  

Link - [https://de.pycon.org/program/pydata-yxndb9-hidden-markov-models-for-chord-recognition-intuition-and-applications-caio-miyashiro/](https://de.pycon.org/program/pydata-yxndb9-hidden-markov-models-for-chord-recognition-intuition-and-applications-caio-miyashiro/)

Backup Files and Pdf versions: https://drive.google.com/drive/folders/1YmfEPtX_QLlpo0sR0kQwFV4-Lz6Sd01W?usp=sharing. Note that this link will be deleted in **January 2020**

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

### Setup without make - only docker commands
1. In the root directory run: `docker build . -t workshop`. This process might take around ~5 minutes
2. Run: `docker run -p 8888:8888 -d --name caio_workshop workshop`
3. You will see an output similar to this:
> [I 06:21:58.349 NotebookApp] Writing notebook server cookie secret to /root/.local/share/jupyter/runtime/notebook_cookie_secret
[I 06:21:59.701 NotebookApp] Serving notebooks from local directory: /workshop
[I 06:21:59.701 NotebookApp] The Jupyter Notebook is running at:
[I 06:21:59.701 NotebookApp] http://2d7cc2cb7462:8888/?token=8a9ce1b6213dc455003b2ccdc79028a00b660b7666f9841b
[I 06:21:59.701 NotebookApp]  or http://127.0.0.1:8888/?token=8a9ce1b6213dc455003b2ccdc79028a00b660b7666f9841b  

Copy the **whole** last line URL - the one that starts with `http://127.0.0.1:8888` and paste it into your browser.
