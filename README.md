## PyGazette - Python Wrapper for MV Gazette

This is a Python wrapper for the Maldives Gazette 
(Government publishing) API.

### Requirements

 * Python 3.7+

### Installation

 * Install the package with pip  
   `pip install git+https://github.com/kudanai/PyGazette.git`

**Obtaining Client Credentials**

Visit [Gazette API Page](https://api.gazette.gov.mv/),
and provide your details to obtain your `client_id` & `client_secret`

### Usage

The library provides basic interfaces to look through 
and query the api.

```python
from pygazette import Gazette, IulaanType, VazeefaType

# If you have an auth token already
client = Gazette(token="auth_token_value")

# Otherwise, Obtain an authorization token
# use auto_set=True to be able to use this client instance
# directly. Returns an AuthResponse object
# You must store and manage this token yourself for subsequent
# use. default expiry is 365 days

client = Gazette()
auth = client.authorize("CLIENT_ID","CLIENT_SECRET", auto_set=True)
print(auth.access_token)

# fetch get a page from the listings
# exten_details makes a second call to the details
# automatically and enriches the response list
# returns a list of Iulaan objects

it_jobs = client.fetch_page(
    iulaan_type=IulaanType.VAZEEFA,
    category=VazeefaType.INFORMATION_TECHNOLOGY,
    page=1,
    extend_details=True
)
print(it_jobs)

# OR iterate through pages. Has the same prototype
# as fetch_page, except that it's a generator
# WARNING: the iterator will continue to hit,
# you must provide your own stop conditions

all_items = list()
for page_items in client.iter_pages():
    all_items.extend(page_items)
    print(page_items)
    


# fetch a specific Iulaan
deets_12314 = client.fetch_details(iulaan_id=12314)
print(deets_12314)
```

### Tests
`pytest` based test coverage is included

* `pip install pytest python-dotenv`
* setup a `.env` for the tests to pickup credentials (see sample)
* `pytest --verbose`

**sample `.env`**
```.env
CLIENT_ID=xxxx
CLIENT_SECRET=xxxx
```

### License

```
MIT License

Copyright (c) 2020 Naail Abdul Rahman (@kudanai)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```