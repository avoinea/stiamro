# The file is licenced under Revision 42 of the Beerware Licence.
# <dbatranu@gmail.com> wrote this file. As long as you retain this notice you
# can do whatever you want with this stuff. If we meet some day, and you think
# this stuff is worth it, you can buy <dbatranu@gmail.com> a beer in return.
# David Batranu.

import urllib
from login import GLogin


class Insight(object):

    report_url = 'http://www.google.com/insights/search/overviewReport'

    def __init__(self, opener):
        self.opener = opener
        self.report = ''
        self.data = {}

    def get_report(self, country='RO', period='week'):
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
        mapping = {
            'week': 'today 7-d',
            'month': 'today 1-m',
            'year': 'today 12-m',
            }
        if mapping.has_key(period):
            return mapping[period]
        return period

    def parse_report(self):
        if '<html>' in self.report:
            self.save_report('bad_csv_data.txt')
            raise Exception, 'Login Failed!'

        columns = self.report.split('\n\n\n\n')
        column_top = columns[1].split('\n')[1:]
        column_rising = columns[2].split('\n')[1:]
        self.populate_data('top', column_top)
        self.populate_data('rising', column_rising)

    def populate_data(self, column, lst):
        if not self.data.has_key(column):
            self.data[column] = {}

        for i in range(len(lst)):
            line = lst[i]
            if line == '':
                continue
            term, stat = line.split(',')
            self.data[column][i+1] = (term, stat)

    def get_stat(self, tpe='rising'):
        return self.data[tpe]

    def save_report(self, filename):
        open(filename, 'wb').write(self.report)



if __name__ == "__main__":
    import getpass
    print 'Login is required to access the Google Insights report!'
    google_email = raw_input('Google email: ')
    google_password = getpass.getpass('Password: ')

    opener = GLogin(google_email, google_password).get_opener()
    data = Insight(opener)
    data.get_report('RO', 'week')
    report_top = data.get_stat('top')
    report_rising = data.get_stat('rising')

    from pprint import pprint
    pprint(report_top)
    pprint(report_rising)
    data.save_report('raport.csv') #optional

