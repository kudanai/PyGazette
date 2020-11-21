from pygazette import Gazette, AuthResponse, IulaanType, VazeefaType
from os import path
import pickle


def get_client():
    """
    handle client auth from disk or new instance
    """
    if path.exists("auth.pickle"):
        with open("auth.pickle", "rb") as f:
            auth: AuthResponse = pickle.load(f)
            client = Gazette(auth.access_token)
    else:
        from dotenv import load_dotenv
        from os import getenv

        load_dotenv()
        client = Gazette()
        auth = client.authorize(getenv("CLIENT_ID"), getenv("CLIENT_SECRET"), auto_set=True)

        with open("auth.pickle", "wb") as f:
            pickle.dump(auth, f)

    return client


def main():
    client = get_client()

    i = 1
    items = []
    for page in client.iter_pages(iulaan_type=IulaanType.VAZEEFA, category=VazeefaType.INFORMATION_TECHNOLOGY, extend_details=True):
        items.extend(page)
        i += 1
        if i > 3: break

    from pprint import pprint
    pprint(items, indent=4)


if __name__ == "__main__":
    main()