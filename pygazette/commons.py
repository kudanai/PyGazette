from functools import wraps
from typing import Optional, TypeVar, Type
from httpx import codes
from .models import IulaanType, VazeefaType

BASE_URL = "https://api.gazette.gov.mv"
AUTH_URL = f"{BASE_URL}/oauth/token"
T = TypeVar('T')


def requires_token(token):
    """
    decorator to mark function calls that require an auth token to function
    """
    def _decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not token:
                raise RuntimeError("Must provide auth token")
            else:
                return func(*args, **kwargs)

        return wrapper

    return _decorator


def get_detail_url(iulaan_id):
    return f"{BASE_URL}/iulaan/{iulaan_id}"


def get_query_url(iulaan_type: Optional[IulaanType] = None, category: Optional[VazeefaType] = None, page: int = 1):
    """
    constructs appropriate query URL for listing retrieval
    based on the input parameters
    """
    if category:
        if not iulaan_type:
            iulaan_type = IulaanType.VAZEEFA  # allow this default if only category is set

        if not iulaan_type == IulaanType.VAZEEFA:
            raise RuntimeError("category is only supported for vazeefa type")

    # build the URL for the status code
    url = f"{BASE_URL}/iulaan"
    if iulaan_type:
        url += f"/type/{iulaan_type.value}"
    if category:
        url += f"/category/{category.value}"
    if page:
        url += f"/page/{page}"

    return url


def parse_response(response, t_class: Type[T]) -> T:
    """
    helper method to marshall a response into an iulaan item
    """
    if response.status_code == codes.OK:
        j = response.json()
        res = t_class(**j)
        return res
    else:
        response.raise_for_status()

