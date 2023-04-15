# kubernetes_homework
DevOps course. Kubernetes homework. Nexign

## Задачи

Создать приложение, состоящее из клиента и сервера, запускаемого через Docker compose.

1. Создать web-приложение "server", которое выводит строку "Hello world!" при обращении по http-адресу
   "http://127.0.0.1:8000".
2. Собрать его в виде Docker image.
3. Запустить Docker container и проверить, что web-приложение работает.
4. Выложить image на Docker Hub.
5. Создать приложение "client", которое обращается к "server" по указанному выше адресу и выводит ответ.
6. Запустить Docker containers "server" и "client" через Docker compose.

## Шаг 1

Docker-desktop был установлен по ссылке - https://docs.docker.com/get-docker/ . Аккаунт docker-hub - `beonewithyuri`.

```shell
$ sudo docker info

Client:
 Context:    default
 Debug Mode: false
 Plugins:
  buildx: Docker Buildx (Docker Inc.)
    Version:  v0.10.4
    Path:     /usr/lib/docker/cli-plugins/docker-buildx
  compose: Docker Compose (Docker Inc.)
    Version:  v2.17.2
    Path:     /usr/lib/docker/cli-plugins/docker-compose
  dev: Docker Dev Environments (Docker Inc.)
    Version:  v0.1.0
    Path:     /usr/lib/docker/cli-plugins/docker-dev
  extension: Manages Docker extensions (Docker Inc.)
    Version:  v0.2.19
    Path:     /usr/lib/docker/cli-plugins/docker-extension
  init: Creates Docker-related starter files for your project (Docker Inc.)
    Version:  v0.1.0-beta.2
    Path:     /usr/lib/docker/cli-plugins/docker-init
  sbom: View the packaged-based Software Bill Of Materials (SBOM) for an image (Anchore Inc.)
    Version:  0.6.0
    Path:     /usr/lib/docker/cli-plugins/docker-sbom
  scan: Docker Scan (Docker Inc.)
    Version:  v0.25.0
    Path:     /usr/lib/docker/cli-plugins/docker-scan
  scout: Command line tool for Docker Scout (Docker Inc.)
    Version:  v0.9.0
    Path:     /usr/lib/docker/cli-plugins/docker-scout

Server:
 Containers: 3
  Running: 0
  Paused: 0
  Stopped: 3
 Images: 4
 Server Version: 23.0.3
 Storage Driver: overlay2
  Backing Filesystem: extfs
  Supports d_type: true
  Using metacopy: false
  Native Overlay Diff: true
  userxattr: false
 Logging Driver: json-file
 Cgroup Driver: systemd
 Cgroup Version: 2
 Plugins:
  Volume: local
  Network: bridge host ipvlan macvlan null overlay
  Log: awslogs fluentd gcplogs gelf journald json-file local logentries splunk syslog
 Swarm: inactive
 Runtimes: runc io.containerd.runc.v2
 Default Runtime: runc
 Init Binary: docker-init
 containerd version: 2806fc1057397dbaeefbea0e4e17bddfbd388f38
 runc version: v1.1.5-0-gf19387a
 init version: de40ad0
 Security Options:
  seccomp
   Profile: builtin
  cgroupns
 Kernel Version: 5.15.90.1-microsoft-standard-WSL2
 Operating System: Ubuntu 22.04.2 LTS
 OSType: linux
 Architecture: x86_64
 CPUs: 12
 Total Memory: 15.59GiB
 Name: DESKTOP-RD06M0K
 ID: 3fb76714-2d74-4b26-92b2-3d6353585dc4
 Docker Root Dir: /var/lib/docker
 Debug Mode: false
 Username: beonewithyuri
 Registry: https://index.docker.io/v1/
 Experimental: false
 Insecure Registries:
  127.0.0.0/8
 Live Restore Enabled: false
```

Структура файлов проекта:
```shell
$ tree -I 'venv'
.
├── LICENSE
├── README.md
├── client
│   ├── Dockerfile
│   └── client.py
├── docker-compose.yml
├── requirements.txt
└── server
    ├── Dockerfile
    └── server.py
```

