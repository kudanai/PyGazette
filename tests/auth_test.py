from os import getenv
from dotenv import load_dotenv
import pygazette as po

load_dotenv()
client = po.Gazette()


def test_env():
    assert getenv("CLIENT_ID") and getenv("CLIENT_SECRET")


def test_call_unauthed_fail():
    try:
        resp = client.fetch_page()
        assert False
    except Exception as e:
        assert True


def test_auth():
    auth = client.authorize(getenv("CLIENT_ID"), getenv("CLIENT_SECRET"))
    assert isinstance(auth, po.AuthResponse)
    assert auth.access_token


def test_bad_auth():
    try:
        client.authorize("bullshit", "more bullshit")
        assert False
    except Exception as e:
        assert True


def test_inline_auth():
    auth = client.authorize(getenv("CLIENT_ID"), getenv("CLIENT_SECRET"), auto_set=True)
    assert auth.access_token == client.token
