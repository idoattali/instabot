import os
import time
from optparse import OptionParser

from instabot.utils.instagram_session import InstagramSession
from instabot.utils.misc import create_logger, load_config, Struct, StoreAccount


def main():
    options, args = get_opt()
    user_conf = Struct(load_config(options.file))
    logger = create_logger(options.log)

    ig_session = InstagramSession()
    ig_session.full_login(user_conf.username, user_conf.password, user_conf.sessionid)
    store_account = StoreAccount(options.file)

    logger.info('Edit account information...')
    ig_session.edit_account(
        store_account.username,
        store_account.display_name,
        store_account.bio,
        store_account.website,
        store_account.phone_number,
        store_account.email
    )
    logger.info('Finished edit, wait for 5 seconds')
    time.sleep(60)

    logger.info('Upload new profile picture...')
    ig_session.upload_profile_picture(
        open(store_account.profile_picture, 'rb'),
        str(os.path.getsize(store_account.profile_picture))
    )
    logger.info('Finished upload profile picture, wait for 10 seconds')
    time.sleep(120)

    logger.info('Start upload posts, wait 2 minute between posts')
    for picture in store_account.pictures:
        logger.info('Upload post...')
        ig_session.upload_post(open(picture, 'rb'),
                               str(os.path.getsize(picture)),
                               store_account.post_caption)
        logger.info('Finished uploading, wait for 2 minutes')
        time.sleep(60*30)

    logger.info('Done')


def get_opt():
    parser = OptionParser()
    parser.add_option('-f', '--file', type='string')
    parser.add_option('-l', '--log', type='string', default=None)
    return parser.parse_args()


if __name__ == '__main__':
    main()
