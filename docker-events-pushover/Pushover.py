import sys
import time
import logging

from http.client import HTTPSConnection
from urllib.parse import urlencode

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

class PushoverException(Exception):
    pass


class Pushover(object):
    def __init__(self, token, user):
        self._token = token
        self._user = user

    def notify(self, message, title="", **kwargs):
        """
        priority (-2 -1 0 1 2)
        sound (bike,bugle,cashregister,classical,cosmic,falling,gamelan,
               incoming,intermission,magic,mechanical,pianobar,siren,spacealarm,
               tugboat,alien,climb,persistent,echo,updown,none)
        """
        logger.info(
            "pushover notify title:{0} message:{1}".format(title, message))
        try:
            data = {
                'token': self._token,
                'user': self._user,
                'title': title,
                'message': message,
            }
            data.update(kwargs)
            payload = []
            for (k, v) in data.items():
                if isinstance(v, str):
                    payload.append((k, v.encode("utf-8")))
                else:
                    payload.append((k, v))
            headers = {"Content-type": "application/x-www-form-urlencoded",}
            conn = HTTPSConnection("api.pushover.net")
            params = urlencode(payload)
            conn.request("POST", "/1/messages.json", params, headers)
            rsp = conn.getresponse()
            if rsp.status != 200:
                raise PushoverException("pushover:{0}".format(rsp.status))
            conn.close()
        except Exception as e:
            raise PushoverException("exception:{0!r}".format(e))

