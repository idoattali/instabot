import logging
import json

LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'


def create_logger(log_path=None):
    logger = logging.getLogger('instabot')
    logger.setLevel(logging.DEBUG)
    if log_path:
        fh = logging.FileHandler(log_path)
        fh.setLevel(logging.DEBUG)
        formatter = logging.Formatter(LOG_FORMAT)
        fh.setFormatter(formatter)
        logger.addHandler(fh)
    else:
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        formatter = logging.Formatter(LOG_FORMAT)
        ch.setFormatter(formatter)
        logger.addHandler(ch)
    return logger


def load_config(conf_file):
    with open(conf_file, 'r') as f:
        conf_text = f.read()
    return Struct(json.loads(conf_text))


class StoreAccount(object):
    def __init__(self, user_conf_path):
        self._user_conf = json.loads(open(user_conf_path, 'r').read())
        self._store_conf = json.loads(open(self._user_conf.get('store'), 'r').read())

        self._username = self._user_conf.get('username')
        self._email = self._user_conf.get('email')
        self._phone_number = self._user_conf.get('phone_number')
        self._display_name = self._store_conf.get('display_name')
        self._website = self._store_conf.get('website')
        self._bio = self._store_conf.get('bio')
        self._profile_picture = self._store_conf.get('profile_picture')
        self._pictures = self._store_conf.get('pictures')
        self._post_caption = self._store_conf.get('post_caption')

    @property
    def post_caption(self):
        return self._post_caption

    @property
    def pictures(self):
        return self._pictures

    @property
    def profile_picture(self):
        return self._profile_picture

    @property
    def email(self):
        return self._email

    @property
    def phone_number(self):
        return self._phone_number

    @property
    def display_name(self):
        return self._display_name

    @property
    def website(self):
        return self._website

    @property
    def bio(self):
        return self._bio

    @property
    def username(self):
        return self._username


class Struct(dict):
    """
    Example:
    m = Map({'first_name': 'Eduardo'}, last_name='Pool', age=24, sports=['Soccer'])
    """
    def __init__(self, *args, **kwargs):
        super(Struct, self).__init__(*args, **kwargs)
        for arg in args:
            if isinstance(arg, dict):
                for k, v in arg.iteritems():
                    self[k] = v

        if kwargs:
            for k, v in kwargs.iteritems():
                self[k] = v

    def __getattr__(self, attr):
        return self.get(attr)

    def __setattr__(self, key, value):
        self.__setitem__(key, value)

    def __setitem__(self, key, value):
        super(Struct, self).__setitem__(key, value)
        self.__dict__.update({key: value})

    def __delattr__(self, item):
        self.__delitem__(item)

    def __delitem__(self, key):
        super(Struct, self).__delitem__(key)
        del self.__dict__[key]
