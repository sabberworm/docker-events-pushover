# Copyright 2018 Socialmetrix
#
# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import signal
import sys
import time

import docker
from .Pushover import Pushover


def get_config(env_key, default_value=None):
    value = os.getenv(env_key)
    if value:
        return value

    if default_value == None:
        print(f'Environment variable {env_key} is missing. Can’t continue')
        sys.exit(1)
    return default_value


def handle_event(event):
    attributes = event['Actor']['Attributes']

    if attributes['name'] in IGNORE_NAMES:
        return

    for ignore_label in IGNORE_LABELS:
        if ignore_label in attributes:
            return

    if IGNORE_CLEAN_EXIT and 'exitCode' in attributes and attributes['exitCode'] == '0':
        return

    when = time.strftime('%Y-%m-%d %H:%M:%S %Z', time.localtime(event['time']))
    send_message(f'Container event {event["status"]} ({when}): {attributes}')


def send_message(message):
    PUSHOVER_CLIENT.send_message(message, title=f'Docker Event on {HOST}')
    pass


def exit_handler(signo, _stack_frame):
    send_message(f'{APP_NAME} {signal.strsignal(signo)}. Goodbye!')
    sys.exit(0)


def host_server(docker_client):
    return docker_client.info()['Name']


EVENT_FILTERS = get_config(
    'EVENTS',
    'create update destroy die kill pause unpause start stop'
).split()
IGNORE_NAMES = get_config('IGNORE_NAMES', '').split()
IGNORE_LABELS = get_config('IGNORE_LABELS', 'docker-events.ignore').split()
IGNORE_CLEAN_EXIT = bool(os.getenv('IGNORE_CLEAN_EXIT'))

APP_NAME = 'Docker Events Pushover'

PUSHOVER_TOKEN = get_config('PUSHOVER_TOKEN')
PUSHOVER_KEY = get_config('PUSHOVER_KEY')
PUSHOVER_CLIENT = Pushover(PUSHOVER_KEY, api_token=PUSHOVER_TOKEN)

DOCKER_URL = get_config('DOCKER_URL', 'unix://var/run/docker.sock')
DOCKER_CLIENT = docker.DockerClient(base_url=DOCKER_URL)

HOST = host_server(DOCKER_CLIENT)

send_message(f'{APP_NAME} reporting for duty on {HOST}')

signal.signal(signal.SIGTERM, exit_handler)
signal.signal(signal.SIGINT, exit_handler)

for event in DOCKER_CLIENT.events(filters={'event': EVENT_FILTERS}, decode=True):
    handle_event(event)
