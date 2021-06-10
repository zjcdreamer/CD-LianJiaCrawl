# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class LjApartmentItem(scrapy.Item):
    # 公寓名称
    title = scrapy.Field()
    # 公寓最低单间价
    price = scrapy.Field()
    # 公寓地址
    address = scrapy.Field()
    # 公寓坐标（绘制地图备用）
    location = scrapy.Field()
    # 公寓介绍
    introduction = scrapy.Field()
    # 单间个数
    room_number = scrapy.Field()
    # 单间信息
    room_infos = scrapy.Field()
    # 房间链接
    room_url = scrapy.Field()


class LjZufangItem(scrapy.Item):
    # 房间名称
    title = scrapy.Field()
    # 房间价格
    price = scrapy.Field()
    # 发布日期
    publish_time = scrapy.Field()
    # 房间地址
    address = scrapy.Field()
    # 房间坐标（绘制地图备用）
    location = scrapy.Field()
    # 房间图片
    room_img = scrapy.Field()
    # 房间布局
    room_layout = scrapy.Field()
    # 房间面积
    room_area = scrapy.Field()
    # 房间朝向
    room_orientation = scrapy.Field()
    # 房间基本信息
    room_infos = scrapy.Field()
    # 周围环境描述
    surrounding_desc = scrapy.Field()
    # 房间链接
    room_url = scrapy.Field()
