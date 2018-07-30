import time
import logging

from profile_page import ProfilePage

logger = logging.getLogger('instabot')

class MediaFilter(object):
    @staticmethod
    def basic_remove_tags(medias):
        new_list = []
        for media in medias:
            try:
                if '@' not in media['node']['edge_media_to_caption']['edges'][0]['node']['text']:
                    new_list.append(media)
            except Exception:
                pass
        return new_list

    @staticmethod
    def get_only_low_text(medias):
        new_list = []
        for media in medias:
            try:
                text = media['node']['edge_media_to_caption']['edges'][0]['node']['text']
                text = text.split('#')[0]
                if len(text) < 100:
                    new_list.append(media)
            except Exception:
                pass
        return new_list

    @staticmethod
    def standart_best_media(medias):
        best_score = 0
        best_medias = []
        for media in medias:
            try:
                user_info = ProfilePage.getBasicInfo(media['node']['owner']['id'])
                time.sleep(2)
                following = user_info['user']['following_count']
                followers = user_info['user']['follower_count']
                cur_score = (float(following) / followers) * following
                if cur_score > best_score:
                    best_score = cur_score
                    best_medias = [media]
            except Exception:
                pass

        logger.info("Found user with {0} following".format(best_score))
        return best_medias

    @staticmethod
    def standart_filter(medias, first = 3):
        def check_media(media):
            try:
                user_info = ProfilePage.getBasicInfo(media['node']['owner']['id'])
                #if user_info['user']['following_count'] > (user_info['user']['follower_count']) * 1.2:
                if user_info['user']['following_count'] > 5000:
                    return True
                return False
            except Exception:
                return False

        filtered_list = []
        for media in medias:
            if check_media(media):
                filtered_list.append(media)
                if len(filtered_list) == first:
                    return filtered_list
        return filtered_list