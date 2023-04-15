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

Docker-desktop был установлен заранее. Аккаунт docker-hub - 'beonewithyuri'

'''shell
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
'''
