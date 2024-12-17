# Vue-Python-Tempplate
Template for vue and python projects.
NB: backend endpoints er åbne udtil (samme som frontend'en). Hvis der skal bruges en "rigtig" backend - deploy [vue](https://github.com/Randers-Kommune-Digitalisering/vue-js-template) og [flask](https://github.com/Randers-Kommune-Digitalisering/python-app-template) i hver sin pod.

## Kørsel af frontend + backend i docker
* Kør ```docker-compose up``` i top dir
* Backend på port 8080, frontend på port 3000

## Kørsel af Frontenden(Vue)
* CD hen til vue folder: ``` cd vue ```
* Installerer afhængigheder: ``` npm install ```
* Compile, hot reload og start frontenden: ``` npm run dev ```

## Kørsel af Bakcenden(Python)
* Start applikationen: ``` python flask/src/main.py ```

## Udviklings commands:
* Bygge docker image: ```docker build -t vue-python-template .```
* Kør container ud fra det image man byggede: ```docker run -p 8080:8080 vue-python-template```
* Lint: ```flake8 python/src tests --count --select=E9,F63,F7,F82 --show-source --statistics```
* Unit tests: ``` pytest ```


