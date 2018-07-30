import requests
import json

class TagPage(object):
    def __init__(self, tag):
        self._tag = tag
        self._tag_json = {}

    def get_name(self):
        return self._tag

    def update_last_media(self):
        #tag_json_bae_url = 'https://www.instagram.com/graphql/query/?query_hash=ded47faa9a1aaded10161a2ff32abb6b&variables=%7B%22tag_name%22%3A%22{0}%22%2C%22first%22%3A6%7D'
        tag_json_base_url = 'https://www.instagram.com/explore/tags/{0}/?__a=1&max_id=3'
        tag_json_url = tag_json_base_url.format(self._tag)
        tag_json = requests.get(tag_json_url, verify = False)
        self._tag_json = json.loads(tag_json.content)

    def get_media_list(self, first = None):
        media_list = self._tag_json['graphql']['hashtag']['edge_hashtag_to_media']['edges']
        #ids_list = [media['node']['id'] for media in media_list]
        if first:
            return media_list[:first]
        return media_list