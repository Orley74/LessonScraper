# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import json
import neo4j
from neo4j import GraphDatabase
from itemadapter import ItemAdapter


class JsonWriterPipeline:
    uri = 'neo4j+s://b35e138c.databases.neo4j.io'
    auth = ("neo4j", 'VGfvQTk0VCkEzne79CGPXTKA_Eykhx0OwudLZUKG7sQ')
    driver = GraphDatabase.driver(uri, auth=auth,max_connection_lifetime=10000,max_connection_pool_size=10000)

    def open_spider(self, spider):
        self.session = self.driver.session(database='neo4j')

    def close_spider(self, spider):
        self.session.close()
        self.driver.close()

    def process_item(self, item, spider):
        line = ItemAdapter(item)


        self.session.run(
            """Merge (b:Block {id_prow: $id_prow, place: $place, date: $date, nr_bloku: $block})
            On Create
                SET
                b.id_prow = $id_prow,
                b.place = $place,
                b.date = $date,
                b.nr_zajec = $nr,
                b.groups = [$group],
                b.form = $form,
                b.short = $short,
                b.full = $full,
                b.nr_bloku = $block     
            On match
                SET b.groups = CASE
                    WHEN NOT $group IN b.groups THEN b.groups + $group
                    ELSE b.groups
            END
            """,
            date=line.get('date')[0], group=line.get('group')[0], block=line.get('block')[0], id_prow=line.get('id_prow')[0],
            place=line.get('place')[0], form=line.get('form')[0],short=line.get('short')[0], full=line.get('full')[0],
            nr=line.get('nr')[0])


        self.session.run("""match (g:Group), (b:Block)
                        Where  g.ID in b.groups
                        and b.date = $date
                        and b.nr_bloku = $block
                        MERGE (g)-[:zajecia_grupy]->(b)""",
                        date=line.get('date')[0], group=line.get('group')[0], block=line.get('block')[0])


        self.session.run("""match (p:Pracownik), (b:Block)
                    Where  b.id_prow = p.ID
                    and b.date = $date
                    and b.nr_bloku = $block
                    MERGE (p)-[:prowadzi_zajecia]->(b)""",
                     date=line.get('date')[0], block=line.get('block')[0],
                     id_prow=line.get('id_prow')[0])



        return item
