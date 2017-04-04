# coding=UTF-8
from flask import url_for


def test_index(client):
    res = client.get(url_for('index'))
    assert res.status_code == 200
    assert 'Hello, World!' in res.data

def test_push_hook(client):
    res = client.post('/postreceive', '{"foo":"bar"}')
    assert res.status_code == 400
