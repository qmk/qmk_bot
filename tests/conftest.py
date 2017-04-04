# coding=UTF-8
import pytest
from qmk_bot import app as qmk_bot_app

@pytest.fixture
def app():
    return qmk_bot_app
