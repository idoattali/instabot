class TagPage(object):
    def __init__(self, tag):
        self._tag = tag
        self._tag_json = {}

    def get_name(self):
        return self._tag

    def update_last_media(self, data):
        self._tag_json = data

    def get_media_list(self, first = None):
        media_list = self._tag_json['data']['hashtag']['edge_hashtag_to_media']['edges']
        if first:
            return media_list[:first]
        return media_list
