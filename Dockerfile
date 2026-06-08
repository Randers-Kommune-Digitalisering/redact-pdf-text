FROM node:20-alpine AS frontend-build

WORKDIR /app/vue

COPY ./vue/package*.json ./
RUN npm ci

COPY ./vue ./
RUN npm run build


FROM node:20-alpine AS runtime

ENV HOME=/app
ENV FLASK_PORT=8080
ENV VITE_PORT=3000

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
COPY --from=frontend-build /app/vue/dist $HOME/vue/dist
COPY --from=frontend-build /app/vue/package*.json $HOME/vue/
COPY --from=frontend-build /app/vue/node_modules $HOME/vue/node_modules
COPY --from=frontend-build /app/vue/vite.config.js $HOME/vue/vite.config.js
COPY --from=frontend-build /app/vue/index.html $HOME/vue/index.html
COPY --from=frontend-build /app/vue/public $HOME/vue/public

RUN pip install --upgrade pip --break-system-packages
RUN pip install -r requirements.txt --break-system-packages

EXPOSE $FLASK_PORT $VITE_PORT

ENTRYPOINT ["sh", "-c", "cd /app/flask && python main.py & cd /app/vue && npm run preview -- --host 0.0.0.0 --port $VITE_PORT"]