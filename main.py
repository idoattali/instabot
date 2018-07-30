import json
import logging

from optparse import OptionParser

from instagram_bot import InstagramBot

def load_config(conf_file):
    with open(conf_file, 'r') as f:
        conf_text = f.read()
    return json.loads(conf_text)

def create_logger(log_path):
    logger = logging.getLogger('instabot')
    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler(log_path)
    fh.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    logger.addHandler(fh)

def main():
    options, args = getopt()
    user_conf = load_config(options.file)
    create_logger(options.log)

    bot = InstagramBot(
        username=user_conf.get('username'),
        password=user_conf.get('password'),
        session_id=user_conf.get('session_id'),
        tags=user_conf.get('tags')
    )

    bot.run()

def getopt():
    parser = OptionParser()
    parser.add_option('-f', '--file', type='string')
    parser.add_option('-l', '--log', type='string')
    return parser.parse_args()

if __name__ == '__main__':
    main()