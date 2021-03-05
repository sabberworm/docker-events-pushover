# Docker Events Pushover
Receive Pushover notifications on docker container events.

## How it works

This script connects to a Docker server, and listens to events using the [Docker events API](https://docs.docker.com/engine/api/v1.41/#operation/SystemEvents). When certain container events are triggered it sends the affected information to Pushover.

## Environment variables

* `PUSHOVER_TOKEN`: The app token for your Pushover app. _Required_.
* `PUSHOVER_KEY`: The Pushover API key for your account/group. _Required_.
* `EVENTS`: Whitespace-separated list of events to include. Defaults to `create update destroy die kill pause unpause start stop`.
* `IGNORE_NAMES`: Whitespace-separated list of container names to ignore. Defaults to none.
* `IGNORE_LABELS`: Whitespace-separated list of container labels to ignore. Defaults to `docker-events.ignore`. Label values are not considered.
* `IGNORE_CLEAN_EXIT`: Set to a non-empty value to ignore `die` events that were clean (exit code `0`).
* `DOCKER_URL`: The connection string for the docker client. Defaults to `unix://var/run/docker.sock` (socket connection).

## Run

1. Get a [Pushover](https://pushover.net/) account
2. Make a note of your user key (`export PUSHOVER_KEY="«INSERT-KEY-HERE»"`)
3. Create a new application within pushover, and make a note of the token (`export PUSHOVER_TOKEN="«INSERT-TOKEN-HERE»"`)
4. Install requirements using `pip install -r requirements.txt`
5. Run using `python -m docker-events-pushover`

### Run with docker

When running with the docker instance whose events you try to capture, mount the docker socket using a read-only volume mapping.

```shell
docker build . -t «name-of-built-image»

docker run \
    -d --restart=always \
    -v /var/run/docker.sock:/var/run/docker.sock:ro \
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
      # Any other env vars you want to configure
```

## License
Apache License Version 2.0
