"""
The file is licenced under Revision 42 of the Beerware Licence.
# <dbatranu@gmail.com> wrote this file. As long as you retain this notice you
# can do whatever you want with this stuff. If we meet some day, and you think
# this stuff is worth it, you can buy <dbatranu@gmail.com> a beer in return.
# David Batranu.
"""

import urllib
import urllib2
import re

class Insight(object):
    """ Insights report
    """
    report_url = 'http://www.google.com/insights/search/overviewReport'

    def __init__(self, opener):
        self.opener = opener
        self.report = ''
        self.data = {}

    def get_report(self, country='RO', period='week'):
        """ Get report
        """
        req_data = urllib.urlencode({
            'geo': country,
            'date': self.get_date_for_req(period),
            'content': '1',
            'export': '1',
            'hl': 'ro',
            'cmpt': 'geo', #q, geo, date
            })
        self.report = self.opener.open(self.report_url, req_data).read()
        self.parse_report()

    def get_date_for_req(self, period):
        """ Get data
        """
        mapping = {
            'week': 'today 7-d',
            'month': 'today 1-m',
            'year': 'today 12-m',
            }
        if mapping.has_key(period):
            return mapping[period]
        return period

    def parse_report(self):
        """ Parse
        """
        if '<html>' in self.report:
            self.save_report('bad_csv_data.txt')
            raise Exception, 'Login Failed!'

        columns = self.report.split('\n\n\n\n')
        column_top = columns[1].split('\n')[1:]
        column_rising = columns[2].split('\n')[1:]
        self.populate_data('top', column_top)
        self.populate_data('rising', column_rising)

    def populate_data(self, column, lst):
        """ Populate
        """
        if not self.data.has_key(column):
            self.data[column] = {}

        for i in range(len(lst)):
            line = lst[i]
            if line == '':
                continue
            term, stat = line.split(',')
            self.data[column][i+1] = (term, stat)

    def get_stat(self, tpe='rising'):
        """ Get stat
        """
        return self.data[tpe]

    def save_report(self, filename):
        """ Save
        """
        open(filename, 'wb').write(self.report)

class GLogin(object):
    """ Login
    """
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

        self.login_params = urllib.urlencode( {
           'Email' : email,
           'Passwd' : password,
           'GALX': galx_value,
        })

    def __call__(self):
        self.opener.open(self.authenticate_url, self.login_params)
        return self.opener
