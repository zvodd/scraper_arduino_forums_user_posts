# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exceptions import DropItem

class ConvertTimePipeline(object):
    def process_item(self, item, spider):
        item['time'] = self.convert_time(item['time'])
        return item

    def convert_time(self, tstring):
        # why am i doing this.... use date_time module

        minutes, hours = None, None
        month, day, year = None, None, None
        total_seconds = 0
        d_components = tstring.strip().split(",")
        time_str = d_components.pop()
        year = d_components.pop().strip()
        month, day = d_components.pop().strip().split(" ")
        t_components = time_str.strip().split(":")

        minutes, pm_am =  t_components.pop().split(" ")
        hours = t_components.pop().strip()

        for i, comp in enumerate(reversed(t_components)):
            if i == 1:
                minutes = int(comp)
                total_seconds += minutes * 60
            if i == 2:
                hours = int(comp)
                if pm_am == 'pm':
                    hours += 12
                total_seconds += hours * 3600

        total_seconds += int(day) * 24 * 3600

        print([year, month, day, hours, minutes])
        return total_seconds

class DbOutputPipeline(object):
    def __init__(self, *args, **kwargs):
        super(DbOutputPipeline, *args, **kwargs)
        from arduino_forum_user_posts import db_api
        self.db = db_api.AppDatabase();

    def process_item(self, item, spider):
        keys = ["post_id", "author_id", "title", "description", "time"]
        args = []
        for k in keys:
            args.append(item[k])

        self.db.push_entry(*args)
        return item