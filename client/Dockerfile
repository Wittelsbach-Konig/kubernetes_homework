FROM python:3.10-alpine

ARG USER=app
ARG UID=1001
ARG GID=1001

RUN addgroup -g ${GID} -S ${USER} \
    && adduser -u ${UID} -S ${USER} -G ${USER} \
    && mkdir -p /app \
    && chown -R ${USER}:${USER} /app
USER ${USER}

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY --chown=$USER:$USER client.py /app

CMD [ "python", "client.py" ]