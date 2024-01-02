"""Client for HTTP Requests

This module provides a Client object to interface with an API.

"""

import datetime
import json
import logging
import os
import requests
import time

from apps.apihandler.errors import UnprocessableEntity
from requests import HTTPError
from requests import Session
from requests.adapters import HTTPAdapter
#from requests.compat import urljoin
from requests.packages.urllib3.util.retry import Retry # type: ignore

bearerToken = 'Bearer Token December 2023'
basedir     = os.path.abspath(os.path.dirname(__file__))
logger      = logging.getLogger(__name__)

'''
/*
 *Urls for asking questions of the documents, retrieving the
 * answers, and giving feedback as to the goodness of references.
 */'''
class Client(Session):
    """GeneNetworkQA Client

    Constructs a :obj:`requests.Session` for GeneNetworkQA API requests with
    authorization, base URL, request timeouts, and request retries.

    Args:
        account (str): base address subdomain
        api_key (str): API key
        version (str, optional): API version, defaults to "v3"
        timeout (int, optional): :obj:`` timeout value, defaults to 5
        total (int, optioanl): :obj:`Retry` total value, defaults to 5
        backoff_factor (int, optional): :obj:`Retry` backoff_factor value, defaults to 30

    Usage::
        from genenetworkqa import Client
        gnqa = Client(account="account-name", api_key="XXXXXXXXXXXXXXXXXXX...")
    """

    def __init__(self, account, api_key, v="v3", timeout=5, total=5, backoff_factor=30) -> None:
        """
        """
        super().__init__()
        self.host = f"https://genenetwork.fahamuai.com/api/tasks"
        self.headers.update(self.getAuth(self.openAPIConfig()))
        self.baseUrl      = 'https://genenetwork.fahamuai.com/api/tasks'
        self.answerUrl    = self.baseUrl + '/answers'
        self.feedbackUrl  = self.baseUrl + '/feedback'
        adapter = TimeoutHTTPAdapter(
            timeout=timeout,
            max_retries=Retry(
                total=total,
                status_forcelist=[429, 500, 502, 503, 504],
                backoff_factor=backoff_factor,
            ),
        )
        self.mount("https://", adapter)
        self.mount("http://", adapter)


    def openAPIConfig(self):
        f = open(os.path.join(basedir, "api.config.json") , "rb" )
        result = json.load(f)
        f.close()
        return result

    def getAuth(self, api_config):
        return {"Authorization": "Bearer " + api_config[bearerToken]}

    def ask(self, exUrl, *args, **kwargs):
        askUrl = self.baseUrl + exUrl
        res    = self.custom_request('POST', askUrl, *args, **kwargs)
        if (res.status_code != 200):
            return self.negativeStatusMsg(res), 0
        task_id = self.getTaskIDFromResult(res)
        return res, task_id

    def getAnswer(self, taskid, *args, **kwargs):
        query = self.answerUrl + self.extendTaskID(taskid)
        res   = self.custom_request('GET', query, *args, **kwargs)
        if (res.status_code != 200):
            return self.negativeStatusMsg(res), 0
        return res, 1

    def negativeStatusMsg(self, res):
        return 'Problems\n\tStatus code => {0}\n\tReason=> {res.reason}'.format(res.status_code, res.reason)

    def extendTaskID(self, task_id):
        return '?task_id=' + str(task_id['task_id'])

    def getTaskIDFromResult(self, res):
        return json.loads(res.text)

    def custom_request(self, method, url, *args, **kwargs):
        max_retries = 5
        retry_delay = 4

        print ('[{0}] Request begin'.format(datetime.datetime.now()))
        response = super().request(method, url, *args, **kwargs)
        print ('[{0}] Response arrival'.format(datetime.datetime.now()))

        i = 0
        for i in range(max_retries):
            try:
                print ('Raising status for response {0} -- {1}'.format(i+1, datetime.datetime.now()))
                response.raise_for_status()
            except requests.exceptions.RequestException as exc:
                code = exc.response.status_code
                if code == 422:
                    raise UnprocessableEntity(exc.request, exc.response)
                    #from exc
                elif i == max_retries - 1:
                    raise
            if response.ok:
                print('Status code for response is {0}'.format(response.status_code))
                # Give time to get all the data
                print ('[{0}] delay begin'.format(datetime.datetime.now()))
                time.sleep(retry_delay*3)
                print ('[{0}] delay   end'.format(datetime.datetime.now()))
                return response
            else:
                print ('[{1}] Retry {0}'.format(i+1, datetime.datetime.now()))
                time.sleep(retry_delay)
        return response

class TimeoutHTTPAdapter(HTTPAdapter):
    def __init__(self, timeout, *args, **kwargs):
        """TimeoutHTTPAdapter constructor.

        Args:
            timeout (int): How many seconds to wait for the server to send data before
                giving up.
        """
        self.timeout = timeout
        super().__init__(*args, **kwargs)

    def send(self, request, **kwargs):
        """Override :obj:`HTTPAdapter` send method to add a default timeout."""
        timeout = kwargs.get("timeout")
        if timeout is None:
            kwargs["timeout"] = self.timeout

        return super().send(request, **kwargs)
