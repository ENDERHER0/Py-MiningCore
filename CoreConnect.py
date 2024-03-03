import simplejson as json
import requests

with open("F:\\BitcoinCore\\Bitcoin\\BlockChain\\.cookie", "r") as creds:
    cookie = creds.read()

NODE_URL = "http://127.0.0.1:8332"
NODE_USER = cookie.split(":")[0]
NODE_PASSWORD = cookie.split(":")[1]


def rpc(method, params=[]):
    payload = json.dumps({
        "jsonrpc": "2.0",
        "id": "minebet",
        "method": method,
        "params": params
    })
    return requests.post(NODE_URL, auth=(NODE_USER, NODE_PASSWORD), data=payload).json()['result']


print(rpc('uptime'))
