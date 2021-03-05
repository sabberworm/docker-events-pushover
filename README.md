# Docker Events Pushover
Receive Pushover notifications when on docker container events

## How it works
This image connects to the host machine socket, through a volume mapping, and listen [Docker Events API](https://docs.docker.com/engine/reference/api/docker_remote_api_v1.24/#/monitor-dockers-events).

When specified events are triggered it sends the affected containers' information to PushBullet.  

If no events are specified in the enironment variables, these are the default ones: "create","update","destroy","die","kill","pause","unpause","start","stop"

If the label docker-events.ignore is specified, then that container will not be checked.

## Environment variables

* `PUSHOVER_TOKEN`: The App token for your Pushover app. _Required_.
* `PUSHOVER_KEY`: The Pushover API key for your account/group. _Required_.
* `EVENTS`: Comma-separated list of events to include. Defaults to `create,update,destroy,die,kill,pause,unpause,start,stop`.
* `IGNORE_NAMES`: Comma-separated list of container names to ignore.
* `IGNORE_LABELS`: Comma-separated list of container labels to ignore. Defaults to `docker-events.ignore`. Label values are not considered.
* `IGNORE_CLEAN_EXIT`: Set to `1` to ignore `die` events that were clean (exit code `0`).

## Build
You must [create a release tag](https://git-scm.com/book/en/v2/Git-Basics-Tagging) in order to build and publish this image.
```shell
./build-all.sh
```

## Run
First, get a Pushover account (https://https://pushover.net/)
Then, make a note of your User Key
Then, create a new Application within Pushover, and make a note of the Token

### Run (default events)
```shell
docker run \
    -d --restart=always \
    -v /var/run/docker.sock:/var/run/docker.sock \
    -e PUSHOVER_TOKEN="INSERT-TOKEN-HERE" \
    -e PUSHOVER_KEY="INSERT-KEY-HERE" \
    derekoharrow/docker-events-pushover:latest
```

### Run (Docker Compose/Stack)
```yml
version: '2'
 
services:
  docker-events:
    container_name: docker-events
    image: derekoharrow/docker-events-pushover:latest
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
    environment:
      - PUSHOVER_TOKEN=INSERT-TOKEN-HERE
      - PUSHOVER_KEY=INSERT-KEY-HERE
      - EVENTS=die,destroy,kill
    restart: unless-stopped

```

## License
Apache License Version 2.0