В качестве фреймворка для сервера использован [Python Flask](https://flask.palletsprojects.com/). Код `server/server.py`:

```python
from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello_world():
    """Hello world function

    Returns:
        str : 'Hello World!'
    """
    return 'Hello World!'

```

В файле `server/Dockerfile` описана сборка и описан запуск сервера:

```Dockerfile
# Based image
FROM python:3.10-alpine

# Variables required for enviroment creation
ARG USER=app
ARG UID=1001
ARG GID=1001

# Framework installation
RUN pip install --no-cache-dir Flask==2.2.*

# Creating OS user and home directory
RUN addgroup -g ${GID} -S ${USER} \
   && adduser -u ${UID} -S ${USER} -G ${USER} \
   && mkdir -p /app \
   && chown -R ${USER}:${USER} /app
USER ${USER}

# Entering home dir /app
WORKDIR /app

# Enviroment variables required for launching web-application
ENV FLASK_APP=server.py \
   FLASK_RUN_HOST="0.0.0.0" \
   FLASK_RUN_PORT="8000" \
   PYTHONUNBUFFERED=1

# Copying application code to home directory
COPY --chown=$USER:$USER server.py /app

# Publishing the port that the application is listening on
EXPOSE 8000

# Application launch command
CMD ["flask", "run"]
```

## Шаг 2

Используя приведённую команду ниже создаём образ - Docker image:

```shell
sudo docker build -t beonewithyuri/server:1.0.0 --network host -t beonewithyuri/server:latest server
```

Список image:

```shell
$ sudo docker image ls
REPOSITORY             TAG       IMAGE ID       CREATED          SIZE
beonewithyuri/client   1.0.0     aafb423ebb1c   47 minutes ago   49.7MB
beonewithyuri/server   1.0.0     f5cb4a0262f0   2 hours ago      60.6MB
beonewithyuri/server   latest    f5cb4a0262f0   2 hours ago      60.6MB
<none>                 <none>    be73e9f8b66b   2 hours ago      60.6MB
hello-world            latest    feb5d9fea6a5   18 months ago    13.3kB
```

## Шаг 3

Из созданного image был запущен Docker container, вместе с ним web-приложение.

```shell
$ sudo docker run -ti --rm -p 8000:8000 --name server --network host beonewithyuri/server:1.0.0
WARNING: Published ports are discarded when using host network mode
 * Serving Flask app 'server.py'
 * Debug mode: off
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:8000
 * Running on http://172.21.30.20:8000
Press CTRL+C to quit
```

Замечание игнорируем. Для просмотра запущенных контейнеров:

```shell
$ sudo docker container list
CONTAINER ID   IMAGE                        COMMAND       CREATED         STATUS         PORTS     NAMES
37d755539280   beonewithyuri/server:1.0.0   "flask run"   2 minutes ago   Up 2 minutes             server
```

Откроем в браузере адрес `http://127.0.0.1:8000`. Будет показан текст `Hello world!`. 
Также проверить его работу можно через команду `curl`.

```shell
$ curl http://127.0.0.1:8000
Hello World!
```

Наше web-приложение работает.
Остановить запущенный container можно при помощи `Ctrl+c` в консоле контейнера.

## Шаг 4

Получим Access Token в `https://hub.docker.com/settings/security`

Авторизуемся в Docker registry. В качестве пароля введем Access Token.

```shell
$ sudo docker login -u beonewithyuri

Password:
Login Succeeded
```

Отправим Docker image в Registry Docker Hub.

```shell
$ sudo docker push beonewithyuri/server:1.0.0
```

Откроем web-интерфейс Docker Hub по адресу `https://hub.docker.com/` и найдем загруженный image

![image](https://user-images.githubusercontent.com/59288516/232248179-095471b8-ac50-4312-b82c-970540bd8e88.png)

## Шаг 5.

Создадим файл `client/client.py` с кодом web-приложения "client".

```python
import urllib.request


client = urllib.request.urlopen("http://127.0.0.1:8000")


# Decoding response
encodedContent = client.read()
decodedContent = encodedContent.decode("utf8")

print(decodedContent)
client.close()

```

Создадим Dockerfile для сборки "client".

## Шаг 6.

Создадим файл `docker-compose.yml`, где опишем конфигурацию сборки и запуска приложений.

```yaml
# Версия API Docker compose
version: "3"

# Раздел, в котором описываются приложения (сервисы).
services:

  # Раздел для описания приложения 'server'.
  server:

    # Имя image tag
    image: beonewithyuri/server:1.0.0
 
    # Параметры сборки Docker image.
    build: 
      # Путь к Dockerfile,
      context: server/
      # Использовать host-сеть при сборке,
      network: host

    # Перенаправление портов из Docker container на host-машину.
    ports:
      - 8000:8000

    # Имя user, используемого в image,
    user: "1001"

    # Используемый тип сети при запуске container.
    network_mode: host

    # Проверка готовности приложения к работе. Параметр "--spider" означает: не загружать url, 
    # а только проверить его наличие.
    healthcheck:
        test: wget --no-verbose --tries=1 --spider http://localhost:8000 || exit 1
        interval: 5s
        timeout: 5s
        retries: 5

  # Раздел для описания приложения 'client'.
  client:

    image: beonewithyuri/client:1.0.0

    build: 
      context: client/

    user: "1001"

    network_mode: host

    # Команда запуска приложения внутри container,
    command: "python ./client.py"

    # Зависимость от других сервисов,
    depends_on:
      # Сервис 'client' зависит от сервиса 'server'. 
      # Прежде чем запустить 'client' необходимо дождаться запуска 'server'.
      # Условием запуска сервиса 'server' является его healthcheck.
      server:
        condition: service_healthy
```

Соберем Docker images при помощи docker compose. Docker image "server" и "client" будет пересобран с использованием cache.

```shell
$ sudo docker compose build
[+] Building 1.2s (11/11) FINISHED                                                                                                                                                                                                                                                                         
 => [internal] load build definition from Dockerfile                                                                                                                                                                                                                                                  0.0s
 => => transferring dockerfile: 842B                                                                                                                                                                                                                                                                  0.0s
 => [internal] load .dockerignore                                                                                                                                                                                                                                                                     0.0s
 => => transferring context: 2B                                                                                                                                                                                                                                                                       0.0s
 => [internal] load metadata for docker.io/library/python:3.10-alpine                                                                                                                                                                                                                                 1.1s
 => [auth] library/python:pull token for registry-1.docker.io                                                                                                                                                                                                                                         0.0s
 => [internal] load build context                                                                                                                                                                                                                                                                     0.0s
 => => transferring context: 31B                                                                                                                                                                                                                                                                      0.0s
 => [1/5] FROM docker.io/library/python:3.10-alpine@sha256:1eba91607a236342119c5e2caaab14dc906c8370fe647477279e76d01c6dd733                                                                                                                                                                           0.0s
 => CACHED [2/5] RUN pip install --no-cache-dir Flask==2.2.*                                                                                                                                                                                                                                          0.0s
 => CACHED [3/5] RUN addgroup -g 1001 -S app    && adduser -u 1001 -S app -G app    && mkdir -p /app    && chown -R app:app /app                                                                                                                                                                      0.0s
 => CACHED [4/5] WORKDIR /app                                                                                                                                                                                                                                                                         0.0s
 => CACHED [5/5] COPY --chown=app:app server.py /app                                                                                                                                                                                                                                                  0.0s
 => exporting to image                                                                                                                                                                                                                                                                                0.0s
 => => exporting layers                                                                                                                                                                                                                                                                               0.0s
 => => writing image sha256:be73e9f8b66b79306b5c72a7661fba0d6f6f2c25afc254fc3b15e2713fcf2661                                                                                                                                                                                                          0.0s
 => => naming to docker.io/beonewithyuri/server:1.0.0                                                                                                                                                                                                                                                 0.0s
[+] Building 0.3s (9/9) FINISHED                                                                                                                                                                                                                                                                           
 => [internal] load .dockerignore                                                                                                                                                                                                                                                                     0.0s
 => => transferring context: 2B                                                                                                                                                                                                                                                                       0.0s
 => [internal] load build definition from Dockerfile                                                                                                                                                                                                                                                  0.0s
 => => transferring dockerfile: 371B                                                                                                                                                                                                                                                                  0.0s
 => [internal] load metadata for docker.io/library/python:3.10-alpine                                                                                                                                                                                                                                 0.2s
 => [internal] load build context                                                                                                                                                                                                                                                                     0.0s
 => => transferring context: 31B                                                                                                                                                                                                                                                                      0.0s
 => [1/4] FROM docker.io/library/python:3.10-alpine@sha256:1eba91607a236342119c5e2caaab14dc906c8370fe647477279e76d01c6dd733                                                                                                                                                                           0.0s
 => CACHED [2/4] RUN addgroup -g 1001 -S app     && adduser -u 1001 -S app -G app     && mkdir -p /app     && chown -R app:app /app                                                                                                                                                                   0.0s
 => CACHED [3/4] WORKDIR /app                                                                                                                                                                                                                                                                         0.0s
 => CACHED [4/4] COPY --chown=app:app client.py /app                                                                                                                                                                                                                                                  0.0s
 => exporting to image                                                                                                                                                                                                                                                                                0.0s
 => => exporting layers                                                                                                                                                                                                                                                                               0.0s
 => => writing image sha256:aafb423ebb1ca7c49d12650066a7f76d584846f6d7df9dbf2121531525636cea                                                                                                                                                                                                          0.0s
 => => naming to docker.io/beonewithyuri/client:1.0.0 
 ```
 
 Запустим оба приложения при помощи docker compose. Сначала запустится Docker container 'server',
затем выполнится проверка его работоспособности (healthcheck), затем запустится Docker container 'client'.

```shell
[+] Running 2/0
 ✔ Container kubernetes_homework-server-1  Created                                                                                                                                                                                                                                                    0.0s 
 ✔ Container kubernetes_homework-client-1  Created                                                                                                                                                                                                                                                    0.0s 
Attaching to kubernetes_homework-client-1, kubernetes_homework-server-1
kubernetes_homework-server-1  |  * Serving Flask app 'server.py'
kubernetes_homework-server-1  |  * Debug mode: off
kubernetes_homework-server-1  | WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
kubernetes_homework-server-1  |  * Running on all addresses (0.0.0.0)
kubernetes_homework-server-1  |  * Running on http://127.0.0.1:8000
kubernetes_homework-server-1  |  * Running on http://172.21.30.20:8000
kubernetes_homework-server-1  | Press CTRL+C to quit
kubernetes_homework-server-1  | 127.0.0.1 - - [15/Apr/2023 18:59:41] "GET / HTTP/1.1" 200 -
kubernetes_homework-server-1  | 127.0.0.1 - - [15/Apr/2023 18:59:42] "GET / HTTP/1.1" 200 -
kubernetes_homework-client-1  | Hello World!
kubernetes_homework-client-1 exited with code 0
kubernetes_homework-server-1  | 127.0.0.1 - - [15/Apr/2023 18:59:46] "GET / HTTP/1.1" 200 -
kubernetes_homework-server-1  | 127.0.0.1 - - [15/Apr/2023 18:59:51] "GET / HTTP/1.1" 200 -
```

Посмотрим логи наших Docker containers. Логи можно увидеть даже после остановки containers.

```shell
$ sudo docker logs kubernetes_homework-client-1
Hello World!
```

```shell
$ sudo docker logs kubernetes_homework-server-1
 * Serving Flask app 'server.py'
 * Debug mode: off
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:8000
 * Running on http://172.21.30.20:8000
Press CTRL+C to quit
127.0.0.1 - - [15/Apr/2023 17:43:26] "GET / HTTP/1.1" 200 -
127.0.0.1 - - [15/Apr/2023 17:43:27] "GET / HTTP/1.1" 200 -
127.0.0.1 - - [15/Apr/2023 17:43:31] "GET / HTTP/1.1" 200 -
127.0.0.1 - - [15/Apr/2023 17:43:36] "GET / HTTP/1.1" 200 -
```
