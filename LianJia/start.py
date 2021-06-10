from scrapy import cmdline

# 这里使用 -o 文件名.csv -s FEED_EXPORT_ENCODING=UTF-8 将数据直接保存为csv文件，简单方便。
cmdline.execute("scrapy crawl LJ -o sz-lianjia.csv -s FEED_EXPORT_ENCODING=UTF-8".split())
# cmdline.execute("scrapy crawl LJ".split())