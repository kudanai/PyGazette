from os import getenv
from dotenv import load_dotenv
import pygazette as po
from functools import wraps

load_dotenv()
client = po.Gazette()


def pre_authorize(func):
    @wraps(func)
    def wrapper(*args,**kwargs):
        if not client.token:
            client.authorize(getenv("CLIENT_ID"), getenv("CLIENT_SECRET"), auto_set=True)
        func(*args, **kwargs)
    return wrapper


def test_bad_category():
    try:
        client.fetch_page(iulaan_type=po.IulaanType.DENNEVUN, category=po.VazeefaType.FINANCE)
        assert False
    except RuntimeError as e:
        assert True


@pre_authorize
def test_page_fetch():
    stuff = client.fetch_page(iulaan_type=po.IulaanType.VAZEEFA, category=po.VazeefaType.FINANCE)
    assert len(stuff)


@pre_authorize
def test_page_fetch_enriched():
    stuff = client.fetch_page(iulaan_type=po.IulaanType.VAZEEFA, category=po.VazeefaType.FINANCE, extend_details=True)
    assert len(stuff)
    assert stuff[0].details is not None


@pre_authorize
def test_page_iteration():

    i = 1
    items = []
    for page in client.iter_pages(
            iulaan_type=po.IulaanType.VAZEEFA,
            category=po.VazeefaType.INFORMATION_TECHNOLOGY,
            extend_details=True):

        items.extend(page)
        i += 1
        if i > 3: break

    assert i > 1
    assert len(items) == 30


@pre_authorize
def test_item_fetch():
    test_id = 127342
    stuff = client.fetch_details(iulaan_id=test_id)
    assert stuff.iulaan_id == test_id
    assert stuff.details is not None
