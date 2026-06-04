FROM node:20-alpine AS frontend-build

WORKDIR /app/vue

COPY ./vue/package*.json ./
RUN npm ci

COPY ./vue ./
RUN npm run build


FROM node:20-alpine AS runtime

ENV HOME=/app
ENV FLASK_PORT=8080

RUN apk add --no-cache \
	python3 \
	py3-pip \
	musl-dev \
	gcc \
	libpq-dev \
	mariadb-connector-c-dev \
	postgresql-dev \
	python3-dev

WORKDIR $HOME/flask

COPY ./flask/src $HOME/flask
COPY --from=frontend-build /app/vue/dist $HOME/flask/dist

RUN pip install --upgrade pip --break-system-packages
RUN pip install -r requirements.txt --break-system-packages

EXPOSE $FLASK_PORT

ENTRYPOINT ["sh", "-c", "cd /app/flask && python main.py"]