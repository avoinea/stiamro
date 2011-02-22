from datetime import datetime
import sys
from urllib import urlopen

def run():
    page = sys.argv[1]
    logfile = sys.argv[2]
    logger = open(logfile, 'a+')
    logger.write('\n')

    now = datetime.now()
    hour = now.hour
    
    if hour not in [5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 0, 1]:
        logger.write('%s\t\t%s\t\tNOT IN UPDATE INTERVAL' % (now.strftime('%d-%m-%Y %H:%M'), '-'))
        logger.close()
        return

    try:
        conn = urlopen(page)
    except Exception, err:
        now = datetime.now()
        logger.write('%s\t\t%s\t\tNOT UPDATED' % (
            now.strftime('%d-%m-%Y %H:%M'),
            err
        ))
    else:
        text = conn.read()
        now = datetime.now()
        logger.write(text)

    # Memcache
    logger.write('\n')
    page = page.replace('/update', '', 1)
    browser = page.replace('http://127.0.0.1:16553/stiam.ro', 'http://stiam.ro', 1)
    try:
        conn = urlopen(browser)
    except Exception, err:
        now = datetime.now()
        logger.write('%s\t\t%s\t\tNOT CACHED' % (
            now.strftime('%d-%m-%Y %H:%M'),
            err
        ))
    else:
        text = conn.read()
        now = datetime.now()
        logger.write('%s\t-\tCACHED' % (
            now.strftime('%d-%m-%Y %H:%M')))

    logger.write('\n')
    mobile = page.replace('http://127.0.0.1:16553/stiam.ro', 'http://m.stiam.ro', 1)
    try:
        conn = urlopen(mobile)
    except Exception, err:
        now = datetime.now()
        logger.write('%s\t\t%s\t\tMOBILE NOT CACHED' % (
            now.strftime('%d-%m-%Y %H:%M'),
            err
        ))
    else:
        text = conn.read()
        now = datetime.now()
        logger.write('%s\t-\tMOBILE CACHED' % (
            now.strftime('%d-%m-%Y %H:%M')))

    logger.write('\n')
    sitemap = page.replace('http://127.0.0.1:16553/stiam.ro', 'http://stiam.ro', 1)
    try:
        conn = urlopen(sitemap + '/sitemap.xml')
    except Exception, err:
        now = datetime.now()
        logger.write('%s\t\t%s\t\tSITEMAP NOT CACHED' % (
            now.strftime('%d-%m-%Y %H:%M'),
            err
        ))
    else:
        text = conn.read()
        now = datetime.now()
        logger.write('%s\t-\tSITEMAP CACHED' % (
            now.strftime('%d-%m-%Y %H:%M')))

    logger.close()

if __name__ == '__main__':
    run()

