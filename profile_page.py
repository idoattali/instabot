import requests
import json

class ProfilePage(object):
    @staticmethod
    def getBasicInfo(profile_id):
        profile_json_url_format = 'https://i.instagram.com/api/v1/users/{0}/info/'
        profile_json_url = profile_json_url_format.format(profile_id)
        profile = requests.get(profile_json_url, verify=False)
        return json.loads(profile.content)
