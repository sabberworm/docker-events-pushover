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

## Run
First, get a Pushover account (https://https://pushover.net/)
Then, make a note of your User Key
Then, create a new Application within Pushover, and make a note of the Token

### Run manually

```shell
docker run \
    -d --restart=always \
    -v /var/run/docker.sock:/var/run/docker.sock \
    -e PUSHOVER_TOKEN="INSERT-TOKEN-HERE" \
    -e PUSHOVER_KEY="INSERT-KEY-HERE" \
    «name-of-built-image»
```

### Run with docker-compose

```yml 
services:
  docker-events:
    build: «/path/to/this/repository»
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock:ro
    environment:
      - PUSHOVER_TOKEN=INSERT-TOKEN-HERE
      - PUSHOVER_KEY=INSERT-KEY-HERE
    restart: unless-stopped

```

## License
Apache License Version 2.0
