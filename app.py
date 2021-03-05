# Copyright 2018 Socialmetrix
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import signal
import sys
import time

import docker
from pushover import Client, init

event_filters = ["create", "update", "destroy", "die",
                 "kill", "pause", "unpause", "start", "stop"]
ignore_names = []
ignore_labels = ["docker-events.ignore"]
ignore_clean_exit = False

BUILD_VERSION = os.getenv('BUILD_VERSION')
APP_NAME = f'Docker Events Pushover (v{BUILD_VERSION})'


def get_config(env_key, optional=False):
    value = os.getenv(env_key)
    if not value and not optional:
        print(f"Environment variable {env_key} is missing. Can't continue")
        sys.exit(1)
    return value


def handle_event(event):
    attributes = event['Actor']['Attributes']

    if attributes['name'] in ignore_names:
        return

    for ignore_label in ignore_labels:
        if ignore_label in attributes:
            return

    if ignore_clean_exit and 'exitCode' in attributes and attributes['exitCode'] == '0':
        return

    when = time.strftime('%Y-%m-%d %H:%M:%S %Z', time.localtime(event['time']))
    send_message(f"Container event {event['status']} ({when}): {attributes}")


def watch_and_notify_events(client):
    global event_filters

    event_filters = {"event": event_filters}

    for event in client.events(filters=event_filters, decode=True):
        handle_event(event)


pushover_client = None

def send_message(message):
    pushover_client.send_message(message,title=f"Docker Event on {host}")
    pass


def exit_handler(signo, _stack_frame):
    send_message(f'{APP_NAME} {signal.strsignal(signo)}. Goodbye!')
    sys.exit(0)


def host_server(client):
    return client.info()['Name']


if __name__ == '__main__':
    po_token = get_config("PUSHOVER_TOKEN")
    po_key = get_config("PUSHOVER_KEY")
    pushover_client = Client(po_key, api_token=po_token)

    events_string = get_config("EVENTS", True)
    if events_string:
        event_filters = events_string.split(',')

    ignore_strings = get_config("IGNORE_NAMES", True)
    if ignore_strings:
        ignore_names = ignore_strings.split(',')

    ignore_label_strings = get_config("IGNORE_LABELS", True)
    if ignore_label_strings:
        ignore_labels = ignore_label_strings.split(',')

    ignore_clean_exit = bool(os.getenv('IGNORE_CLEAN_EXIT'))

    signal.signal(signal.SIGTERM, exit_handler)
    signal.signal(signal.SIGINT, exit_handler)

    client = docker.DockerClient(base_url='unix://var/run/docker.sock')
    host = host_server(client)

    message = f'{APP_NAME} reporting for duty on {host}'
    send_message(message)

    watch_and_notify_events(client)

    pass
