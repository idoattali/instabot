import json

from optparse import OptionParser

from instabot.utils.instagram_bot import InstagramBot
from instabot.utils.misc import create_logger


def load_config(conf_file):
    with open(conf_file, 'r') as f:
        conf_text = f.read()
    return json.loads(conf_text)


def main():
    options, args = get_opt()
    user_conf = load_config(options.file)
    create_logger(options.log)

    bot = InstagramBot(
        username=user_conf.get('username'),
        password=user_conf.get('password'),
        session_id=user_conf.get('sessionid'),
        tags=user_conf.get('tags'),
        like_sleep=user_conf.get('like_sleep')
    )

    bot.run()


def get_opt():
    parser = OptionParser()
    parser.add_option('-f', '--file', type='string')
    parser.add_option('-l', '--log', type='string')
    return parser.parse_args()


if __name__ == '__main__':
    main()