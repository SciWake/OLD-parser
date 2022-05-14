# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import os
import csv
from itemadapter import ItemAdapter


class ReviewPipeline:
    def process_item(self, item, spider):
        return item


class CSVPipeline(object):
    def __init__(self):
        self.file = os.path.join(os.getcwd(), 'database.csv')

        with open(self.file, 'r', newline='', encoding='UTF-8') as csv_file:
            reader = csv.DictReader(csv_file)
            self.id_to_csv = [row['id'] for row in reader]
            self.column_name = reader.fieldnames

    def process_item(self, item, spider):
        csv_file = open(self.file, 'a', newline='', encoding='UTF-8')
        columns = item.fields.keys()

        data = csv.DictWriter(csv_file, columns)
        if not self.column_name:
            data.writeheader()
            self.column_name = True

        if item['id'] not in self.id_to_csv:
            data.writerow(item)
        csv_file.close()

        return item
