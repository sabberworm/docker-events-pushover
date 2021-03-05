# Docker Events Pushover
Receive Pushover notifications on docker container events

## How it works

This container connects to the host machine’s Docker socket through a volume mapping, and listens to events using the [Docker events API](https://docs.docker.com/engine/api/v1.41/#operation/SystemEvents).

When certain events are triggered it sends the affected information to Pushover.  

## Environment variables

* `PUSHOVER_TOKEN`: The app token for your Pushover app. _Required_.
* `PUSHOVER_KEY`: The Pushover API key for your account/group. _Required_.
* `EVENTS`: Whitespace-separated list of events to include. Defaults to `create update destroy die kill pause unpause start stop`.
* `IGNORE_NAMES`: Whitespace-separated list of container names to ignore. Defaults to none.
* `IGNORE_LABELS`: Whitespace-separated list of container labels to ignore. Defaults to `docker-events.ignore`. Label values are not considered.
* `IGNORE_CLEAN_EXIT`: Set to a non-empty value to ignore `die` events that were clean (exit code `0`).
* `BUILD_VERSION`: The version of docker-events-pushover, for version info output in hello and goodbye messages.

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
