from scrapy import cmdline

name = 'stack'
cmdline.execute('scrapy crawl {0}'.format(name).split())
