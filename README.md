# Docker Events Pushover
Receive Pushover notifications when on docker container events

## How it works
This image connects to the host machine socket, through a volume mapping, and listen [Docker Events API](https://docs.docker.com/engine/api/v1.41/#operation/SystemEvents).

When specified events are triggered it sends the affected information to Pushover.  

## Environment variables

* `PUSHOVER_TOKEN`: The App token for your Pushover app. _Required_.
* `PUSHOVER_KEY`: The Pushover API key for your account/group. _Required_.
* `EVENTS`: Comma-separated list of events to include. Defaults to `create,update,destroy,die,kill,pause,unpause,start,stop`.
* `IGNORE_NAMES`: Comma-separated list of container names to ignore.
* `IGNORE_LABELS`: Comma-separated list of container labels to ignore. Defaults to `docker-events.ignore`. Label values are not considered.
* `IGNORE_CLEAN_EXIT`: Set to `1` to ignore `die` events that were clean (exit code `0`).

## Run

1. Get a Pushover account (https://https://pushover.net/)
2. Make a note of your user key
3. Create a new application within pushover, and make a note of the token

### Run manually

```shell
docker run \
    -d --restart=always \
    -v /var/run/docker.sock:/var/run/docker.sock \
    -e PUSHOVER_TOKEN="«INSERT-TOKEN-HERE»" \
    -e PUSHOVER_KEY="«INSERT-KEY-HERE»" \
    «name-of-built-image»
```

### Run with docker-compose

```yml 
services:
  docker-events:
    build: «/path/to/this/repository»
    restart: unless-stopped
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock:ro
    environment:
      - PUSHOVER_TOKEN=«INSERT-TOKEN-HERE»
      - PUSHOVER_KEY=«INSERT-KEY-HERE»

```

## License
Apache License Version 2.0
