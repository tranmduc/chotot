from scrapy import spiderloader
from scrapy.utils import project
from twisted.internet.defer import inlineCallbacks
from twisted.internet import reactor, defer
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging

configure_logging()
runner = CrawlerRunner()

@inlineCallbacks
def crawl():
    settings = project.get_project_settings()
    spider_loader = spiderloader.SpiderLoader.from_settings(settings)
    spiders = spider_loader.list()
    classes = [spider_loader.load(name) for name in spiders]
    for my_spider in classes:
        yield runner.crawl(my_spider)
    reactor.stop()

crawl()
reactor.run()