import json
import logging
import requests


BASE_URL = 'https://idonethis.com/api'
API_VERSION = 'v0.0'


class PyDoneThis(object):
    def __init__(self, cal_name, api_key):
        self._cal_name = cal_name
        self._api_key = api_key
        self._log = logging.getLogger('IDoneThis')

    def new_done(self, done_text):
        params = {
            'raw_text': done_text,
            'team': self._cal_name,
            'done_date': None
        }
        r = self._do_post('dones', params)
        self._log.debug(r.status_code)
        self._log.debug(r.json())

    def _do_post(self, endpoint, params=None):
        return self._do_request(endpoint, params, method='POST')

    def _do_get(self, endpoint, params=None):
        return self._do_request(endpoint, params, method='GET')

    def _do_request(self, endpoint, params, method):
        params = params or {}
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Token %s' % self._api_key
        }
        url = self._build_url(endpoint)
        if method == 'GET':
            r = requests.get(url, headers=headers)
        else:
            self._log.debug('Posting to %s with %s' % (url, json.dumps(params)))
            r = requests.post(url, data=json.dumps(params), headers=headers)
        return r

    def _build_url(self, endpoint):
        return '/'.join([BASE_URL, API_VERSION, endpoint])
