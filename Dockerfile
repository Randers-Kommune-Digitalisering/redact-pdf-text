FROM node:23-alpine AS vue-build

WORKDIR /app

## Build and copy the vue app
COPY vue .
RUN npm install && npm run build

FROM python:3.12-slim

# Set dir and user
ENV GROUP_NAME=app
ENV HOME=/app
ENV GROUP_ID=11000
ENV USER_ID=11001
ENV PORT=8080

# Add user
RUN addgroup --gid $GROUP_ID $GROUP_NAME && \
    adduser $USER_ID -u $USER_ID -D -G $GROUP_NAME -h $HOME

# Install OCR and build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc libpq-dev python3-dev \
    ghostscript qpdf tesseract-ocr tesseract-ocr-dan \
    && rm -rf /var/lib/apt/lists/*

# Set working dir
WORKDIR $HOME

# Copy files and 
COPY --from=vue-build /app/dist ./dist
COPY flask/src .

# Install python packages
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Open port
EXPOSE $PORT

# Set user
USER $USER_ID

ENTRYPOINT ["python"]
CMD ["main.py"]