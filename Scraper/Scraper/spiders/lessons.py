import scrapy
from scrapy.loader import ItemLoader
from ..items import Lesson


class LessonsSpider(scrapy.Spider):
    name = 'lessons'
    group = str()
    sem = str()
    sem_zim = ["01", "09", "10", "11", "12"]
    sem_let = ["02", "03", "04", "05", "06", "07", "08"]
    if sem == "letni":
        taken_sem = sem_let
    else:
        taken_sem = sem_zim

    def parse(self, response):
        lessons = response.xpath('//div[@class="lesson"]')
        for lesson in lessons:
            date = lesson.xpath('.//span[@class="date"]/text()').get()
            curr_day = date.split('_')[1]
            if curr_day in self.taken_sem:
                name = lesson.xpath('.//span[@class="name"]/text()').getall()
                full = lesson.xpath('.//span[@class="info"]/text()').get()
                id_prow = lesson.xpath('.//span[@class="sSkrotProwadzacego"]/text()').get()
                block = lesson.xpath('.//span[@class="block_id"]/text()').get()[-1:]
                short = name[0]
                form = name[1]
                place = name[2]
                nr_zajec = name[3].split('[')[1][:-1]

                l = ItemLoader(Lesson())
                l.add_value("date", date)
                l.add_value("group", self.group)
                l.add_value("block", block)
                l.add_value("id_prow", id_prow)
                l.add_value("place",place)
                l.add_value("form", form)
                l.add_value("short", short)
                l.add_value("full", full)
                l.add_value("nr", nr_zajec)
                self.log(f'Item values: {l.load_item()}')

                yield l.load_item()
