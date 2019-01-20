import requests
import os
import json
import time

from requests_toolbelt import MultipartEncoder

requests.packages.urllib3.disable_warnings()


class InstagramSession(object):
    def __init__(self):
        self._session = requests.session()
        self._session.headers.update({
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Content-Length': '0',
            'Host': 'www.instagram.com',
            'Origin': 'https://www.instagram.com',
            'Referer': 'https://www.instagram.com/',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36',
            'X-Instagram-AJAX': '1',
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-Requested-With': 'XMLHttpRequest'
        })

    def full_login(self, username, password, session_id=None):
        self.get_main_page()
        if session_id:
            self.login_using_session(session_id)
        else:
            self.login(username, password)
        self.get_main_page()
        self.get_profile_page(username)

    def get_main_page(self):
        main_page = self._session.get('https://instagram.com/', verify=False)
        self._session.headers.update({'X-CSRFToken': main_page.cookies['csrftoken']})

        return main_page
    
    def login_using_session(self, session_id):
        self._session.cookies['sessionid'] = session_id

    def login(self, username, password):
        login_data = {'username': username, 'password': password, 'next': '/'}
        login_page = self._session.post('https://www.instagram.com/accounts/login/ajax/', verify=False, data=login_data,
                            allow_redirects=True)
        self._session.headers.update({'X-CSRFToken': login_page.cookies['csrftoken']})

        return login_page

    def get_media_page(self, media_short_code):
        media_url_format = 'https://www.instagram.com/p/{0}'
        media_url = media_url_format.format(media_short_code)
        try:
            media_page = self._session.get(media_url, verify = False)
            self._session.headers.update({'X-CSRFToken': media_page.cookies['csrftoken']})

            return media_page
        except Exception:
            pass

    def get_tag_page(self, tag):
        tag_page_url_format = 'https://www.instagram.com/explore/tags/{0}/'
        tag_page_url = tag_page_url_format.format(tag)
        try:
            tag_page = self._session.get(tag_page_url, vefiry = False)
            self._session.headers.update({'X-CSRFToken': tag_page.cookies['csrftoken']})

            return tag_page
        except Exception:
            pass

    def like(self, media_id):
        like_url_format = 'https://www.instagram.com/web/likes/{0}/like/'
        like_url = like_url_format.format(media_id)
        try:
            like_page = self._session.post(like_url, verify = False)
            self._session.headers.update({'X-CSRFToken': like_page.cookies['csrftoken']})

            return like_page
        except Exception:
            pass

    def get_tag_page(self, tag):
        tag_base_url = 'https://www.instagram.com/explore/tags/'
        tag_url = os.path.join(tag_base_url, tag)
        try:
            tag_page = self._session.get(tag_url, verify = False)
            self._session.headers.update({'X-CSRFToken': tag_page.cookies['csrftoken']})
            return tag_page
        except Exception:
            pass

    def get_tag_json(self, tag):
        tag_json_bae_url = 'https://www.instagram.com/graphql/query/?query_hash=f92f56d47dc7a55b606908374b43a314&variables=%7B%22tag_name%22%3A%22{0}%22%2C%22show_ranked%22%3Afalse%2C%22first%22%3A6%7D'
        tag_json_url = tag_json_bae_url.format(tag)
        tag_json = self._session.get(tag_json_url, verify=False)
        return json.loads(tag_json.content)

    def get_profile_page(self, username):
        profile_json_url_format = 'https://instagram.com/{0}'
        profile_json_url = profile_json_url_format.format(username)
        profile = self._session.get(profile_json_url, verify=False)
        return profile

    def get_profile_info(self, username):
        profile_json_url_format = 'https://instagram.com/{0}/?__a=1'
        profile_json_url = profile_json_url_format.format(username)
        profile = self._session.get(profile_json_url, verify=False)
        return profile

    def edit_account(self, username, display_name, bio, website, phone_number, email):
        edit_account_url = 'https://instagram.com/accounts/edit/'
        data = {
            'first_name': display_name,
            'email': email,
            'username': username,
            'phone_number': phone_number,
            'gender': '3',
            'biography': bio,
            'external_url': website,
            'chaining_enabled': 'on'
        }
        response = self._session.post(edit_account_url, data=data, verify=False)
        return response

    def upload_profile_picture(self, picture_bin, content_length):
        m = MultipartEncoder(
            fields={'profile_pic': ('profilepic.jpg', picture_bin, 'image/png')},
            boundary='----WebKitFormBoundaryx6wIh7mzMqDpTWZU'
        )
        new_h = self._session.headers.copy()
        new_h['Content-Type'] = m.content_type
        new_h['Content-Length'] = content_length
        upload_profile_url = 'https://www.instagram.com/accounts/web_change_profile_picture/'

        res = self._session.post(upload_profile_url, data=m, headers=new_h)

        if res.status_code == 200:
            return json.loads(res.content).get('has_profile_pic')

        return False

    def upload_post(self, picture_bin, content_length, caption):
        upload_id = self._upload_photo(picture_bin, content_length)
        self._configure_photo(upload_id, caption)

    def _upload_photo(self, picture_bin, content_length):
        m = MultipartEncoder(
            fields={
                'upload_id': (str(time.time()).replace('.', '')),
                'photo': ('photo.jpg', picture_bin, 'image/png'),
                'media_type': '1'
            },
            boundary='----WebKitFormBoundaryx6wIh7mzMqDpTWZU'
        )
        new_h = self._session.headers.copy()
        new_h['Content-Type'] = m.content_type
        new_h['Content-Length'] = content_length
        upload_profile_url = 'https://www.instagram.com/create/upload/photo/'

        res = self._session.post(upload_profile_url, data=m, headers=new_h)

        if res.status_code == 200:
            return json.loads(res.content).get('upload_id', -1)

        return -1

    def _configure_photo(self, upload_id, caption):
        configure_photo_url = 'https://instagram.com/create/configure/'
        data = {
            'upload_id': upload_id,
            'caption': caption,
            'usertags': '',
            'custom_accessibility_caption': '',
            'retry_timeout': ''
        }

        response = self._session.post(configure_photo_url, data=data, verify=False)
        return response
