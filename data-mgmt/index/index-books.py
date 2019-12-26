from elasticsearch_dsl import Document, Text, Integer, Float
from elasticsearch_dsl import Index
from elasticsearch_dsl import analyzer
from elasticsearch_dsl.connections import connections
from elasticsearch.helpers import bulk

from models import Book, session

connections.configure(default={'hosts': 'localhost:9200'})
title_analyzer = analyzer('title_analyzer',
                          tokenizer='whitespace',
                          filter=['lowercase'])


class BookDocument(Document):
    book_id = Integer()
    title = Text(analyzer='title_analyzer')
    rating = Integer()
    price = Float()
    thumbnail = Text()
    category = Text()
    currency = Text()

    def to_dict(self, **kwargs):
        self.meta.id = self.book_id
        return super(BookDocument, self).to_dict(**kwargs)

    class Index:
        name = 'books'


class BaseIndex(object):
    document = None
    analyzers = None

    def __init__(self, index_name):
        self.index = Index(index_name)

    def get_or_create(self):
        if self.index.exists():
            print('Ignoring any additional settings since index already exists')
        else:
            self._create_index()

    def _create_index(self):
        # define custom settings
        self.index.settings(number_of_shards=5, number_of_replicas=5)

        # register a document with the index
        if self.document:
            self.index.document(self.document)

        # attach custom analyzers to the index
        if isinstance(self.analyzers, list):
            for x in self.analyzers:
                self.index.analyzer(x)

        self.index.create()


class BookIndex(BaseIndex):
    document = BookDocument
    analyzers = [title_analyzer]


if __name__ == '__main__':
    BookIndex('books').get_or_create()
    book_docs = []
    for book in session.query(Book).all():
        book_doc = BookDocument(book_id=book.id,
                                title=book.title,
                                thumbnail=book.thumbnail,
                                rating=book.rating,
                                price=book.price,
                                category=book.category_obj.title,
                                currency=book.currency)
        book_doc.meta.index = 'books'
        book_docs.append(book_doc)
    bulk(connections.get_connection(), (doc.to_dict(include_meta=True) for doc in book_docs))
    session.close()
