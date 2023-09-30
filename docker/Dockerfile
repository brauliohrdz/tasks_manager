FROM python:3.11-alpine
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Dependencias de Pillow
RUN apk --no-cache add \
    jpeg-dev \
    zlib-dev

# Postgresql 
RUN apk add --no-cache postgresql-libs postgresql-dev
RUN apk add --no-cache gcc musl-dev

# Configurar directorio de trabajo
RUN mkdir /app  
WORKDIR /app

# Instalar paquetes del proyecto
COPY ./app/requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt


COPY ./app/ /app/

RUN mkdir /scripts
COPY entrypoint.sh /scripts/