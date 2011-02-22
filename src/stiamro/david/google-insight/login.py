import urllib
import urllib2
import re


class GLogin(object):
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
    urllib2.install_opener(opener)
    login_page_url = 'https://www.google.com/accounts/ServiceLogin'
    authenticate_url = 'https://www.google.com/accounts/ServiceLoginAuth'


    def __init__(self, email, password):
        login_page_contents = self.opener.open(self.login_page_url).read()

        search_string = r'name="GALX"\s*value="([^"]+)"'
        galx_match_obj = re.search(search_string,
                                   login_page_contents,
                                   re.IGNORECASE)

        galx_value = ''
        if galx_match_obj.group(1):
            galx_value = galx_match_obj.group(1)

        login_params = urllib.urlencode( {
           'Email' : email,
           'Passwd' : password,
           'GALX': galx_value,
        })

        self.opener.open(self.authenticate_url, login_params)

    def get_opener(self):
        return self.opener
