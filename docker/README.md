Docker の使い方メモ
=================


# Docker ビルド手順

## Fire it up
Start the container by issuing one of the following commands:
```bash
docker-compose up             # run in foreground
docker-compose up -d          # run in background
```

## Other commands
Build images:
```bash
docker-compose build
docker-compose build --no-cache       # build without cache
```

See processes:
```bash
docker-compose ps                 # docker-compose processes
docker ps -a                      # docker processes (sometimes needed)
docker stats [container name]     # see live docker container metrics
```

Run commands in container:
```bash
CONTAINER_ID=$(docker ps -a | awk '/geodjango-postgis-gae/ { print $1 }')
docker exec -it $CONTAINER_ID bash
docker exec -it $CONTAINER_ID env # env vars
```

Stop container:
```bash
docker-compose stop
```

Remove all container:
```bash
docker rm `docker ps -a -q`
```

Remove all data volume
```bash
docker volume rm `docker volume ls -q`
```

Show iamge:
```bash
docker images
```

Remove unused images:
```bash
docker rmi $(docker images | awk '/^<none>/ { print $3 }')    # REPOSITORY が <none> のimageを削除
```
