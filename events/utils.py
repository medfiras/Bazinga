from django.conf import settings

from django.utils.six import text_type
try:
    from django.utils.six.moves.urllib.parse import urlencode
except ImportError:
    from six.moves.urllib.parse import urlencode
from django.utils.encoding import smart_bytes

import urllib, random, datetime
try:
    from hashlib import sha1 as sha_constructor, md5 as md5_constructor
except ImportError:  # pragma: no cover
    from django.utils.hashcompat import sha_constructor, md5_constructor


def generate_sha1(string, salt=None):
    """
    Generates a sha1 hash for supplied string. Doesn't need to be very secure
    because it's not used for password checking. We got Django for that.
    :param string:
        The string that needs to be encrypted.
    :param salt:
        Optionally define your own salt. If none is supplied, will use a random
        string of 5 characters.
    :return: Tuple containing the salt and hash.
    """
    if not isinstance(string, (str, text_type)):
        string = str(string)

    if not salt:
        salt = sha_constructor(str(random.random()).encode('utf-8')).hexdigest()[:5]

    salted_bytes = (smart_bytes(salt) + smart_bytes(string))
    hash_ = sha_constructor(salted_bytes).hexdigest()

    return salt, hash_

def get_datetime_now():
    """
    Returns datetime object with current point in time.
    In Django 1.4+ it uses Django's django.utils.timezone.now() which returns
    an aware or naive datetime that represents the current point in time
    when ``USE_TZ`` in project's settings is True or False respectively.
    In older versions of Django it uses datetime.datetime.now().
    """
    try:
        from django.utils import timezone
        return timezone.now() # pragma: no cover
    except ImportError: # pragma: no cover
        return datetime.datetime.now()
