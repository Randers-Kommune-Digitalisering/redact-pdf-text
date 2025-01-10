FROM node:20-alpine

ENV HOME=/app
ENV FLASK_PORT=8080
ENV VITE_PORT=3000

RUN  apk add python3 py3-pip musl-dev gcc libpq-dev mariadb-connector-c-dev postgresql-dev python3-dev

WORKDIR $HOME/vue

COPY ./vue/package*.json ./

RUN cd $HOME/vue && npm install

COPY ./vue $HOME/vue

WORKDIR $HOME/flask

COPY ./flask/src $HOME/flask

RUN pip install --upgrade pip --break-system-packages

RUN pip install -r requirements.txt --break-system-packages

EXPOSE $FLASK_PORT $VITE_PORT

ENTRYPOINT ["sh", "-c", "cd /app/flask && python main.py & cd /app/vue && npm run host"]