# -*- coding: utf-8 -*-
import scrapy
from urllib import parse
from LianJia.items import LjApartmentItem, LjZufangItem
import re


class LjSpiderSpider(scrapy.Spider):
    name = 'LJ'
    allowed_domains = ['lianjia.com']
    page = 1
    start_urls = ['https://cd.lianjia.com/zufang/pg1/']

    def parse(self, response):
        """
        获取每一个租房详情页的链接
        :param response:
        :return:
        """
        links = response.xpath("//div[@class='content__list']/div/a/@href").extract()
        for link in links:
            # 补全详情页链接
            url = parse.urljoin(response.url, link)
            if url.find('apartment') != -1:
                yield scrapy.Request(url=url, callback=self.apartment_parse)
            else:
                yield scrapy.Request(url, callback=self.zufang_parse)
        # 翻页
        self.page += 1
        # page_urls = 'https://sz.lianjia.com/zufang/pg{}/'.format(self.page)
        page_urls = 'https://cd.lianjia.com/zufang/pg{}/'.format(self.page)
        # 爬取100页数据
        if self.page < 50:
            yield scrapy.Request(url=page_urls, callback=self.parse)
        else:
            print('爬取结束')

    def apartment_parse(self, response):
        """
        爬取公寓房间信息
        :param response:
        :return:
        """
        title = response.xpath("//p[contains(@class,'flat__info--title')]/text()").extract()[0].strip('\n').strip()
        # price = int("".join(response.xpath("//p[@class='content__aside--title']/span[last()]/text()").extract()).strip())
        price = response.xpath("/html/body/div[3]/div[1]/div[3]/div[2]/div[2]/div/span/text()").strip()
        # 将response.text中的特殊符号去掉，方便正则匹配
        text = re.sub(r"[{}\s':,;]", "", response.text)
        address = re.match(r".*g_conf.name=(.*)g_conf.houseCode.*", text).group(1)
        longitude = re.match(r".*longitude?(.*)latitude.*", text).group(1)
        latitude = re.match(r".*latitude?(.*)g_conf.name.*", text).group(1)
        # 将经纬度格式化，为之后数据可视化做准备
        location = longitude + "," +latitude
        room_url = response.url
        apartment_desc = response.xpath("//p[@data-el='descInfo']/@data-desc").extract()[0]
        introduction = apartment_desc.replace(r"<br />", "").replace("\n", "")
        li_list = response.xpath("//ul[@data-el='layoutList']/li")
        room_number = len(li_list)
        room = []
        for li in li_list:
            print(li)
            rooms = {}
            _type = li.xpath(".//p[@class='flat__layout--title']/text()").extract()[0]
            room_type = _type.replace("\n", "").strip(" ")
            room_img = li.xpath(".//img/@data-src").extract()[0]
            li_price = li.xpath(".//p[@class='flat__layout--title']/span/text()").extract()[0]
            room_price = li_price.replace("\n", "").strip(" ")
            area = li.xpath(".//p[@class='flat__layout--subtitle']/text()").extract()[0]
            room_area_str = area.replace("\n", "").replace(" ", "")
            room_area = re.match(r".*?(\d+).*", room_area_str)
            if room_area is None:
                room_area = "未知"
                room_price = "已满房"
            else:
                room_area = room_area.group(1)
            room_left = li.xpath(".//p[@class='flat__layout--subtitle']/span/text()").extract()[0]
            rooms['图片'] = room_img
            rooms['类型'] = room_type
            rooms['价格'] = room_price
            rooms['面积'] = room_area
            rooms['余房'] = room_left
            room.append(rooms)

        item = LjApartmentItem()
        item['title'] = title
        item['price'] = price
        item['address'] = address
        item['location'] = location
        item['introduction'] = introduction
        item['room_number'] = room_number
        item['room_infos'] = room
        item['room_url'] = room_url
        yield item

    def zufang_parse(self, response):
        """
        爬取业主出租房间信息
        :param response:
        :return:
        """
        title = response.xpath("//p[@class='content__title']/text()").extract()[0]
        # price = int(response.xpath("//p[@class='content__aside--title']/span/text()").extract()[0])/3
        price = response.xpath("/html/body/div[3]/div[1]/div[3]/div[2]/div[2]/div[1]/span/text()").extract()
        publish_time = "".join(response.xpath("//div[@class='content__subtitle']/text()").extract()).strip().split(" ")[-1]
        # 将response.text中的特殊符号去掉，方便正则匹配
        text = re.sub(r"[{}\s':,;]", "", response.text)
        address = re.match(r".*g_conf.name=(.*)g_conf.houseCode.*", text).group(1)
        longitude = re.match(r".*longitude?(.*)latitude.*", text).group(1)
        latitude = re.match(r".*latitude?(.*)g_conf.subway.*", text).group(1)
        # 将经纬度格式化，为之后数据可视化做准备
        location = longitude + "," + latitude
        room_url = response.url
        room_img = "".join(response.xpath("//div[@class='content__article__slide__item']/img/@data-src").extract())
        # conditions中有4项内容（租赁方式、布局、面积、朝向）
        # conditions = response.xpath("//p[@class='content__article__table']/span/text()").extract()
        # conditions = response.xpath("//p[@class='content__article__table']/span/text()").extract()
        # room_layout = conditions[1]
        # room_area = conditions[2]
        # room_orientation = conditions[3]
        room_infos = response.xpath("//div[@class='content__article__info']/ul/li/text()").extract()
        for index, li in enumerate(room_infos):
            if li.find("\xa0") != -1:
                del room_infos[index]
        surrounding = "".join(response.xpath("//p[@data-el='houseComment']/@data-desc").extract())
        surrounding_desc = surrounding.replace("<br />", "").replace("\n", "")
        item = LjZufangItem()
        item['title'] = title
        item['price'] = price
        item['publish_time'] = publish_time
        item['address'] = address
        item['location'] = location
        item['room_img'] = room_img
        # item['room_layout'] = room_layout
        # item['room_area'] = room_area
        # item['room_orientation'] = room_orientation
        item['room_infos'] = room_infos
        item['surrounding_desc'] = surrounding_desc
        item['room_url'] = room_url
        yield item
