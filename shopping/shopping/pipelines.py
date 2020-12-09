from itemadapter import ItemAdapter
from elasticsearch import Elasticsearch


class ShoppingPipeline:
    def open_spider(self, spider):
        self.es_url = spider.settings.attributes.get('ES_URL').value
        self.es_port = spider.settings.attributes.get('ES_PORT').value
        self.index = spider.settings.attributes.get('ES_INDEX').value
        self.dryrun = spider.settings.attributes.get('ES_DRYRUN').value
        if not self.dryrun:
            self.es = Elasticsearch([self.es_url], port=self.es_port)

    def close_spider(self, spider):
        pass

    def remove_lists(self, data: dict):
        for key, value in data.items():
            if isinstance(data[key], list):
                data[key] = data[key][0]
        return self

    def add_primary_key(self, data: dict):
        data['pk'] = "lidl-{}-{}".format(data['product_id'], data['week_number'])
        return self

    def save_item_to_elastic(self, data: dict):
        self.es.index(
            index=self.index,
            id=data['pk'],
            body=data
        )

    def process_item(self, item, spider):
        data = ItemAdapter(item).asdict()
        self.remove_lists(data).add_primary_key(data)
        if not self.dryrun:
            self.save_item_to_elastic(data)
        return item
