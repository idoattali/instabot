import logging

from datetime import datetime

from instagram_session import InstagramSession
from tag_page import TagPage
from filters import MediaFilter
import time

class InstagramBot(object):
    def __init__(self, username, password, session_id=None, tags=[], like_sleep=50, plan="regular"):
        self._session = InstagramSession()

        self._session.get_main_page()
        if session_id:
            self._session.login_using_session(session_id)
        else:
            self._session.login(username, password)
        self._session.get_main_page()

        self._username = username
        self._tags = [TagPage(tag) for tag in tags]
        self._logger = logging.getLogger('instabot')
        self._like_sleep = like_sleep
        self._plan = plan

    def _filter_by_plan(self, medias):
        if "follow_ratio" in self._plan:
            self._logger.info("Looking for new users in current media list")
            media_list = MediaFilter.standart_best_media(medias[:10])
            if len(media_list) > 0:
                self._logger.info("Found {0} users to use.".format(len(media_list)))
            else:
                self._logger.info("Cannot find users, probably there are no users who pass the filter.")
            return media_list
        if "dummy" in self._plan:
            self._logger.info("Choose the first media by \"dummy\" decision")
            return [medias[0]]
        self._logger.error("No plan!")

    def run(self):
        x = 1
        last_like = datetime(1970,1,1)
        start_time = datetime.now()
        while True:
            for tag in self._tags:
                try:
                    self._logger.info("--------------------------------------------------------------------------")
                    self._logger.info("Updating  and fetching media from tag '{0}'...".format(tag.get_name()))
                    tag.update_last_media()
                    media_list = tag.get_media_list()
                    self._logger.info("Tag currently has {0} medias".format(len(media_list)))

                    media_list = self._filter_by_plan(media_list)

                    tag_page = self._session.get_tag_page(tag.get_name())
                    time.sleep(2)

                    for media in media_list:
                        self._logger.info('')
                        self._logger.info("Bot is about to like this media: {0}".format(media['node']['shortcode']))

                        media_page = self._session.get_media_page(media['node']['shortcode'])
                        time.sleep(2)

                        time_diff = datetime.now() - last_like
                        seconds_diff = time_diff.total_seconds()
                        if seconds_diff < self._like_sleep:
                            to_wait = self._like_sleep - seconds_diff
                            self._logger.info('Sleeping for {0} seconds'.format(to_wait))
                            time.sleep(to_wait)
                            self._logger.info("Finished wait, go to like.")
                        like_page = self._session.like(media['node']['id'])
                        last_like = datetime.now()

                        self._logger.info("Media were liked, print metadata:")
                        self._logger.info("\t{0}:{1}".format("Username", self._username))
                        self._logger.info("\t{0}:{1}".format("Media short code:", media['node']['shortcode']))
                        self._logger.info("\t{0}:{1}".format("Media id", media['node']['id']))
                        self._logger.info("\t{0}:{1}".format("Page content (like answer)", like_page.content))
                        self._logger.info("\t{0}:{1}".format("Like number", x))
                        self._logger.info("\t{0}: {1}".format("Bot starts before", (last_like - start_time).total_seconds()))
                        x = x + 1
                    self._logger.info('')
                    self._logger.info('')
                except Exception as e:
                    self._logger.error("HUGE exception handled, exception: {0}".format(e.message))
                    time.sleep(10)
                    self._logger.error('')
                    self._logger.error('')
