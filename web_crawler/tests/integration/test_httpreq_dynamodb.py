import requests
import json


url = "https://e94zsuwqm3.execute-api.us-east-2.amazonaws.com/prod/websites"
get_url= "https://e94zsuwqm3.execute-api.us-east-2.amazonaws.com/prod/websites?websiteId=200"

def test_http_post_method():
    website = {"websiteId": "200", "web_URL": "hello.com"}
    r = requests.post (url, data= json.dumps(website))
    assert r.status_code == 200


def test_http_get_method():
    r = requests.get(get_url)
    assert r.status_code == 200


def test_http_patch_method():
    website = {"websiteId": "200", "updateKey": "web_URL", "updateValue":"yousaf.zxc"}
    r = requests.patch(url, data= json.dumps(website))
    assert r.status_code == 200

def test_http_delete_method():
    website = {"websiteId": "200"}
    r = requests.delete(url, data= json.dumps(website))
    assert r.status_code == 200