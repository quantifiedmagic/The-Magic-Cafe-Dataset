import scrapy
import re

class GuestsSpider(scrapy.Spider):
    name = "guests"

    def start_requests(self):
        urls = [
            'https://www.themagiccafe.com/forums/guests.php?year=2002',
            'https://www.themagiccafe.com/forums/guests.php?year=2003',
            'https://www.themagiccafe.com/forums/guests.php?year=2004',
            'https://www.themagiccafe.com/forums/guests.php?year=2005',
            'https://www.themagiccafe.com/forums/guests.php?year=2006',
            'https://www.themagiccafe.com/forums/guests.php?year=2007',
            'https://www.themagiccafe.com/forums/guests.php?year=2008',
            'https://www.themagiccafe.com/forums/guests.php?year=2009',
            'https://www.themagiccafe.com/forums/guests.php?year=2010',
            'https://www.themagiccafe.com/forums/guests.php?year=2011',
            'https://www.themagiccafe.com/forums/guests.php?year=2012',
            'https://www.themagiccafe.com/forums/guests.php?year=2013',
            'https://www.themagiccafe.com/forums/guests.php?year=2014',
            'https://www.themagiccafe.com/forums/guests.php?year=2015',
            'https://www.themagiccafe.com/forums/guests.php?year=2016',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_main_forum)

    def parse_main_forum(self, response):
        for x in response.css("a.b"):
            tmp = x.attrib['href']
            if 'index' not in tmp:
                next_page = response.urljoin(tmp)
                yield scrapy.Request(next_page, callback=self.parse_sub_forum)

    def parse_sub_forum(self, response):
        for x in response.css("a.b"):
            tmp = x.attrib['href']
            next_page = response.urljoin(tmp)
            yield scrapy.Request(next_page, callback=self.parse_thread)

        for x in response.css("td.normal.bgc1.b.midtext")[0].css('a'):
            tmp = x.attrib['href']
            next_page = response.urljoin(tmp)
            yield scrapy.Request(next_page, callback=self.parse_sub_forum)

    def parse_thread(self, response):
        posts = response.css('table.normal')[1].css('tr')
        thread = {'posts':[], 'link':response.request.url}
        for post in posts:
            if 'Go to page' in post.css('::text').extract()[1]:
                thread['page'] = post.css('span.on_page::text').extract()[0]
                links = post.css('a')
                for link in links:
                    if link.attrib['title'] != 'Next Page':
                        tmp = link.attrib['href']
                        next_page = response.urljoin(tmp)
                        yield scrapy.Request(next_page, callback=self.parse_thread)
            else:
                if 'The Magic Cafe Forum Index' in post.css('::text').extract()[1]:
                    topics = [x.replace('» »','').strip() for x in post.css('::text').extract() if re.match(r"[a-zA-Z]", x.replace('» »', '').strip())]
                    thread['title'] = topics
                else:
                    username = post.css('td.normal.bgc1.c.w13.vat').css('strong::text')[0].extract()
                    date = post.css('td')[1].css('div.vt1.liketext')[0].css('div.like_left')[0].css('span.b::text')[1].extract().strip()
                    post_text = ' '.join(post.css('td')[1].css('div.w100::text').extract()).strip()
                    post = {'username': username, 'date':date, 'post':post_text}
                    thread['posts'].append(post)
        yield thread

