import requests
from common import *

_user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36"

def post(url,headers=None,data=None):
    if headers is None:
        headers = {'User-Agent':_user_agent}
    else:
        headers['User-Agent'] = _user_agent
    
    for wait in range(1,8):
        try:
            res = _session.post(url,headers=headers,data=data,timeout=wait)
            break
        except Exception as e:
            get_Exception(e,wait)
    return res

def get(url):
    headers = {'User-Agent' : _user_agent}

    for wait in range(1,8):
        try:
            res = _session.get(url,headers=headers,timeout=wait)
            break
        except Exception as e:
            get_Exception(e,wait)
    return res

def cookie(name):
    return _session.cookies[name]

_session = requests.Session()