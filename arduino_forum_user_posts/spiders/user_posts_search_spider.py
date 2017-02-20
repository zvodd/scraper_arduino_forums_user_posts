from __future__ import print_function
import scrapy
from scrapy.utils.project import get_project_settings
#from ipdb import set_trace as debug
from arduino_forum_user_posts.items import Post_Item
from arduino_forum_user_posts.request_object_parser import ChromeRequest
from scrapy.http.cookies import CookieJar
from lxml import html
from arduino_forum_user_posts.cookie_import import parse_cookies
import json

class UserPostSearchSpider(scrapy.Spider):
    
    name = 'arduino_spider'
    def __init__(self, *args, **kwargs):
        super(UserPostSearchSpider, self).__init__(*args, **kwargs)

        if "userid" not in kwargs:
            raise ValueError("Need argument 'userid' : -a userid=\"000000\"")    
        self.user_id = kwargs.get('userid')

        self.my_base_url = 'http://forum.arduino.cc'
        self.start_url = f'{self.my_base_url}/index.php?action=profile;area=showposts;u={self.user_id}'
        
        settings = get_project_settings()
        hf = settings.get("CHROME_HEADERS_FILE")
        cj = settings.get("COOKIES_JSON")
        if hf:
            ch = ChromeRequest.from_file(hf)
            self.init_cookies = ch.cookies
        elif cj:
            with open (cj, 'r') as fh:
                cookies = parse_cookies(fh.read())
                self.init_cookies = cookies

        if not hasattr(self, "init_cookies"):
            raise ValueError("Need to specify 'CHROME_HEADERS_FILE' "+
                             "or 'COOKIES_JSON' in settings.")


    def start_requests(self):
        """
        This overide gets the first page with cookies.
        """
        yield scrapy.Request(self.start_url, cookies=self.init_cookies)


    def parse(self, response):
        if response.status != 200:
            print("\n"*2," No Sign In" ,"\n")
            raise scrapy.exceptions.CloseSpider(reason='Not signed in on first page')

        page_contents = response.body_as_unicode()
        etree = html.fromstring(page_contents)
        posts = x = etree.xpath("(//div[contains(@class,'windowbg')])")
        for entry in posts:
            hitem = Post_Item()
            title_element = entry.cssselect("div.topic_details a")

            hitem['author_id'] = self.user_id

            if len(title_element) > 0:
                title_element = title_element.pop()
                hitem['title'] = title_element.text_content()
                hitem['post_id'] = title_element.get('href')

            date_el =  entry.cssselect("div.topic_details > span.smalltext")
            if len(date_el) > 0:
                hitem['time'] = date_el.pop().text

            descp_el = entry.cssselect('div.list_posts')
            if len(descp_el) == 1:
                descp_el = descp_el[0]
                hitem['description'] = html.tostring(descp_el)
            else:
                hitem['description'] = None
            yield hitem

        #find next url
        next_uri = etree.xpath("(//div[@class='pagelinks'])[last()]//*[@class='next_page']/parent::*/@href")
        if len(next_uri) > 0:
            yield scrapy.Request(f"{next_uri[0]}",
                                 cookies=self.init_cookies,
                                 callback=self.parse)
        else:
            raise scrapy.exceptions.CloseSpider(
                       reason='No more posts.')

