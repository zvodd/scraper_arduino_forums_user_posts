# -*- coding: utf-8 -*-

# Scrapy settings for arduino_forum_user_posts project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'arduino_forum_user_posts'

SPIDER_MODULES = ['arduino_forum_user_posts.spiders']
NEWSPIDER_MODULE = 'arduino_forum_user_posts.spiders'
COOKIES_ENABLED = True
DOWNLOADER_MIDDLEWARES = {
	'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware' : 500
}
ITEM_PIPELINES = {
    'arduino_forum_user_posts.pipelines.ConvertTimePipeline': 301,
    'arduino_forum_user_posts.pipelines.DbOutputPipeline': 901,
}

# CHROME_HEADERS_FILE = "request_headers.txt"
COOKIES_JSON = "cookies.json"

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = ('arduino_forum_user_posts ' +
			 '(+https://github.com/zvodd)')
