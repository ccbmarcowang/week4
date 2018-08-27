# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from sqlalchemy.orm import sessionmaker
from shiyanlou.models import Repository,engine
from datetime import datetime

class ShiyanlouPipeline(object):
    def process_item(self, item, spider):
        item['update_time']=datetime.strptime(' '.join(item['update_time'][:-1].split('T')),'%Y-%m-%d %H:%M:%S')
        item['releases']=int(item['releases'])
        item['branches']=int(item['branches'])
        if ',' in item['commits']:
            item['commits']=''.join(item['commits'].split(','))
        item['commits']=int(item['commits'])



        self.session.add(Repository(**item))
        return item
    def open_spider(self,spider):
    	Session=sessionmaker(bind=engine)
    	self.session=Session()
    def close_spider(self,spider):
    	self.session.commit()
    	self.session.close()
